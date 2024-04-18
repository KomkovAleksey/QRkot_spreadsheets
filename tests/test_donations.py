import time
from datetime import datetime

import pytest

DONATIONS_URL = '/donation/'
DONATON_DETAILS_URL = DONATIONS_URL + '{donation_id}'
MY_DONATIONS_URL = DONATIONS_URL + 'my'


@pytest.mark.parametrize('json_data, expected_keys, expected_data', [
    (
        {'full_amount': 10},
        {'full_amount', 'id', 'create_date'},
        {'full_amount': 10, 'id': 1},
    ),
    (
        {'full_amount': 5, 'comment': 'To you for chimichangas'},
        {'full_amount', 'id', 'create_date', 'comment'},
        {'full_amount': 5, 'id': 1, 'comment': 'To you for chimichangas'},
    ),
])
def test_create_donation(user_client, json_data, expected_keys, expected_data):
    response = user_client.post(DONATIONS_URL, json=json_data)
    assert response.status_code == 200, (
        'Корректный POST-запрос зарегистрированного пользователя к эндпоинту '
        f'`{DONATIONS_URL}` должен возвращать ответ со статус-кодом 200.'
    )
    data = response.json()
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        'В ответе на POST-запрос зарегистрированного пользователя к эндпоинту '
        f'`{DONATIONS_URL}` не хватает следующих ключей: '
        f'`{"`, `".join(missing_keys)}`'
    )
    data.pop('create_date')
    data.pop('comment', None) if not data.get('comment') else None
    assert data == expected_data, (
        'При создании пожертвования тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json_data', [
    {'comment': 'To you for chimichangas'},
    {'full_amount': -1},
    {'full_amount': None},
    {'fully_invested': True},
    {'user_id': 3},
    {'create_date': str(datetime.now())},
    {'invested_amount': 10},
])
def test_create_donation_incorrect(user_client, json_data):
    response = user_client.post(DONATIONS_URL, json=json_data)
    assert response.status_code == 422, (
        f'При некорректном теле POST-запроса к эндпоинту `{DONATIONS_URL}` '
        'должен вернуться статус-код 422.'
    )


@pytest.mark.usefixtures('another_donation')
def test_get_user_donation(user_client, donation):
    response = user_client.get(MY_DONATIONS_URL)
    assert response.status_code == 200, (
        'GET-запрос зарегистрированного пользователя к эндпоинту '
        f'`{MY_DONATIONS_URL}` должен вернуть ответ со статус-кодом 200.'
    )
    response_data = response.json()
    assert isinstance(response_data, list), (
        'В ответ на GET-запрос зарегистрированного пользователя к эндпоинту '
        f'`{MY_DONATIONS_URL}` должен возвращаться список пожертвований '
        'пользователя (объект типа `list`).'
    )
    assert len(response_data) == 1, (
        'В ответе на GET-запрос зарегистрированного пользователя к эндпоинту '
        f'`{MY_DONATIONS_URL}` должны быть только пожертвования пользователя, '
        'сделавшего запрос.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        'При получении списка пожертвований пользователя в ответе должны '
        f'быть ключи `{keys}`.'
    )
    assert response.json() == [{
        'comment': donation.comment,
        'create_date': '2011-11-11T00:00:00',
        'full_amount': donation.full_amount,
        'id': donation.id,
    }], (
        'При получении списка пожертвований пользователя тело ответа API '
        'отличается от ожидаемого.'
    )


