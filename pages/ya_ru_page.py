from playwright.sync_api import expect

from pages.base_page import BasePage


class YaRuPage(BasePage):
    URL = "https://ya.ru/"

    def open(self) -> None:
        self.goto(self.URL)
        expect(self.page.get_by_role("link", name="Войти")).to_be_visible()

    def click_login(self) -> None:
        self.page.get_by_role("link", name="Войти").click()
