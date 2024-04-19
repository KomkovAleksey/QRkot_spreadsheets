"""
Константы.
"""
MAX_PROJECT_NAME_LENGTH = 100
DEFAULT_INVESTED_AMOUNT = 0
DEFAULT_FULLY_INVESTED = False
MIN_ANYSTR_LENGTH = 1

TOKEN_VALIdITY_PERIOD = 3600
MIN_LEN_PASSWORD = 3

DATE_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
# Дата для заголовка таблицы в Google API
COLUMNS = 5  # Колонки таблицы в Google API
ROWS = 100  # Ряды таблицы в Google API
RANGE = 'A1:C30'


class ErrorText():
    """Текст ошибок."""

    PASSWORD_TOO_SHORT = 'Пароль должен состоять минимум из 3 символов.'
    EMAIL_IN_PASSWORD = 'Пароль не должен содержать адрес электронной почты.'
    NAME_DUPLICATE = 'Проект с таким именем уже существует!'
    PROJECT_NOT_FOUND = 'Проект не найден!'
    PROJECT_CLOSED = 'Проект закрыт, нельзя редактировать!.'
    PROJECT_WITH_FUNDS = 'Нельзя удалить проект с вложенными средстваим.'
    FULL_AMOUNT_ERROR = (
        'Новая полная сумма пожертвований не может быть меньше старой суммы.'
    )
