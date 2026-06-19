from playwright.sync_api import Page, expect


class BasePage:
    """Базовый Page Object с общими действиями и ожиданиями."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def click_back(self) -> None:
        self.page.get_by_test_id("back-button").click()

    def open_more_menu(self) -> None:
        self.page.get_by_test_id("split-add-user-more-button").click()

    def expect_visible(self, locator) -> None:
        expect(locator).to_be_visible()

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()

    def expect_text(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()
