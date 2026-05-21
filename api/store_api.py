from at_store.api.base_api import ApiBaseCtx
from at_store.api.urls import EP_BASE, EP_USER_CREATE, EP_USER_SUCCESS, \
    EP_USER_LOGIN
from at_store.data.data_at_store import BASE_URL


class ApiStore(ApiBaseCtx):

    def create_user(self, data_json: dict):
        """
        https://automationteststore.com/index.php?rt=account/create
        POST
        """
        endpoint = EP_BASE + EP_USER_CREATE
        # endpoint = BASE_URL + EP_BASE + EP_USER_CREATE
        print(f"🔍 POST-form Create: {endpoint=}")
        self.response = self.post_form(endpoint, data_json=data_json,
                                       expected_status_code=200)  # 302
        return self.response

    def check_open(self, expected_url_part: str = "account/account",
                   msg: str = "✅ Регистрация успешна! Редирект в ЛК."):
        if expected_url_part in self.response.url:
            print(msg)
            return

    def login_open(self):
        endpoint = EP_BASE + EP_USER_LOGIN
        print(f"🔍 GET Open: {endpoint=}")
        self.response = self.get(endpoint, expected_status_code=200)
        return self.response

    def login_user(self, data_json: dict):
        endpoint = EP_BASE + EP_USER_LOGIN
        print(f"🔍 POST-form Login: {endpoint=}")
        self.response = self.post_form(endpoint, data_json=data_json,
                                       expected_status_code=200)  # 302
        return self.response

    def check_user(self):
        endpoint = EP_BASE + EP_USER_SUCCESS
        print(f"🔍 GET Check: {endpoint=}")
        self.response = self.get(endpoint)
        return self.response
