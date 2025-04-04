import asyncio

import pytest

from api_client import create_task_api, get_task
from app import tasks_db, Task
from utils import generate_random_integer


def test_create_task(created_user_id: int) -> None:
    task_id = generate_random_integer()
    user_id = created_user_id

    created_task_status_code = create_task_api(task_id, user_id).status_code
    created_task = get_task(task_id).json()
    tasks_db.pop(task_id)

    assert (
        created_task_status_code == 201
    ), f'Некорректный статус код: ОР 201, ФР {created_task_status_code}'
    assert (
        created_task['id'] == task_id
    ), f'Некорректный id: ОР {task_id}, ФР {created_task["id"]}'
    assert (
        created_task['user_id'] == user_id
    ), f'Некорректный name: ОР {user_id}, ФР {created_task["user_id"]}'
    Task.model_validate_json(created_task)  # проверка, что схема валидна


@pytest.mark.asyncio
async def test_task_processing(created_user_id: int, created_task_id: int) -> None:
    task_id = created_task_id
    user_id = created_user_id
    create_task_api(task_id, user_id)
    timeout = 10

    while timeout > 0:
        current_status = await get_task(task_id).json()['status']

        if current_status != 'pending':
            break

        await asyncio.sleep(1)
        timeout -= 1
    else:
        pytest.fail(f'Таска с id {task_id} неожиданно зависла в статусе pending!')

    assert get_task(task_id).json()['status'] == 'done'


@pytest.mark.parametrize(
    'task_id, user_id, expected_code',
    [
        (5, 323232, 400),
        (1, 1, 400),  # проверка на дубль таски
        (-1, 1, 400),  # проверка на присваивание отрицательного id
        (1, -1, 400),
        (1, None, 400),
        (None, 1, 400),
    ],
)
def test_create_task_validations(
    created_task_id: int, task_id: int, user_id: int, expected_code: int
) -> None:
    _ = created_task_id
    response = create_task_api(task_id, user_id)
    assert (
        response.status_code == expected_code
    ), f'Некорректный статус код: ОР- 400, ФР: {response.status_code}'
