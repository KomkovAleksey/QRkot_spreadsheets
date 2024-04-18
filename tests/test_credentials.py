try:
    from app.core.config import settings
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен инициализированный объект `settings`.'
        'Проверьте и поправьте: он должен быть доступен в модуле '
        '`app.core.config`',
    )


def test_google_cred():
    need_cred = [
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
        'email',
    ]
    for cred in need_cred:
        assert hasattr(settings, cred), (
            f'В объекте `app.core.config.Settings` нет атрибута `{cred}`'
        )
