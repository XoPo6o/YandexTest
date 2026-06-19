from dataclasses import dataclass


@dataclass(frozen=True)
class AuthTestData:
    valid_phone: str = "+7 (918) 252-93-84"
    new_phone: str = "+7 (918) 888-88-88"
    invalid_phone: str = "+7 (000) 000-00-00"
    blocked_email: str = "xs1089@gmail.com"
    valid_email: str = "kcio77@yandex.ru"


AUTH_DATA = AuthTestData()
