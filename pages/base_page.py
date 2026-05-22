from playwright.async_api import Page, expect
from data.data_at_store import BASE_URL, BASE_URL_NO_WWW


class BasePage:

    def __init__(self, page_):
        self.page: Page = page_

    async def open(self, url="/"):
        await self.page.goto(url)

    async def check_url(self, endpoint="/index.html", www: bool = False):
        _base_url = BASE_URL_NO_WWW if not www else BASE_URL
        expect(self.page).to_have_url(_base_url + endpoint)

    async def check_logined_via_cookie(self):
        """
        проверка: куки 'customer' - есть
        - значит авторизация успешна
        """
        cookies = await self.page.context.cookies()
        print(f"{cookies=}")
        assert any(c['name'] == 'customer' for c in cookies), \
            "Нет куки 'customer' — логин не прошёл"
