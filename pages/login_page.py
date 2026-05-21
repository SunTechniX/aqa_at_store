from at_store.api.urls import EP_BASE, EP_USER_LOGIN
from at_store.data.data_at_store import DATA_LOGIN
from at_store.page.base_page import BasePage


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
        self.field_csrftoken_create = self.page.locator("#AccountFrm input[name='csrftoken']")
        self.field_csrfinst_create = self.page.locator("#AccountFrm input[name='csrfinstance']")
        self.field_csrftoken_login = self.page.locator("#loginFrm input[name='csrftoken']")
        self.field_csrfinst_login = self.page.locator("#loginFrm input[name='csrfinstance']")

    def open(self, url=EP_BASE + EP_USER_LOGIN):
        self.page.goto(url)

    def fill_login_form(self, data_dict: dict = DATA_LOGIN):
        self.field_name.fill(data_dict["loginname"])
        self.field_pass.fill(data_dict["password"])

    def click_btn_login(self):
        self.btn_login.click()

    def click_btn_continue(self):
        self.btn_continue.click()

    def _get_value(self, loc) -> str | tuple[str]:
        if len(loc.all()) > 1:
            items = []
            for item in loc.all():
                items.append(item.get_attribute("value", timeout=7_000))
        else:
            items = loc.get_attribute("value", timeout=7_000)
        return items

    @property
    def csrftoken_create(self):
        return self._get_value(self.field_csrftoken_create)

    @property
    def csrfinstance_create(self):
        return self._get_value(self.field_csrfinst_create)

    @property
    def csrftoken_login(self):
        return self._get_value(self.field_csrftoken_login)

    @property
    def csrfinstance_login(self):
        return self._get_value(self.field_csrfinst_login)