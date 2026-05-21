from api.store_api import ApiStore
from data.data_at_store import DATA_REGISTER_LOGIN, DATA_LOGIN, \
    DATA_REGISTER_LOGIN_FULL
from helpers.utils import load_data
from pages.login_create_page import LoginCreatePage
from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestAT:

    @staticmethod
    def interceptor(route):
        if route.request.resource_type not in ("font", "image", "script",
                                               "stylesheet", "xhr", "other"):
            print(f"🔍 {route.request.method} {route.request.url} [{route.request.resource_type}]")
            if route.request.resource_type == "document":
                if hasattr(route.request, "body") and route.request.body:
                    print(route.request.body[:50])
                if hasattr(route.request, "data") and route.request.data:
                    print(route.request.data[:50])
                if hasattr(route.request, "form") and route.request.form:
                    print(route.request.form[:50])
                if "create" in route.request.url:
                    print(route.request.__dict__)
        route.continue_()

    def test_01_at_login_simple(self, context, page):  # driver
        """ Просто Web-логин с имеющимся пользователем """

        at = MainPage(page)
        print()
        at.page.route("**/*", self.interceptor)
        at.open()
        at.click_login()

        # Страница Login
        at_login = LoginPage(page)
        # Нажали Continue
        at_login.click_btn_continue()

        data_for_register_form = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_login_form = DATA_LOGIN.copy()

        api = ApiStore(context)  # ApiStore(driver)
        tokens = at_login.csrftoken_create
        instance = at_login.csrfinstance_create
        load_data(data_for_register_form, tokens, instance)
        api.create_user(data_for_register_form)  # API Create

        at.page.wait_for_timeout(15_000)
        at.open()

        at.click_login()
        at_login.fill_login_form(data_for_login_form)
        at_login.click_btn_login()
        at.page.wait_for_timeout(15_000)

        # at.click_login()
        # at_reg.click_btn_login()
        #
        # # Отправить API-Login
        # api.login_open()
        #
        # tokens = at_reg.csrftoken_login
        # instance = at_reg.csrfinstance_login
        # load_data(data_for_login_form, tokens, instance)
        # api.login_user(data_for_register_form)
        #
        # at_reg.page.wait_for_timeout(2_000)
        # api.check_user()
        at.open()
        at.page.reload()
        at.page.wait_for_timeout(5_000)

    def test_02_create_web_login_api(self, context, page):  # driver
        at = MainPage(page)
        print()
        at.page.route("**/*", self.interceptor)
        at.open()
        at.click_login()

        at_login = LoginPage(page)
        # at_login.check_url("/index.php?rt=account/login")
        at_login.click_btn_continue()

        # данные
        data_for_register_form = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_login_form = DATA_LOGIN.copy()

        # 3. Страница формы создания Login-а
        # page.goto("index.php?rt=account/login")
        at_create = LoginCreatePage(page)
        #at_create.open()

        at_create.fill_login_create_form(data_for_register_form)
        at_create.click_btn_continue()

        at_create.page.wait_for_timeout(2_000)
        # at_login.page.pause()

        # 4. Идём логиниться
        at_login.open()
        at_login.check_url("/index.php?rt=account/login")

        tokens = at_login.csrftoken_login
        instance = at_login.csrfinstance_login
        load_data(data_for_login_form, tokens, instance)

        # pprint(data_for_login_form, indent=4)
        print(data_for_login_form)

        # Login via WEB
        # at.click_login()
        # at_login.fill_login_form(data_for_login_form)
        # at_login.click_btn_login()

        # 5 Login via API
        api = ApiStore(context)
        api.login_user(data_for_login_form)
        # at.page.reload()

        page.goto("/index.php?rt=account/account")

        at_login.page.wait_for_timeout(5_000)
        at_login.check_logined_via_cookie()

    def test_03_at_create_api_login_web(self, context, page):  # driver
        # 1. Главная
        at = MainPage(page)
        print()
        at.page.route("**/*", self.interceptor)
        at.open()
        at.click_login()

        # 2. Страница Login
        at_login = LoginPage(page)
        # Нажали Continue
        at_login.click_btn_continue()

        # page.goto("index.php?rt=account/create")
        # at_login.check_url("/index.php?rt=account/create")

        # 3. Страница формы создания Login-а

        # данные
        data_for_register_form = DATA_REGISTER_LOGIN.copy()
        data_for_login_form = DATA_LOGIN.copy()

        at_create = LoginCreatePage(page)
        tokens = at_create.csrftoken_create
        instance = at_create.csrfinstance_create
        load_data(data_for_register_form, tokens, instance)

        # at_create.fill_login_create_form(data_for_register_form)
        # at_create.click_btn_continue()

        api = ApiStore(context)
        api.create_user(data_for_register_form)
        # 5. Чекаем ошибки
        api.check_html_for_errors(save_html=True)
        # 6. Проверяем редирект в ЛК
        api.check_open()
        # 7. Если вернулась форма — возможно, тихая ошибка
        api.check_reg_form(save_html=True)

        at_create.page.wait_for_timeout(5_000)

        # Login via WEB
        at.click_login()
        at_login.fill_login_form(data_for_login_form)
        at_login.click_btn_login()

    def test_04_at_create_api_login_api(self, context, page):  # driver
        # 1. Главная
        at = MainPage(page)
        print()
        at.page.route("**/*", self.interceptor)
        at.open()
        at.click_login()

        # 2. Страница Login
        at_login = LoginPage(page)
        # Нажали Continue
        at_login.click_btn_continue()

        # page.goto("index.php?rt=account/create")
        # at_login.check_url("/index.php?rt=account/create")

        # 3. Страница формы создания Login-а

        # данные
        data_for_register_form = DATA_REGISTER_LOGIN.copy()
        data_for_login_form = DATA_LOGIN.copy()

        at_create = LoginCreatePage(page)
        tokens = at_create.csrftoken_create
        instance = at_create.csrfinstance_create
        load_data(data_for_register_form, tokens, instance)

        # -= API =-
        api = ApiStore(context)
        api.create_user(data_for_register_form)
        # 5. Чекаем ошибки
        api.check_html_for_errors()
        # 6. Проверяем редирект в ЛК
        api.check_open()
        # 7. Если вернулась форма — возможно, тихая ошибка
        api.check_reg_form(save_html=True)

        at_create.page.wait_for_timeout(5_000)
        # at_login.page.pause()

        at.open()

        # 4. Идём логиниться
        # at_login.open("/index.php?rt=account/login")
        at.click_login()
        at_login.page.wait_for_load_state("networkidle")
        # at_login.check_url("/index.php?rt=account/login")

        tokens = at_login.csrftoken_login
        instance = at_login.csrfinstance_login
        load_data(data_for_login_form, tokens, instance)

        # pprint(data_for_login_form, indent=4)
        print(data_for_login_form)

        # 5 Login via API
        api.login_user(data_for_login_form)
        at.page.reload()

        at.page.goto("/index.php?rt=account/account")

        at.page.wait_for_timeout(5_000)
        api.check_logined_via_cookie_api()
        at.check_logined_via_cookie()

