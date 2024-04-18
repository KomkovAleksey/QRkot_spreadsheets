import pytest

DONATION_URL = '/donation/'
PROJECTS_URL = '/charity_project/'


@pytest.mark.usefixtures('donation')
def test_donation_exist_non_project(superuser_client):
    response_donation = superuser_client.get(DONATION_URL)
    data_donation = response_donation.json()
    assert len(data_donation) == 1, (
        'Убедитесь, что в ответ на GET-запрос суперпользователя к эндпоинту '
        f'`{DONATION_URL}` возврашается список существующих пожертвований.'
    )
    assert data_donation[0]['invested_amount'] == 0, (
        'Если получено пожертвование, но открытых проектов нет, '
        'сумма в поле `invested_amount` должна оставаться нулевой.'
    )


@pytest.mark.usefixtures('charity_project')
def test_project_exist_non_donations(superuser_client):
    response = superuser_client.get(PROJECTS_URL)
    data = response.json()
    assert data[0]['invested_amount'] == 0, (
        'Если проект существует, но пожертвований пока нет, '
        'сумма в поле `invested_amount` должна оставаться нулевой.'
    )


def test_fully_invested_amount_for_two_projects(user_client, charity_project,
                                                charity_project_nunchaku):
    common_asser_msg = (
        'При тестировании создано два пустых проекта. '
        'Затем тест создал два пожертвования, которые '
        'полностью и без остатка покрывают требуемую сумму первого проекта. '
        'Второй проект должен оставаться не инвестированным.'
    )
    [user_client.post(
        DONATION_URL, json={'full_amount': 500000}) for _ in range(2)]
    assert charity_project.fully_invested, common_asser_msg
    assert not charity_project_nunchaku.fully_invested, common_asser_msg
    assert charity_project_nunchaku.invested_amount == 0, common_asser_msg


def test_donation_to_little_invest_project(
        user_client, charity_project_little_invested, charity_project_nunchaku
):
    common_asser_msg = (
        'При тестировании создано два проекта, '
        'один из которых частично инвестирован, а второй - без инвестиций. '
        'Затем тест создает пожертвование, недостаточное для закрытия '
        'первого проекта. Пожертвование должно добавиться '
        'в первый проект; второй проект должен остаться пустым.'
    )
    user_client.post(DONATION_URL, json={'full_amount': 900})
    assert not charity_project_little_invested.fully_invested, common_asser_msg
    assert charity_project_little_invested.invested_amount == 1000, (
        common_asser_msg
    )
    assert not charity_project_nunchaku.fully_invested, common_asser_msg
    assert charity_project_nunchaku.invested_amount == 0, common_asser_msg
