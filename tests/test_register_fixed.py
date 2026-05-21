"""
test_register_fixed.py
Регистрация на automationteststore.com через API — ИСПРАВЛЕННАЯ ВЕРСИЯ

Запуск:
    pytest test_register_fixed.py::test_api_register_fixed -v -s

✅ Исправления:
- loginname = только буквы/цифры (без @ и домена)
- email = полный email с доменом
- телефон с разделителями
- все обязательные поля адреса
"""
import re
import time
from playwright.sync_api import Page


def extract_visible_errors(html: str) -> list[str]:
    """Извлекает видимые сообщения об ошибках из HTML"""
    errors = []
    # Удаляем скрипты, стили, комментарии
    clean = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    
    patterns = [
        r'<div[^>]*class="[^"]*alert[^"]*error[^"]*"[^>]*>(?:<button[^>]*></button>)?\s*([^<]+)</div>',
        r'<div[^>]*class="[^"]*error[^"]*"[^>]*>([^<]+)</div>',
        r'<span[^>]*class="[^"]*error[^"]*"[^>]*>([^<]+)</span>',
        r'(?:^|[\s>])(Error|Warning|Notice):\s*([^<\.\n]+)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, clean, flags=re.IGNORECASE)
        for match in matches:
            text = match[-1].strip() if isinstance(match, tuple) else match.strip()
            if text and len(text) < 150 and '<' not in text and not text.startswith(('function', 'var', 'if', '$')):
                errors.append(text)
    return list(dict.fromkeys(errors))

# WORK
def test_api_register_fixed(page: Page):
    """
    Регистрация через API с исправленным loginname.
    
    🔑 КЛЮЧЕВОЕ:
    - loginname: только буквы и цифры (pytest_auto_12345)
    - email: полный адрес (pytest_auto_12345@gmail.com)
    """
    # 🔥 Генерируем данные
    timestamp = int(time.time())
    U_LOGIN = f"pytest_auto_{timestamp}"           # ← ТОЛЬКО буквы и цифры!
    U_EMAIL = f"{U_LOGIN}@gmail.com"                # ← Полный email
    U_PASS = "Aa1!StrongPass99"                     # Сложный пароль
    
    print(f"\n🔐 Регистрируем: login='{U_LOGIN}', email='{U_EMAIL}'")
    
    # 1. Открываем страницу
    page.goto("https://www.automationteststore.com/index.php?rt=account/create")
    page.wait_for_load_state("networkidle")
    
    # 2. CSRF из формы #AccountFrm (с большой буквы!)
    csrf_token = page.locator("#AccountFrm [name='csrftoken']").get_attribute("value")
    csrf_instance = page.locator("#AccountFrm [name='csrfinstance']").get_attribute("value")
    
    # 3. 🔥 ПОЛНЫЙ payload с РАЗДЕЛЬНЫМИ loginname и email
    payload = {
        # CSRF
        "csrftoken": csrf_token,
        "csrfinstance": csrf_instance,
        
        # 🔹 Личные данные
        "firstname": "Pytest",
        "lastname": "User",
        "email": U_EMAIL,              # ← pytest_auto_12345@gmail.com
        "telephone": "123-456-7890",   # ← С разделителями
        "fax": "",
        
        # 🔹 Адрес
        "company": "Test Inc",
        "address_1": "123 Main Street",
        "address_2": "",
        "city": "TestCity",
        "postcode": "12345",
        "country_id": "223",           # USA
        "zone_id": "3655",             # California
        
        # 🔹 Данные для входа (КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ!)
        "loginname": U_LOGIN,          # ← pytest_auto_12345 (БЕЗ @gmail.com!)
        "password": U_PASS,
        "confirm": U_PASS,
        
        # 🔹 Опции
        "newsletter": "0",
        "agree": "1",                  # ← Строка "1" для checkbox
    }
    
    # 4. Отправляем запрос
    response = page.request.post(
        "/index.php?rt=account/create",
        form=payload
    )
    
    # 🔍 Отладка
    print(f"🔍 Status: {response.status}")
    print(f"🔍 URL: {response.url}")
    
    # 5. Ищем реальные ошибки
    errors = extract_visible_errors(response.text())
    if errors:
        print(f"❌ Ошибки сервера:")
        for e in errors:
            print(f"   • {e}")
        with open(f"debug_register_error_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(response.text())
        assert False, f"Registration failed: {errors[0]}"
    
    # 6. Проверяем успех (редирект)
    if "account/account" in response.url or "success" in response.url.lower():
        print(f"✅ Регистрация успешна! Редирект в ЛК.")
        return
    
    # 7. Если вернулась форма — возможно, тихая ошибка
    if "AccountFrm" in response.text():
        print("⚠️  Вернулась форма регистрации — сохраняем для анализа")
        with open(f"debug_register_form_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(response.text())
    
    # 8. Пробуем залогиниться (проверка, создался ли аккаунт)
    print(f"🔄 Пробуем логин с loginname='{U_LOGIN}'...")
    page.goto("https://www.automationteststore.com/index.php?rt=account/login")
    page.wait_for_load_state("networkidle")
    
    csrf_login = page.locator("#loginFrm [name='csrftoken']").get_attribute("value")
    csrf_inst_login = page.locator("#loginFrm [name='csrfinstance']").get_attribute("value")
    
    login_payload = {
        "csrftoken": csrf_login,
        "csrfinstance": csrf_inst_login,
        "loginname": U_LOGIN,          # ← ТО ЖЕ имя, что при регистрации!
        "password": U_PASS,
        "account": "login"
    }
    
    login_resp = page.request.post(
        "/index.php?rt=account/login",
        form=login_payload
    )
    
    if login_resp.status == 200 and "Account Login" in login_resp.text():
        login_errors = extract_visible_errors(login_resp.text())
        if login_errors:
            print(f"❌ Ошибка логина: {login_errors[0]}")
        with open(f"debug_login_after_reg_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(login_resp.text())
        assert False, "Registration failed — login не прошёл. См. файлы debug_*.html"
    else:
        print(f"✅ Логин успешен! Аккаунт '{U_LOGIN}' создан и активен.")
