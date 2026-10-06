from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url: str):
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()
