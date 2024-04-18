import types
try:
    from app.core import google_client
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `google_client`. '
        'Проверьте и поправьте: он должн быть доступен в модуле `app.core`.',
    )


def test_scopes():
    assert hasattr(google_client, 'SCOPES'), (
        'В файле `google_client` не обнаружена переменная `SCOPES`'
    )
    assert len(google_client.SCOPES) == 2, (
        'Убедитесь что количество объектов в `google_client.SCOPES` равно '
        'двум.'
    )
    for scope in google_client.SCOPES:
        assert any(s in scope for s in ['drive', 'spreadsheets']), (
            'В `google_client.SCOPES` не обнаружен необходимый уровень доступа'
        )


def test_info():
    assert hasattr(google_client, 'INFO'), (
        'В файле `google_client` не обнаружена переменная `INFO`'
    )
    info = google_client.INFO
    need_info_keys = [
        'type',
        'project_id',
        'private_key_id',
        'private_key',
        'client_email',
        'client_id',
        'auth_uri',
        'token_uri',
        'auth_provider_x509_cert_url',
        'client_x509_cert_url',
    ]

    for info_key in need_info_keys:
        assert info_key in info, (
            f'В объекте `google_client.INFO` не обнаружено ключа `{info_key}`'
        )


def test_connect():
    assert hasattr(google_client, 'get_service'), (
        'В файле `google_client` не обнаружена функция `get_service`'
    )
    service = google_client.get_service()
    assert isinstance(service, types.AsyncGeneratorType), (
        'Функция `google_client.get_service` должна возвращать асинхронный '
        'генератор.'
    )
