from api.urls import EP_BASE, EP_USER_LOGIN
from data.data_at_store import DATA_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page_):
        super().__init__(page_)
        self.field_name = self.page.locator("#loginFrm_loginname")
        self.field_pass = self.page.locator("#loginFrm_password")
        self.btn_login = self.page.get_by_role(
            "button", name="Login"
            )
        self.btn_continue = self.page.get_by_role(
            "button", name="Continue"
            )
        # self.field_csrftoken = self.page.locator("[name='csrftoken']")
        # self.field_csrfinst = self.page.locator("[name='csrfinstance']")
        # self.field_csrftoken_create = self.page.locator("#AccountFrm input[name='csrftoken']")
        # self.field_csrfinst_create = self.page.locator("#AccountFrm input[name='csrfinstance']")
        self.field_csrftoken_login = self.page.locator("#loginFrm input[name='csrftoken']")
        self.field_csrfinst_login = self.page.locator("#loginFrm input[name='csrfinstance']")

    async def open(self, url=EP_BASE + EP_USER_LOGIN):
        await self.page.goto(url)

    async def check_url(self, endpoint=EP_BASE + EP_USER_LOGIN, www: bool = False):
        await super().check_url(endpoint, www)

    async def fill_login_form(self, data_dict: dict = DATA_LOGIN):
        await self.field_name.fill(data_dict["loginname"])
        await self.field_pass.fill(data_dict["password"])

    async def click_btn_login(self):
        await self.btn_login.click()

    async def click_btn_continue(self):
        await self.btn_continue.click()

    async def _get_value(self, loc) -> str | list[str]:
        if len(await loc.all()) > 1:
            items = []
            for item in await loc.all():
                items.append(await item.get_attribute("value", timeout=7_000))
        else:
            items = await loc.get_attribute("value", timeout=7_000)
        return items

    # @property
    # def csrftoken_create(self):
    #     return self._get_value(self.field_csrftoken_create)
    #
    # @property
    # def csrfinstance_create(self):
    #     return self._get_value(self.field_csrfinst_create)

    # @property
    async def csrftoken_login(self) -> str | list[str]:
        return await self._get_value(self.field_csrftoken_login)

    # @property
    async def csrfinstance_login(self) -> str | list[str]:
        return await self._get_value(self.field_csrfinst_login)