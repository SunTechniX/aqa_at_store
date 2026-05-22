from playwright.async_api import expect

from api.urls import EP_BASE, EP_USER_CREATE
from data.data_at_store import DATA_REGISTER_LOGIN, \
    DATA_REGISTER_LOGIN_FULL
from pages.base_page import BasePage


class LoginCreatePage(BasePage):

    def __init__(self, page_):
        super().__init__(page_)
        self.field_firstname = self.page.locator("#AccountFrm_firstname")
        self.field_lastname = self.page.locator("#AccountFrm_lastname")
        self.field_email = self.page.locator("#AccountFrm_email")
        self.field_telephone = self.page.locator("#AccountFrm_telephone")

        self.field_company = self.page.locator("#AccountFrm_company")
        self.field_address_1 = self.page.locator("#AccountFrm_address_1")
        self.field_address_2 = self.page.locator("#AccountFrm_address_2")
        self.field_city = self.page.locator("#AccountFrm_city")
        self.field_zone_id = self.page.locator("#AccountFrm_zone_id")  # 2795
        self.field_postcode = self.page.locator("#AccountFrm_postcode")
        self.field_country_id = self.page.locator("#AccountFrm_country_id")  # "Russia" 176

        self.field_loginname = self.page.locator("#AccountFrm_loginname")
        self.field_password = self.page.locator("#AccountFrm_password")
        self.field_confirm = self.page.locator("#AccountFrm_confirm")
        self.field_newsletter0 = self.page.locator("#AccountFrm_newsletter0")

        self.chkbox_agree = self.page.locator("#AccountFrm_agree")

        self.btn_continue = self.page.get_by_role(
            "button", name="Continue"
            )

        # self.field_csrftoken_create = self.page.locator("#AccountFrm input[name='csrftoken']")
        # self.field_csrfinst_create = self.page.locator("#AccountFrm input[name='csrfinstance']")


    async def open(self, url=EP_BASE + EP_USER_CREATE):
        await self.page.goto(url)

    async def check_url(self, endpoint=EP_BASE + EP_USER_CREATE, www: bool = False):
        await super().check_url(endpoint, www)

    async def get_hidden_input_value(self, name: str) -> str:
        """ Извлекает значение из hidden input по имени """
        self.page.wait_for_selector(f"[name='{name}']", state="attached")
        return self.page.locator(f"[name='{name}']").first.get_attribute("value")

    # @property
    async def csrftoken_create(self):
        return await self.get_hidden_input_value("csrftoken")
        # return self._get_value(self.field_csrftoken_create)

    # @property
    async def csrfinstance_create(self):
        return await self.get_hidden_input_value("csrfinstance")
        # return self._get_value(self.field_csrfinst_create)

    # @property
    # def csrftoken_create(self):
    #     return self.field_csrftoken_create.get_attribute("value")
    #
    # @property
    # def csrfinstance_create(self):
    #     return self.field_csrfinst_create.get_attribute("value")

    async def fill_login_create_form(self, data_json: dict = DATA_REGISTER_LOGIN_FULL):
        await self.field_firstname.fill(data_json["firstname"])
        await self.field_lastname.fill(data_json["lastname"])
        await self.field_email.fill(data_json["email"])
        await self.field_telephone.fill(data_json["telephone"])

        await self.field_company.fill(data_json["company"])
        await self.field_address_1.fill(data_json["address_1"])
        await self.field_address_2.fill(data_json["address_2"])
        await self.field_city.fill(data_json["city"])
        await self.field_postcode.fill(data_json["postcode"])
        # self.field_country_id.select_option("176")
        await self.field_country_id.select_option(index=177)  # (label=data_json["country_id"])

        # self.field_zone_id.click()
        await self.page.wait_for_timeout(1_000)
        await self.field_zone_id.select_option("2795")
        # self.field_zone_id.select_option(index=1)   # (label=data_json["zone_id"])
        # self.field_zone_id.select_option("3607")
        # self.field_zone_id.select_option(index=12)

        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("Enter")

        await self.field_loginname.fill(data_json["loginname"])
        await self.field_password.fill(data_json["password"])
        await self.field_confirm.fill(data_json["confirm"])
        await self.field_newsletter0.click()
        await self.chkbox_agree.check()

    async def fill_login_create_form2(self, data_json: dict = DATA_REGISTER_LOGIN):
        await self.field_firstname.fill(data_json["firstname"])
        await self.field_lastname.fill(data_json["lastname"])
        await self.field_email.fill(data_json["email"])
        await self.field_telephone.fill(data_json["telephone"])
        await self.field_loginname.fill(data_json["loginname"])
        await self.field_password.fill(data_json["password"])
        await self.field_confirm.fill(data_json["confirm"])
        await self.field_newsletter0.click()
        await self.chkbox_agree.check()

    async def click_btn_continue(self):
        expect(self.btn_continue).to_be_visible()
        await self.btn_continue.click()
