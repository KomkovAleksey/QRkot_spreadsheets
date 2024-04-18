import time
from datetime import datetime

import pytest

PROJECTS_URL = '/charity_project/'
PROJECT_DETAILS_URL = PROJECTS_URL + '{project_id}'


@pytest.mark.parametrize(
    'invalid_name',
    [
        '',
        'lovechimichangasbutnunchakuisbetternunchakis4life' * 3,
        None,
    ],
    ids=['empty', 'too_long', 'None'],
)
def test_create_invalid_project_name(superuser_client, invalid_name):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': invalid_name,
            'description': 'Project_1',
            'full_amount': 5000,
        },
    )
    assert response.status_code == 422, (
        'Создание проектов с пустым названием или с названием длиннее 100 '
        'символов должно быть запрещено.'
    )


@pytest.mark.parametrize(
    'desc', [
        '',
        None,
    ]
)
def test_create_project_no_desc(superuser_client, desc):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'Мертвый Бассейн',
            'description': desc,
            'full_amount': 5000,
        },
    )
    assert (
        response.status_code == 422
    ), 'Создание проектов с пустым описанием должно быть запрещено.'


@pytest.mark.parametrize('json_data', [
    {'invested_amount': 100},
    {'fully_invested': True},
    {'id': 5000},
])
def test_create_project_with_autofilling_fields(superuser_client, json_data):
    response = superuser_client.post(
        PROJECTS_URL,
        json=json_data
    )
    assert response.status_code == 422, (
        'При попытке передать в запросе значения для автозаполняемых полей '
        'должна возвращаться ошибка 422.'
    )


@pytest.mark.parametrize(
    'invalid_full_amount',
    [
        -100,
        0.5,
        'test',
        0.0,
        '',
        None,
    ],
)
def test_create_invalid_full_amount_value(superuser_client,
                                          invalid_full_amount):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'Project_1',
            'description': 'Project_1',
            'full_amount': invalid_full_amount,
        },
    )
    assert response.status_code == 422, (
        'Убедитесь, что поле `full_amount` (требуемая сумма проекта) '
        'принимает только целочисленные положительные значения.'
    )


@pytest.mark.usefixtures('charity_project')
def test_get_charity_project(user_client):
    response = user_client.get(PROJECTS_URL)
    assert response.status_code == 200, (
        f'При GET-запросе к эндпоинту `{PROJECTS_URL}` должен возвращаться '
        'статус-код 200.'
    )
    response_data = response.json()
    assert isinstance(response_data, list), (
        f'При GET-запросе к эндпоинту `{PROJECTS_URL}` должен возвращаться '
        'объект типа `list`.'
    )
    assert len(response_data) == 1, (
        'Убедитесь, что при корректном POST-запросе '
        f'к эндпоинту `{PROJECTS_URL}` создаётся объект в БД. '
        'Проверьте модель `CharityProject`.'
    )
    first_elem = response_data[0]
    expected_keys = {
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
    }
    missing_keys = expected_keys - first_elem.keys()
    assert not missing_keys, (
        f'В ответе на GET-запрос к эндпоинту `{PROJECTS_URL}` не хватает '
        f'следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    response_data[0].pop('close_date', None)
    assert response_data == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life',
        }
    ], (
        f'При GET-запросе к эндпоинту `{PROJECTS_URL}` тело ответа API '
        'отличается от ожидаемого.'
    )


@pytest.mark.usefixtures('charity_project', 'charity_project_nunchaku')
def test_get_all_charity_project(user_client):
    response = user_client.get(PROJECTS_URL)
    assert response.status_code == 200, (
        'При запросе перечня проектов должен возвращаться статус-код 200.'
    )
    response_data = response.json()
    assert isinstance(response_data, list), (
        'При запросе перечня проектов должен возвращаться объект типа `list`.'
    )
    assert len(response_data) == 2, (
        'Убедитесь, что при корректном POST-запросе '
        f'к эндпоинту `{PROJECTS_URL}` '
        'создаётся объект в БД. Проверьте модель `CharityProject`.'
    )
    first_elem = response_data[0]
    expected_keys = {
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
    }
    missing_keys = expected_keys - first_elem.keys()
    assert not missing_keys, (
        f'В ответе на GET-запрос к эндпоинту `{PROJECTS_URL}` не хватает '
        f'следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    [project.pop('close_date', None) for project in response_data]
    assert response_data == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life',
        },
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku',
        },
    ], (
        f'При GET-запросе к эндпоинту `{PROJECTS_URL}` тело ответа API отличается '
        'от ожидаемого.'
    )


