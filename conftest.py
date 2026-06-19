import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from typing import Generator
from pages.passport_auth_page import PassportAuthPage
from pages.ya_ru_page import YaRuPage

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """Фикстура для запуска браузера с предустановленными настройками."""
    # Настройки для запуска браузера
    browser_launch_options = {
        "headless": True,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-notifications",
            "--disable-infobars",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--disable-save-password-bubble"
        ]
    }

    # Запуск Playwright
    playwright = sync_playwright().start()
    
    # Запуск браузера с указанными настройками
    browser = playwright.chromium.launch(**browser_launch_options)

    try:
        yield browser
    finally:
        # Гарантированная очистка: закрытие браузера и остановка Playwright
        browser.close()
        playwright.stop()

@pytest.fixture(scope="session")
def browser_context_args() -> dict:
    """Настройки для контекста браузера (без timeout и navigation_timeout)."""
    return {
        "locale": "ru-RU",
        "timezone_id": "Europe/Moscow",
        "geolocation": {"latitude": 55.7558, "longitude": 37.6173},
        "permissions": [],  # Запрещаем все разрешения по умолчанию
        "extra_http_headers": {
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        },
        "viewport": {"width": 1280, "height": 1024}  # Восстановлен viewport
    }

@pytest.fixture
def context(browser: Browser, browser_context_args: dict) -> BrowserContext: # type: ignore
    """Фикстура для создания контекста браузера."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Page: # type: ignore
    """Фикстура для страницы."""
    page = context.new_page()
    # Устанавливаем таймауты на уровне страницы
    page.set_default_timeout(60000)  # общий таймаут для действий
    page.set_default_navigation_timeout(60000)  # таймаут для навигации
    yield page

@pytest.fixture
def ya_ru_page(page: Page) -> YaRuPage:
    return YaRuPage(page)

@pytest.fixture
def passport_auth_page(page: Page) -> PassportAuthPage:
    return PassportAuthPage(page)

@pytest.fixture
def open_passport_login(ya_ru_page: YaRuPage, passport_auth_page: PassportAuthPage) -> PassportAuthPage:
    """Открывает ya.ru и переходит на экран входа в Паспорт."""
    try:
        ya_ru_page.open()
        ya_ru_page.click_login()
        passport_auth_page.wait_for_phone_screen()  # вызов метода с ()
        return passport_auth_page
    except Exception as e:
        print(f"Ошибка при открытии экрана входа: {e}")  # Исправлен синтаксис f-строки
        raise