def test_get_all_donations(superuser_client, donation, another_donation):
    response = superuser_client.get(DONATIONS_URL)
    assert response.status_code == 200, (
        f'GET-запрос суперпользователя к эндпоинту `{DONATIONS_URL}` должен '
        'вернуть ответ со статус-кодом 200.'
    )
    response_data = response.json()
    assert isinstance(response_data, list), (
        'При получении списка всех пожертвований должен возвращаться объект '
        'типа `list`.'
    )
    assert len(response_data) == 2, (
        'Ответ на GET-запрос суперпользователя к эндпоинту '
        f'`{DONATIONS_URL}` должен содержать данные всех пожертвований.'
    )
    first_elem = response_data[0]
    expected_keys = {
        'full_amount',
        'comment',
        'id',
        'create_date',
        'user_id',
        'invested_amount',
        'fully_invested',
    }
    missing_keys = expected_keys - first_elem.keys()
    assert not missing_keys, (
        'В ответе на GET-запрос суперпользователя к эндпоинту '
        f'`{DONATIONS_URL}` не хватает следующих ключей: '
        f'`{"`, `".join(missing_keys)}`'
    )
    [donation.pop('close_date', None) for donation in response_data]
    assert sorted(response_data, key=lambda x: x['id']) == sorted(
        [
            {
                'comment': donation.comment,
                'create_date': '2011-11-11T00:00:00',
                'full_amount': donation.full_amount,
                'id': donation.id,
                'user_id': donation.user_id,
                'invested_amount': donation.invested_amount,
                'fully_invested': donation.fully_invested,
            },
            {
                'comment': another_donation.comment,
                'create_date': '2012-12-12T00:00:00',
                'full_amount': another_donation.full_amount,
                'id': another_donation.id,
                'user_id': another_donation.user_id,
                'invested_amount': another_donation.invested_amount,
                'fully_invested': another_donation.fully_invested,
            }
        ],
        key=lambda x: x['id']
    ), (
        'При запросе суперпользователя на получение списка '
        'всех пожертвований тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json_data', [
    {'full_amount': -1},
    {'full_amount': 0.5},
    {'full_amount': 0.155555},
    {'full_amount': -1.5},
])
def test_donation_invalid(user_client, json_data):
    response = user_client.post(DONATIONS_URL, json=json_data)
    assert response.status_code == 422, (
        'POST-запрос зарегистрированного пользователя к эндпоинту '
        f'`{DONATIONS_URL}` с некорректным значением поля `full_amount` '
        'должен вернуть ответ со статус-кодом 422. Это поле '
        'должно принимать только целые положительные числа.'
    )


@pytest.mark.parametrize(
    'client, user_role',
    [
        (pytest.lazy_fixture('superuser_client'), 'суперпользователя'),
        (pytest.lazy_fixture('user_client'), 'пользователя'),
        (pytest.lazy_fixture('test_client'), 'анонимного пользователя'),
    ],
    ids=['superuser', 'user', 'anonymous'],
)
def test_donations_cant_be_updated(donation, client, user_role):
    response = client.patch(
        DONATON_DETAILS_URL.format(donation_id=donation.id)
    )
    assert response.status_code == 404, (
        f'PATCH-запрос {user_role} к эндпоинту `{DONATON_DETAILS_URL}` '
        'должен вернуть ответ со статус-кодом 404.'
    )


@pytest.mark.parametrize(
    'client, user_role',
    [
        (pytest.lazy_fixture('superuser_client'), 'суперпользователя'),
        (pytest.lazy_fixture('user_client'), 'пользователя'),
        (pytest.lazy_fixture('test_client'), 'анонимного пользователя'),
    ],
    ids=['superuser', 'user', 'anonymous'],
)
def test_donations_cant_be_deleted(donation, client, user_role):
    response = client.delete(
        DONATON_DETAILS_URL.format(donation_id=donation.id)
    )
    assert response.status_code == 404, (
        f'DELETE-запрос {user_role} к эндпоинту `{DONATON_DETAILS_URL}` '
        'должен вернуть ответ со статус-кодом 404.'
    )


def test_create_donation_check_create_date(user_client):
    response_1 = user_client.post(DONATIONS_URL, json={'full_amount': 10})
    time.sleep(0.01)
    response_2 = user_client.post(DONATIONS_URL, json={'full_amount': 20})
    assert (
        response_1.json()['create_date'] != response_2.json()['create_date']
    ), (
        'Убедитесь, что при неодновременном создании двух пожертвований '
        'у них отличаются значения в поле `create_date`.'
    )