def test_create_charity_project(superuser_client):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 1000000,
        },
    )
    assert (
        response.status_code == 200
    ), 'При создании проекта должен возвращаться статус-код 200.'
    data = response.json()
    expected_keys = {
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        'В ответе на корректный POST-запрос суперпользователя к эндпоинту '
        f'`{PROJECTS_URL}` на создание проекта не хватает следующих ключей: '
        f'`{"`, `".join(missing_keys)}`'
    )
    data.pop('create_date')
    data.pop('close_date', None)
    assert data == {
        'description': 'Deadpool inside',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
        'name': 'Мертвый Бассейн',
    }, (
        f'При POST-запросе суперпользователя к эндпоинту `{PROJECTS_URL}` '
        'тело ответа API отличается от ожидаемого. Проверьте структуру ответа '
        'и убедитесь, что пустые поля не выводятся в ответе.'
    )


@pytest.mark.parametrize(
    'json_data',
    [
        {
            'name': 'Мертвый Бассейн',
            'full_amount': '1000000',
        },
        {
            'description': 'Deadpool inside',
            'full_amount': '1000000',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 'Donat',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': '',
        },
        {},
    ],
)
def test_create_charity_project_validation_error(json_data, superuser_client):
    response = superuser_client.post(PROJECTS_URL, json=json_data)
    assert response.status_code == 422, (
        'Некорректный POST-запрос супервользователя к эндпоинту '
        f'`{PROJECTS_URL}` должен вернуть статус-код 422.'
    )
    data = response.json()
    assert 'detail' in data, (
        'В ответе на некорректный POST-запрос суперпользователя к эндпоинту '
        f'`{PROJECTS_URL}` должно содержаться поле `detail`.'
    )


def test_delete_project_usual_user(user_client, charity_project):
    response = user_client.delete(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id))
    assert response.status_code == 403, (
        f'DELETE-запрос к эндпоинту `{PROJECT_DETAILS_URL}` от пользователя, '
        'не являющегося суперюзером, должен вернуть ответ со '
        'статус-кодом 403.'
    )


def test_delete_charity_project(superuser_client, charity_project):
    response = superuser_client.delete(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id))
    assert response.status_code == 200, (
        'DELETE-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` должен вернуть ответ со статус-кодом 200.'
    )
    data = response.json()
    expected_keys = {
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        'В ответе на DELETE-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` не хватает следующих ключей: '
        f'`{"`, `".join(missing_keys)}`'
    )


def test_delete_charity_project_invalid_id(superuser_client):
    response = superuser_client.delete(
        PROJECT_DETAILS_URL.format(project_id='999a4'))
    assert response.status_code == 422, (
        'Если в DELETE-запросе суперпользователя '
        f'к эндпоинту `{PROJECT_DETAILS_URL}` '
        'передан некорректный id проекта - должен вернуться статус-код 422.'
    )
    data = response.json()
    assert 'detail' in data, (
        'Ответ на некорректный DELETE-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` должен содержать поле `detail`'
    )


