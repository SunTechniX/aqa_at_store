from api.store_api import ApiStore
from api.urls import EP_BASE, EP_USER_CABINET
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
                if hasattr(route.request, "post_data") and route.request.post_data:
                    # print(route.request.post_data)
                    from urllib.parse import parse_qs
                    print(parse_qs(route.request.post_data))
                if "create" in route.request.url:
                    print(route.request.__dict__)
        route.continue_()

    def test_01_at_login_simple(self, context, page):  # driver
        """ Просто Web-логин с имеющимся пользователем """
        context.route("**/*", self.interceptor)  # перехват своих api + страницы
        at = MainPage(page)
        print()
        # at.page.route("**/*", self.interceptor)  # перехват страницы
        at.open()
        at.click_login()

        # Страница Login
        at_login = LoginPage(page)
        # Нажали Continue
        at_login.click_btn_continue()

        data_for_register_form = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_login_form = DATA_LOGIN.copy()

        api = ApiStore(context)  # ApiStore(driver)
        at_create = LoginCreatePage(page)
        tokens = at_create.csrftoken_create
        instance = at_create.csrfinstance_create
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
        context.route("**/*", self.interceptor)  # перехват своих api + страницы
        # 1. Главная
        at = MainPage(page) # Основная страница
        print()
        at.open()  # открываем основную страницу
        at.click_login()  # Кликаем Login or Register

        # 2. Страница Login
        at_login = LoginPage(page) # Страница Login
        at_login.check_url(www=False)
        at_login.page.wait_for_load_state("networkidle")
        at_login.click_btn_continue() # Нажали Continue

        # формируем данные
        data_for_form_register = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_form_login = DATA_LOGIN.copy()

        # 3. Страница формы создания Login-а -> CreateLogin
        at_create = LoginCreatePage(page)
        at_create.fill_login_create_form(data_for_form_register)
        at_login.page.wait_for_load_state("networkidle")
        at_create.click_btn_continue()

        at_create.page.wait_for_timeout(2_000)
        # at_login.page.pause()

        # 4. Идём логиниться
        at_login.open()
        at_login.check_url(www=True)

        tokens = at_login.csrftoken_login
        instance = at_login.csrfinstance_login
        load_data(data_for_form_login, tokens, instance)  # в data_for_login_form прописываем token и instance

        # pprint(data_for_login_form, indent=4)
        print(data_for_form_login)

        # Login via WEB
        # at.click_login()
        # at_login.fill_login_form(data_for_login_form)
        # at_login.click_btn_login()

        # 5 Login via API
        api = ApiStore(context)
        api.login_user(data_for_form_login)
        # at.page.reload()

        page.goto("/index.php?rt=account/account")

        at_login.page.wait_for_timeout(5_000)
        at_login.check_logined_via_cookie()

    def test_03_at_create_api_login_web(self, context, page):  # driver
        context.route("**/*", self.interceptor)  # перехват своих api + страницы
        # формируем данные
        data_for_register_form = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_login_form = DATA_LOGIN.copy()
        print()

        # Сразу идём на нужную страницу
        at_create = LoginCreatePage(page)  # 3. Страница формы создания Login-а
        at_create.open()
        at_create.check_url(www=True)
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
        at = MainPage(page) # 1. Главная
        at.click_login()
        at_login = LoginPage(page) # 2. Страница Login
        at_login.fill_login_form(data_for_login_form)
        at_login.click_btn_login()

    def test_04_at_create_api_login_api(self, context, page):  # driver
        context.route("**/*", self.interceptor)  # перехват своих api + страницы
        # формируем данные
        data_for_form_register = DATA_REGISTER_LOGIN_FULL.copy()
        data_for_form_login = DATA_LOGIN.copy()
        print()

        # Сразу идём на нужную страницу
        at_create = LoginCreatePage(page)  # 3. Страница формы создания Login-а -> CreateLogin
        at_create.open()
        at_create.check_url(www=True)
        tokens = at_create.csrftoken_create
        instance = at_create.csrfinstance_create
        load_data(data_for_form_register, tokens, instance)  # в data_for_register_form прописываем token и instance
        at_create.page.wait_for_load_state("networkidle")

        # -= API =-
        api = ApiStore(context)
        api.create_user(data_for_form_register)  # создаём пользователя по API
        # Вместо fill_login_create_form

        print("_____ И вот ТУТ я Падаю _____")
        # 5. Чекаем ошибки
        api.check_html_for_errors()
        # 6. Проверяем редирект в ЛК
        api.check_open()
        # 7. Если вернулась форма — возможно, тихая ошибка
        api.check_reg_form(save_html=True)

        at = MainPage(page)  # 1. Главная
        at.open(EP_BASE + EP_USER_CABINET)
        at.check_url(EP_BASE + EP_USER_CABINET, www=True)
        at.page.wait_for_timeout(5_000)
        api.check_logined_via_cookie_api()
        at.check_logined_via_cookie()
