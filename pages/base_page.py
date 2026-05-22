from playwright.sync_api import Page, expect
from data.data_at_store import BASE_URL, BASE_URL_NO_WWW


class BasePage:

    def __init__(self, page_):
        self.page: Page = page_

    def open(self, url="/"):
        self.page.goto(url)

    def check_url(self, endpoint="/index.html", www: bool = False):
        _base_url = BASE_URL_NO_WWW if not www else BASE_URL
        expect(self.page).to_have_url(_base_url + endpoint)

    def check_logined_via_cookie(self):
        """
        проверка: куки 'customer' - есть
        - значит авторизация успешна
        """
        cookies = self.page.context.cookies()
        print(f"{cookies=}")
        assert any(c['name'] == 'customer' for c in cookies), \
            "Нет куки 'customer' — логин не прошёл"
