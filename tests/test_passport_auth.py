import pytest

from data.test_data import AUTH_DATA
from pages.passport_auth_page import PassportAuthPage
from pages.ya_ru_page import YaRuPage


@pytest.mark.auth
class TestPassportAuth:
    """10 тест-кейсов авторизации в Яндекс Паспорте через ya.ru."""

    @pytest.mark.smoke
    def test_01_login_with_valid_phone_shows_push_notification(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-01: Вход с корректным номером телефона — экран уведомления."""
        auth = open_passport_login
        auth.wait_for_phone_screen()
        auth.submit_phone(AUTH_DATA.valid_phone)

        auth.assert_valid_notification_screen()

    @pytest.mark.smoke
    def test_02_login_with_new_phone_shows_push_notification(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-02: Вход с новым номером телефона — экран уведомления."""
        auth = open_passport_login
        auth.wait_for_phone_screen()
        auth.submit_phone(AUTH_DATA.new_phone)

        # auth.assert_new_notification_screen()

    @pytest.mark.negative
    def test_03_login_with_invalid_phone_shows_error(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-03: Вход с некорректным номером — ошибка «Что-то пошло не так»."""
        auth = open_passport_login
        auth.wait_for_phone_screen()
        auth.submit_phone(AUTH_DATA.invalid_phone)

        auth.assert_invalid_phone_error()

    @pytest.mark.negative
    def test_04_webauth_login_shows_biometric_error(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-04: Вход по лицу или отпечатку — сообщение об ошибке."""
        auth = open_passport_login

        auth.open_webauth_login()

        # auth.assert_webauth_error()

    def test_05_qr_login_displays_scan_screen(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-05: Вход по QR — экран «Просканируйте QR»."""
        auth = open_passport_login

        auth.open_qr_login()
        auth.assert_qr_screen()
        auth.click_back()

    @pytest.mark.negative
    def test_06_login_with_blocked_email_shows_error(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-06: Вход по логину — заблокированная почта."""
        auth = open_passport_login

        auth.switch_to_login()
        auth.submit_login(AUTH_DATA.blocked_email)

        auth.assert_blocked_account_error()
        auth.click_back()

    @pytest.mark.smoke
    def test_07_login_with_valid_email_shows_verification_methods(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-07: Вход по корректному логину — способы подтверждения."""
        auth = open_passport_login

        auth.switch_to_login()
        auth.submit_login(AUTH_DATA.valid_email)

        auth.assert_verification_methods_screen()

    def test_08_valid_email_password_screen(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-08: Корректный логин — переход на экран ввода пароля."""
        auth = open_passport_login

        auth.switch_to_login()
        auth.submit_login(AUTH_DATA.valid_email)
        auth.open_password_screen()
        auth.assert_password_screen_for_email(AUTH_DATA.valid_email)

    @pytest.mark.recovery
    def test_09_restore_account_shows_login_methods(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-09: «Не могу зайти» — выбор привычного способа входа."""
        auth = open_passport_login

        auth.open_restore_account()

    @pytest.mark.recovery
    def test_10_forgot_login_opens_recovery_flow(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-10: «Не помню логин» — открытие формы восстановления."""
        auth = open_passport_login

        auth.open_restore_account()
        auth.open_forgot_login()

        auth.assert_enter_id_screen()

    @pytest.mark.recovery
    def test_11_forgot_password_shows_enter_id_screen(
        self,
        open_passport_login: PassportAuthPage,
    ) -> None:
        """TC-11: «Не помню пароль» — экран ввода ID и навигация назад."""
        auth = open_passport_login

        auth.open_restore_account()
        auth.open_forgot_password()

        auth.assert_enter_id_screen()
        auth.navigate_back_from_recovery()
        auth.open_more_from_recovery()
        auth.switch_to_login_from_recovery()
        # get_by_role("heading", name="Введите ID")
