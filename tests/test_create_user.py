import pytest

from api_client import create_user_api, get_user
from app import users_db, User
from utils import generate_random_string, generate_random_integer


def test_create_user() -> None:
    user_id = generate_random_integer()
    username = generate_random_string('name')
    user_email = generate_random_string('user_email') + '@test.ru'

    created_user_status_code = create_user_api(
        user_id, username, user_email
    ).status_code
    created_user = get_user(user_id).json()
    users_db.pop(user_id)
    assert (
        created_user_status_code == 201
    ), f'Некорректный статус код: ОР- 201, ФР: {created_user_status_code}'
    assert (
        created_user['id'] == user_id
    ), f'Некорректный id: ОР {user_id}, ФР: {created_user["id"]}'
    assert (
        created_user['name'] == username
    ), f'Некорректный name: ОР {username}, ФР: {created_user["name"]}'
    assert (
        created_user['email'] == user_email
    ), f'Некорректный email: ОР {user_email}, ФР: {created_user["email"]}'
    User.model_validate_json(created_user)  # проверка, что схема валидна


@pytest.mark.parametrize(
    'user_id, name, email, expected_code',
    [
        (1, 'test', 'test@mail.ru', 400),  # проверка на дубль
        (-1, 'test', 'test@mail.ru', 400),  # проверка на присваивание отрицательного id
        (
            None,
            'test',
            'test@mail.ru',
            400,
        ),  # далее проверки на отсутствие обязательных полей
        (4, 'test', 400),
        (3, 'test', 'test', 400),  # проверка на маску емейла
        (16, 'ОЧЕНЬ ДЛИННОЕ ИМЯ ОЧЕНЬ ДЛИННОЕ ИМЯ ', 'test@mail.ru', 400),
    ],
)
def test_create_user_validations(
    created_user_id: int, user_id: int, name: str, email: str, expected_code: int
) -> None:
    _ = created_user_id
    response = create_user_api(user_id, name, email)
    assert (
        response.status_code == expected_code
    ), f'Некорректный статус код: ОР- 400, ФР: {response.status_code}'
