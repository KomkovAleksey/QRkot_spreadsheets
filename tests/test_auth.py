REGISTER_URL = '/auth/register'


def test_register(test_client):
    user_data = {
        'email': 'dead@pool.com',
        'password': 'chimichangas4life',
    }
    response = test_client.post(REGISTER_URL, json=user_data)
    assert response.status_code == 201, (
        'Проверьте статус ответа API: при регистрации пользователя '
        f'корректный POST-запрос к эндпоинту {REGISTER_URL} '
        'должен вернуть ответ со статусом 201.'
    )
    data = response.json()
    expected_keys = {
        'id',
        'email',
        'is_active',
        'is_superuser',
        'is_verified',
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        f'В ответе на корректный POST-запрос к эндпоинту `{REGISTER_URL}` не '
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    data.pop('id')
    assert data == {
        'email': user_data['email'],
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }, 'При регистрации пользователя тело ответа API отличается от ожидаемого.'


def test_register_invalid_pass(user_client):
    response = user_client.post(REGISTER_URL, json={
        'email': 'dead@pool.com',
        'password': '$',
    })
    assert response.status_code == 400, (
        'Проверьте статус ответа API: '
        'при регистрации пользователя некорректный POST-запрос '
        f'к эндпоинту`{REGISTER_URL}` должен вернуть ответ со статусом 400.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'Убедитесь, что в ответе на некорректный POST-запрос '
        f'к эндпоинту `{REGISTER_URL}` есть ключ `detail`.'
    )
