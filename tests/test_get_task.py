import pytest

from api_client import get_user
from app import Task


def test_get_user(created_user_id: int) -> None:
    response = get_user(created_user_id)
    assert response.status_code == 200
    assert response.json()['id'] == created_user_id
    Task.model_validate_json(response.json())  # проверка, что схема валидна


@pytest.mark.parametrize(
    'user_id, expected_code',
    [
        (878787878, 404),
        (-1, 400),  # хотя в коде нет валидации на 400 ошибку, я добавил проверки
        ('test', 400),
        (0, 400),
    ],
)
def test_get_user_validations(user_id: int, expected_code: int) -> None:
    response = get_user(user_id)
    assert response.status_code == expected_code
