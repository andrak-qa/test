from typing import Generator

import pytest

from api_client import create_user_api, create_task_api
from app import users_db

from utils import generate_random_string, generate_random_integer


@pytest.fixture
def created_user_id() -> Generator[int]:
    user_id = (
        generate_random_integer()
    )  # хотя конечно тут стоит задуматься, нужно ли при создании указывать свой ид
    username = generate_random_string('name')
    user_email = generate_random_string('user_email') + '@test.ru'
    created_user_id = create_user_api(user_id, username, user_email).json()['id']
    yield created_user_id
    users_db.pop(created_user_id)


@pytest.fixture
def created_task_id(created_user_id) -> Generator[int]:
    task_id = generate_random_integer()
    user_id = created_user_id
    created_task_id = create_task_api(task_id, user_id).json()['id']
    yield created_task_id
    users_db.pop(created_task_id)
