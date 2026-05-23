from playwright.async_api import Page

from data.data_at_store import U_NAME, U_PASS


# WORK
def test_api_login_automationteststore(page: Page):
    # 1. Открываем логин
    page.goto("https://www.automationteststore.com/index.php?rt=account/login")

    # 2. CSRF
    csrf_token = page.locator("#loginFrm [name='csrftoken']").get_attribute(
        "value")
    csrf_instance = page.locator(
        "#loginFrm [name='csrfinstance']").get_attribute("value")

    # 3. Payload
    payload = {
        "csrftoken": csrf_token,
        "csrfinstance": csrf_instance,
        "loginname": U_NAME,
        "password": U_PASS,
        "account": "login"
    }

    # 4. API-логин
    response = page.request.post(
        "/index.php?rt=account/login",
        form=payload
    )
    assert response.ok, f"Login request failed: {response.status}"

    # 5. Переход в ЛК
    page.goto("/index.php?rt=account/account", wait_until="networkidle")
    page.wait_for_timeout(5_000)

    # 6. 🔥 Надёжная проверка: кука 'customer' = авторизация успешна
    cookies = page.context.cookies()
    assert any(c['name'] == 'customer' for c in cookies), \
        "Нет куки 'customer' — логин не прошёл"

    # 7. Опционально: визуальная проверка (если нужна)
    # Если хочешь проверить интерфейс — раскомментируй:
    # assert page.locator("h1").first.text_content().lower().count("account") > 0

    print("✅ Логин успешен!")
