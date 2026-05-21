from playwright.sync_api import expect

from at_store.api.urls import EP_BASE, EP_USER_CREATE
from at_store.data.data_at_store import DATA_REGISTER_LOGIN, \
    DATA_REGISTER_LOGIN_FULL
from at_store.page.base_page import BasePage


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

    def open(self, url=EP_BASE + EP_USER_CREATE):
        self.page.goto(url)

    def get_hidden_input_value(self, name: str) -> str:
        """ Извлекает значение из hidden input по имени """
        self.page.wait_for_selector(f"[name='{name}']", state="attached")
        return self.page.locator(f"[name='{name}']").first.get_attribute("value")

    @property
    def csrftoken_create(self):
        return self.get_hidden_input_value("csrftoken")
        # return self._get_value(self.field_csrftoken_create)

    @property
    def csrfinstance_create(self):
        return self.get_hidden_input_value("csrfinstance")
        # return self._get_value(self.field_csrfinst_create)

    def fill_login_create_form(self, data_json: dict = DATA_REGISTER_LOGIN_FULL):
        self.field_firstname.fill(data_json["firstname"])
        self.field_lastname.fill(data_json["lastname"])
        self.field_email.fill(data_json["email"])
        self.field_telephone.fill(data_json["telephone"])

        self.field_company.fill(data_json["company"])
        self.field_address_1.fill(data_json["address_1"])
        self.field_address_2.fill(data_json["address_2"])
        self.field_city.fill(data_json["city"])
        self.field_postcode.fill(data_json["postcode"])
        # self.field_country_id.select_option("176")
        self.field_country_id.select_option(index=177)  # (label=data_json["country_id"])

        # self.field_zone_id.click()
        self.page.wait_for_timeout(1_000)
        self.field_zone_id.select_option("2795")
        # self.field_zone_id.select_option(index=1)   # (label=data_json["zone_id"])
        # self.field_zone_id.select_option("3607")
        # self.field_zone_id.select_option(index=12)

        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("Enter")

        self.field_loginname.fill(data_json["loginname"])
        self.field_password.fill(data_json["password"])
        self.field_confirm.fill(data_json["confirm"])
        self.field_newsletter0.click()
        self.chkbox_agree.check()

    def fill_login_create_form2(self, data_json: dict = DATA_REGISTER_LOGIN):
        self.field_firstname.fill(data_json["firstname"])
        self.field_lastname.fill(data_json["lastname"])
        self.field_email.fill(data_json["email"])
        self.field_telephone.fill(data_json["telephone"])
        self.field_loginname.fill(data_json["loginname"])
        self.field_password.fill(data_json["password"])
        self.field_confirm.fill(data_json["confirm"])
        self.field_newsletter0.click()
        self.chkbox_agree.check()

    def click_btn_continue(self):
        expect(self.btn_continue).to_be_visible()
        self.btn_continue.click()
