import requests
from requests import Response

BASE_URL = 'http://127.0.0.1:8000/'


def create_user_api(user_id: int, username: str, user_email: str) -> Response:
    response = requests.post(
        url=f'{BASE_URL}/users',
        json={'id': user_id, 'name': username, 'email': user_email},
    )
    return response


def get_user(user_id: int) -> Response:
    response = requests.get(url=f'{BASE_URL}/users/{user_id}')
    return response


def create_task_api(task_id: int, user_id: int) -> Response:
    response = requests.post(
        url=f'{BASE_URL}/tasks', json={'id': task_id, 'user_id': user_id},
    )
    return response


def get_task(task_id: int) -> Response:
    response = requests.get(url=f'{BASE_URL}/tasks/{task_id}')
    return response
