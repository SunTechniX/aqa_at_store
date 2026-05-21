from at_store.page.base_page import BasePage


class MainPage(BasePage):

    def __init__(self, page_):
        super().__init__(page_)
        self.btn_login = self.page.get_by_role(
            "link", name="Login or register"
            )

    def click_login(self):
        self.btn_login.click()