@pytest.mark.parametrize(
    'json_data, expected_data',
    [
        (
            {'full_amount': 10},
            {
                'name': 'chimichangas4life',
                'description': 'Huge fan of chimichangas. Wanna buy a lot',
                'full_amount': 10,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
        (
            {'name': 'chimi'},
            {
                'name': 'chimi',
                'description': 'Huge fan of chimichangas. Wanna buy a lot',
                'full_amount': 1000000,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
        (
            {'description': 'Give me the money!'},
            {
                'name': 'chimichangas4life',
                'description': 'Give me the money!',
                'full_amount': 1000000,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
    ],
)
def test_update_charity_project(superuser_client, charity_project, json_data,
                                expected_data):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id),
        json=json_data
    )
    assert response.status_code == 200, (
        'Корректный PATCH-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` должен вернуть статус-код 200.'
    )
    response_data = response.json()
    expected_keys = {
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
    }
    missing_keys = expected_keys - response_data.keys()
    assert not missing_keys, (
        f'В ответе на GET-запрос к эндпоинту `{PROJECT_DETAILS_URL}` не '
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    response_data.pop('close_date', None)
    assert response_data == expected_data, (
        'Тело ответа на PATCH-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` отличается от ожидаемого. Проверьте '
        'структуру ответа и убедитесь, что пустые поля не выводятся в ответе.'
    )


@pytest.mark.parametrize('json_data', [
    {'full_amount': 100},
    {'full_amount': 1000},
])
def test_update_charity_project_full_amount_equal_invested_amount(
        superuser_client, charity_project_little_invested, json_data
):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(
            project_id=charity_project_little_invested.id),
        json=json_data,
    )
    assert response.status_code == 200, (
        'Убедитесь, что при редактировании проекта разрешено устанавливать '
        'требуемую сумму больше или равную внесённой. Соответствующий '
        f'PATCH-запрос суперпользователя к эндпоинту `{PROJECT_DETAILS_URL}` '
        'должен вернуть ответ со статус-кодом 200.'
    )
    assert response.json()['full_amount'] == json_data['full_amount'], (
        'При редактировании проекта должно быть разрешено устанавливать '
        'требуемую сумму больше или равную внесённой. '
        'Убедитесь, что корректный PATCH-запрос суперпользователя '
        f'к эндпоинту `{PROJECT_DETAILS_URL}` изменяет '
        'значение поля `full_amount`.'
    )


@pytest.mark.parametrize(
    'json_data',
    [
        {'description': ''},
        {'name': ''},
        {'full_amount': ''},
    ],
)
def test_update_charity_project_invalid(superuser_client, charity_project,
                                        json_data):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id),
        json=json_data
    )
    assert response.status_code == 422, (
        'Убедитесь, что при редактировании проекта запрещено '
        'назначать пустое имя, описание или цель фонда. '
        'Подобный PATCH-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` должен вернуть статус-код 422.'
    )


@pytest.mark.parametrize(
    'json_data',
    [
        {'invested_amount': 100},
        {'create_date': '2010-10-10'},
        {'close_date': '2010-10-10'},
        {'fully_invested': True},
    ],
)
def test_update_charity_with_unexpected_fields(superuser_client,
                                               charity_project, json_data):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id),
        json=json_data
    )
    assert response.status_code == 422, (
        'Убедитесь, что при редактировании проекта невозможно изменить '
        'значения полей, редактирование которых не предусмотрено '
        'спецификацией к API. '
        'Если в PATCH-запросе суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` этим полям присвоены новые значения -'
        'должен вернуться ответ со статус-кодом 422.'
    )


@pytest.mark.usefixtures('charity_project_nunchaku')
def test_update_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id),
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 400, (
        'Если PATCH-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` присваивает проекту название '
        'другого существующего проекта - '
        'должен вернуться ответ со статус-кодом 400.'
    )
    assert 'detail' in response.json(), (
        'Если PATCH-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` присваивает проекту название '
        'другого существующего проекта - '
        'в ответе должен быть ключ `detail` с описанием ошибки.'
    )


@pytest.mark.parametrize('full_amount', [0, 5])
def test_update_charity_project_full_amount_smaller_already_invested(
        superuser_client, charity_project_little_invested, full_amount
):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(
            project_id=charity_project_little_invested.id),
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': full_amount,
        },
    )
    assert response.status_code in (400, 422), (
        'Убедитесь, что при редактировании проекта запрещено устанавливать '
        'требуемую сумму меньше внесённой.'
    )


def test_create_charity_project_usual_user(user_client):
    response = user_client.post(
        PROJECTS_URL,
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 403, (
        'POST-запрос пользователя, не являющегося суперюзером, к эндпоинту '
        f'`{PROJECTS_URL}` должен вернуть статус-код 403.'
    )
    data = response.json()
    assert 'detail' in data, (
        'Ответ на POST-запрос пользователя, не являющегося суперюзером, к '
        f'эндпоинту `{PROJECTS_URL}` должен содержать ключ `detail`.'
    )


def test_patch_charity_project_usual_user(user_client, charity_project):
    response = user_client.patch(
        PROJECT_DETAILS_URL.format(project_id=charity_project.id),
        json={'full_amount': 10}
    )
    assert response.status_code == 403, (
        'PATCH-запрос пользователя, не являющегося суперюзером, к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` должен вернуть статус-код 403.'
    )
    data = response.json()
    assert 'detail' in data, (
        'Ответ на PATCH-запрос пользователя, не являющегося суперюзером, к '
        f'эндпоинту `{PROJECT_DETAILS_URL}` должен содержать ключ `detail`.'
    )


def test_patch_charity_project_fully_invested(
        superuser_client, small_fully_charity_project,
):
    response = superuser_client.patch(
        PROJECT_DETAILS_URL.format(project_id=small_fully_charity_project.id),
        json={'full_amount': 10}
    )
    common_message_part = (
        'При попытке суперпользователя обновить проект, который был '
        'полностью проинвестирован, с помощью PATCH-запроса к эндпоинту '
        f'`{PROJECT_DETAILS_URL}`'
    )
    assert response.status_code == 400, (
        f'{common_message_part} должен вернуться статус-код 400.'
    )
    data = response.json()
    assert 'detail' in data, (
        f'{common_message_part} ответ должен содержать ключ `detail` с описанием '
        'ошибки.'
    )


def test_create_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': charity_project.name,
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    common_messege_part = (
        f'POST-запрос суперпользователя к эндпоинту `{PROJECTS_URL}`, '
        'содержащий неуникальное значение для поля `name`,'
    )
    assert response.status_code == 400, (
        f'{common_messege_part} должен вернуть статус-код 400.'
    )
    data = response.json()
    assert 'detail' in data, (
        f'В ответе на {common_messege_part} должен быть ключ `detail` с '
        'описанием ошибки.'
    )


def test_create_charity_project_diff_time(superuser_client):
    response_chimichangs = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    time.sleep(0.01)
    response_nunchaku = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'nunchaku',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
        },
    )
    chimichangas_create_date = response_chimichangs.json()['create_date']
    nunchakus_create_date = response_nunchaku.json()['create_date']
    assert chimichangas_create_date != nunchakus_create_date, (
        'Убедитесь, что при создании двух проектов подряд '
        'время создания этих проектов (значение поля `create_date`) отличается. '
        'Проверьте значение по умолчанию у атрибута `create_date`.'
    )


