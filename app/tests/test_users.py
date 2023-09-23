from http import HTTPStatus
import requests
from app.tests.test_functions import (
    create_user_payload,
    create_one_answer,
    create_multiple_choice,
    ENDPOINT,
)


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["phone"] == payload["phone"]
    assert user_data["email"] == payload["email"]

    get_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["phone"] == payload["phone"]
    assert get_response.json()["email"] == payload["email"]

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["phone"] == payload["phone"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_data():
    payload = create_user_payload()
    payload["phone"] = "12345"  # wrong phone
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST

    payload = create_user_payload()
    payload["email"] = "testtest"  # wrong email
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_history():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/history")
    user_history = get_response.json()["history"]
    assert isinstance(user_history, list)

    payload = create_one_answer()
    create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    question_data = create_response.json()
    question_id = question_data["id"]

    user_answer = question_data["answer"]
    payload_solve = {
        "user_id": user_id,
        "user_answer": user_answer,
    }
    solve_response = requests.post(
        f"{ENDPOINT}/questions/{question_id}/solve", json=payload_solve
    )
    assert solve_response.status_code == HTTPStatus.OK

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/history")
    assert len(get_response.json()["history"]) == len(user_history) + 1

    question_data = get_response.json()["history"][-1]
    assert question_data["title"] == payload["title"]
    assert question_data["description"] == payload["description"]
    assert question_data["type"] == payload["type"]
    assert question_data["user_answer"] == user_answer
    assert question_data["reward"] == solve_response.json()["reward"]

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK

    delete_response = requests.delete(f"{ENDPOINT}/questions/{question_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard():
    n = 3
    test_users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])

    payload = {"type": "table"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    leaderboard = get_response.json()["leaderboard"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
