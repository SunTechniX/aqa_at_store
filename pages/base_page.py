class BasePage:

    def __init__(self, page):
        self.page = page

    def open(self, link):
        self.page.go_to(link)
