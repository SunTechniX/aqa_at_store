import time
from playwright.sync_api import APIRequestContext

from at_store.data.data_at_store import BASE_URL
from at_store.helpers.utils import extract_error_text
from at_store.tests.test_register_fixed import extract_visible_errors


class ApiBaseCtx:

    def __init__(self, ctx_):
        self.ctx = ctx_
        self.session: APIRequestContext = self.ctx.request
        self.auth_token = None
        self.response = None
        self.timestamp = int(time.time())

    def _check_status_code(self, expected_status_code: int = 200):
        assert self.response.status == expected_status_code, \
            f"Ожидали код {expected_status_code}, получили {self.response.status}"

    def get(self, endpoint: str, expected_status_code: int = 200):
        self.response = self.session.get(url=endpoint) #, headers=headers_)
        self._check_status_code(expected_status_code)
        return self.response

    def post(self, endpoint: str, data_json: dict = None,
             expected_status_code: int = 200):
        assert data_json is not None, "Тело не заполнено!"
        print(f"\n{data_json=}")
        try:
            # headers_ = {"Content-Type": "application/x-www-form-urlencoded"}
            self.response = self.session.post(url=endpoint, data=data_json)  # , headers=headers_)
        except ConnectionError as e:
            print("\n=== No Connection ===")
            raise AssertionError(e)
        self._check_status_code(expected_status_code)

    def post_form(self, endpoint: str, data_json: dict = None,
                  expected_status_code: int = 200):
        assert data_json is not None, "Тело не заполнено!"
        print(f"\n{data_json=}")
        # headers_ = {"Content-Type": "application/x-www-form-urlencoded"} - само вставится при использовании form=
        self.response = self.session.post(url=endpoint, form=data_json)  # , headers=headers_)
        self._check_status_code(expected_status_code)
        return self.response

    def post_form2(self, endpoint: str, data_json: dict = None,
                   expected_status_code: int = 200):
        assert data_json is not None, "Тело не заполнено!"
        print(f"\n{data_json=}")
        headers_ = {"Content-Type": "application/x-www-form-urlencoded"}
        self.response = self.session.post(url=endpoint, data=data_json, headers=headers_)
        self._check_status_code(expected_status_code)
        return self.response

    def close(self):
        pass

    def check_html_for_errors(self, save_html: bool = False):
        """ Ищем ошибки на Web-странице """
        # errors = extract_visible_errors(self.response.text())
        # if errors:
        #     print(f"❌ ОШИБКА СЕРВЕРА:")
        #     for e in errors:
        #         print(f"   • {e}")
        #     with open(f"error_on_web_{self.timestamp}.html", "w", encoding="utf-8") as f:
        #         f.write(self.response.text())
        #     assert False, f"Registration failed: {errors[0]}"
        error_text = extract_error_text(self.response.text())
        if error_text:
            print(f"❌ ОШИБКА СЕРВЕРА: [[ {error_text} ]]")
            if save_html:  # Сохраняем HTML для глубокой отладки (если нужно)
                with open(f"error_on_web_{self.timestamp}.html", "w",
                          encoding="utf-8") as f:
                    f.write(self.response.text())
                print(f"💾 Полный HTML сохранён в error_on_web_{self.timestamp}.html")
            raise AssertionError(f"Registration failed: [[ {error_text} ]]")

    def check_reg_form(self, save_html: bool = False):
        """ Если вернулась форма — возможно, тихая ошибка """
        if "AccountFrm" in self.response.text():
            print("⚠️ Вернулась форма регистрации — сохраняем для анализа")
            if save_html:
                with open(f"error_on_reg_form_{self.timestamp}.html", "w",
                          encoding="utf-8") as f:
                    f.write(self.response.text())

    def check_logined_via_cookie_api(self):
        """
        проверка: куки 'customer' - есть
        - значит авторизация успешна
        """
        cookies = self.ctx.cookies()
        assert any(c['name'] == 'customer' for c in cookies), \
            "Нет куки 'customer' — логин не прошёл"
