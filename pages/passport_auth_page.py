from playwright.sync_api import expect

from pages.base_page import BasePage


class PassportAuthPage(BasePage):
    """Page Object экранов авторизации Яндекс Паспорта."""

    # --- Локаторы ---

    @property
    def phone_input(self):
        return self.page.get_by_test_id("text-field-input")

    @property
    def next_phone_button(self):
        return self.page.get_by_test_id("split-add-user-next-phone")

    @property
    def next_login_button(self):
        return self.page.get_by_test_id("split-add-user-next-login")

    @property
    def auth_deny_submit(self):
        return self.page.get_by_test_id("auth-deny-submit")

    @property
    def webauth_button(self):
        return self.page.get_by_test_id("webauthn-auth-button")

    @property
    def magic_qr_button(self):
        return self.page.get_by_test_id("magic-btn")

    @property
    def switch_to_login_option(self):
        return self.page.get_by_test_id("menu-option-switchToLogin")

    @property
    def restore_account_option(self):
        return self.page.get_by_test_id("menu-option-restoreAccount")

    @property
    def error_message(self):
        return self.page.get_by_test_id("error-message")

    @property
    def forgot_login_link(self):
        return self.page.get_by_test_id("cant-login-forgot-login-link")

    @property
    def forgot_password_link(self):
        return self.page.get_by_test_id("cant-login-forgot-password-link")

    @property
    def password_button(self):
        return self.page.get_by_test_id("password-btn")

    @property
    def more_menu_button(self):
        return self.page.get_by_test_id("split-add-user-more-button")

    # --- Действия: телефон ---

    def wait_for_phone_screen(self, timeout: float = 15000) -> None:
        expect(self.phone_input).to_be_visible()
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

    def submit_phone(self, phone: str) -> None:
        self.phone_input.click()
        self.phone_input.fill(phone)
        self.next_phone_button.click()

    def assert_valid_notification_screen(self) -> None:
        """Проверяет экран пуш‑уведомления или капчи."""
        try:
            # Сначала проверяем экран пуш‑уведомления
            expect(self.page.get_by_text("Введите код из пуш-уведомления Яндекс Карты")).to_be_visible()
            # expect(self.page.get_by_text("Отправили на устройства, где есть приложения Яндекс")).to_be_visible()
        except Exception:
            # Если пуш не найден, проверяем экран капчи
            expect(self.page.get_by_role("heading", name="Введите фразу с картинки")).to_be_visible()


    def assert_new_notification_screen(self) -> None:
        """Проверяет экран пуш‑уведомления или капчи."""
        try:
            # Сначала проверяем экран пуш‑уведомления
            expect(self.page.get_by_role("heading", name="Нет аккаунтов с этим номером")).to_be_visible()
            # expect(self.page.get_by_text("Отправили на устройства, где есть приложения Яндекс")).to_be_visible()
        except Exception:
            # Если пуш не найден, проверяем экран капчи
            expect(self.page.get_by_role("heading", name="Введите фразу с картинки")).to_be_visible()


    def assert_invalid_phone_error(self) -> None:
        """Проверяет экран пуш‑уведомления или капчи."""
        try:
            # Сначала проверяем экран с ошибкой «Что-то пошло не так»
            self.expect_heading("Что-то пошло не так")
            # Проверяем видимость кнопки отказа от авторизации
            expect(self.auth_deny_submit).to_be_visible()
        except Exception:
            # Если первый экран не найден, проверяем экран капчи
            expect(self.page.get_by_role("heading", name="Введите фразу с картинки")).to_be_visible()

    # --- Действия: WebAuthn ---

    def open_webauth_login(self) -> None:
        self.webauth_button.click()

    def assert_webauth_error(self) -> None:
        expect(self.page.get_by_role("heading", name="Не удалось войти по лицу или отпечатку")).to_be_visible()


    # --- Действия: QR ---

    def open_qr_login(self) -> None:
        self.magic_qr_button.click()

    def assert_qr_screen(self) -> None:
        self.expect_text("Просканируйте QR")

    # --- Действия: логин / email ---

    def switch_to_login(self) -> None:
        self.open_more_menu()
        self.switch_to_login_option.click()
        self.expect_heading("Введите логин")

    def submit_login(self, email: str) -> None:
        self.phone_input.click()
        self.phone_input.fill(email)
        self.next_login_button.click()

    def assert_blocked_account_error(self) -> None:
        expect(self.error_message).to_be_visible()

    def assert_verification_methods_screen(self) -> None:
        """Проверяет экран пуш‑уведомления или капчи."""
        try:
            expect(self.page.get_by_text("Введите код из пуш-уведомления Яндекс — с Алисой")).to_be_visible()
        except Exception:
            self.expect_heading("Приложения, куда отправили код")

    def open_picture_login(self) -> None:
        self.page.get_by_role("button", name="Войти по картинке").click()
        self.expect_heading("Выберите такую картинку в Яндекс ID")

    def open_qr_from_verification(self) -> None:
        self.page.get_by_role("button", name="QR-код").click()
        self.assert_qr_screen()

    def open_password_screen(self) -> None:
        self.password_button.click()
        self.expect_heading("Введите пароль")

    def assert_password_screen_for_email(self, email: str) -> None:
        self.expect_text(f"Чтобы войти в аккаунт {email}")

    # --- Действия: восстановление доступа ---

    def open_restore_account(self) -> None:
        self.open_more_menu()
        self.restore_account_option.get_by_test_id("heading-title").click()
        self.expect_heading("Выберите привычный способ входа")

    def open_forgot_login(self) -> None:
        self.forgot_login_link.click()

    def open_forgot_password(self) -> None:
        self.forgot_password_link.click()

    def assert_enter_id_screen(self) -> None:
        self.expect_heading("Введите ID")
        # expect(self.page.get_by_role("heading", name="Восстановление доступа")).to_be_visible()

    def navigate_back_from_recovery(self) -> None:
        self.page.get_by_role("link", name="Назад").click()

    def open_more_from_recovery(self) -> None:
        self.page.get_by_role("link", name="Ещё").click()

    def switch_to_login_from_recovery(self) -> None:
        self.page.get_by_role("button", name="Войти по логину").click()

    def assert_more_menu_visible(self) -> None:
        expect(self.more_menu_button).to_be_visible()
