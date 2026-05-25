import pytest
from playwright.async_api import async_playwright, Browser, Page

from data.data_at_store import BASE_URL


@pytest.fixture
async def driver():
    async with async_playwright() as drv:
        yield drv

@pytest.fixture
async def context(driver):
    browser: Browser = await driver.chromium.launch(headless=False)
    context = await browser.new_context(base_url=BASE_URL)
    yield context
    await context.close()
    await browser.close()

@pytest.fixture
async def page(context):
    _page = await context.new_page()
    _page.set_default_timeout(8_000)
    return _page


# @pytest.fixture
# def api_login(page: Page):
#     """Фикстура: логинит пользователя через API и возвращает page в авторизованном состоянии"""
#
#     def _login(email: str, password: str):
#         page.goto(
#             "https://www.automationteststore.com/index.php?rt=account/login")
#
#         csrf_token = page.locator(
#             "#loginFrm [name='csrftoken']").get_attribute("value")
#         csrf_instance = page.locator(
#             "#loginFrm [name='csrfinstance']").get_attribute("value")
#
#         payload = {
#             "csrftoken": csrf_token,
#             "csrfinstance": csrf_instance,
#             "loginname": email,
#             "password": password,
#             "account": "login"
#         }
#
#         response = page.request.post(
#             "/index.php?rt=account/login",
#             form=payload
#         )
#         assert response.ok, f"Login failed: {response.status}"
#
#         # Обновляем страницу, чтобы браузер применил куки
#         page.goto("/index.php?rt=account/account", wait_until="networkidle")
#         return page
#
#     return _login
#
#
# # Использование в тесте:
# def test_my_account(api_login, page):
#     authorized_page = api_login("user@example.com", "pass123")
#     assert authorized_page.locator("text=My Account").is_visible()
#     # ... дальше тестирование ЛК