def test_donation_exist_project_create(superuser_client, donation):
    response = superuser_client.post(
        PROJECTS_URL,
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 100,
        },
    )
    data = response.json()
    assert data['fully_invested'], (
        'Если при редактировании проекта новая требуемая сумма '
        'равна уже внесённой - проект должен быть '
        'закрыт: значением поля `fully_invested` должно стать `True`.'
    )
    assert (
        data['close_date'] == datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    ), (
        'Если при редактировании проекта новая требуемая сумма '
        'равна уже внесённой - проект должен быть '
        'закрыт: для поля `close_date` должно быть установлено занчение, '
        'равное текущему времени.'
    )


def test_delete_charity_project_already_invested(
        superuser_client, charity_project_little_invested):
    response = superuser_client.delete(
        PROJECT_DETAILS_URL.format(
            project_id=charity_project_little_invested.id)
    )
    assert response.status_code == 400, (
        'Убедитесь, что запрещено удаление проектов, в которые уже '
        'внесены средства. DELETE-запрос суперпользователя к эндпоинту '
        f'`{PROJECT_DETAILS_URL}` на удаление такого проекта '
        'должен вернуть ответ со статус-кодом 400.'
    )
    assert 'detail' in response.json(), (
        'Убедитесь, что запрещено удаление проектов, в которые уже '
        'внесены средства. В ответе на DELETE-запрос суперпользователя к '
        f'эндпоинту `{PROJECT_DETAILS_URL}` на удаление такого проекта '
        'должен быть ключ `detail` с описанием ошибки.'
    )


def test_delete_charity_project_already_closed(superuser_client,
                                               closed_charity_project):
    response = superuser_client.delete(
        PROJECT_DETAILS_URL.format(project_id=closed_charity_project.id)
    )
    assert response.status_code == 400, (
        'Убедитесь, что удаление закрытых проектов запрещено. DELETE-запрос '
        f'суперпользователя к эндпоинту `{PROJECT_DETAILS_URL}` на удаление '
        'закрытого проекта должен вернуть ответ со статус-кодом 400.'
    )
    assert 'detail' in response.json(), (
        'Убедитесь, что удаление закрытых проектов запрещено. Ответ на '
        f'DELETE-запрос суперпользователя к эндпоинту `{PROJECT_DETAILS_URL}` '
        'должен содержать ключ `detail` с описанием ошибки.'
    )


@pytest.mark.usefixtures('charity_project', 'charity_project_nunchaku')
def test_get_all_charity_project_not_auth_user(test_client):
    response = test_client.get(PROJECTS_URL)
    assert response.status_code == 200, (
        'GET-запрос незарегистрированного пользователя к эндпоинту '
        f'`{PROJECTS_URL}` должен вернуть ответ со статус-кодом 200.'
    )
    data = response.json()
    [project.pop('close_date', None) for project in data]
    assert data == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life'
        },
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku'
        }
    ], (
        'Убедитесь, что в ответ на GET-запрос незарегистрированного '
        f'пользователя к эндпоинту `{PROJECTS_URL}` возвращается список '
        'существующих проектов.'
    )
