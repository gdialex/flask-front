from http import HTTPStatus
import requests
from uuid import uuid4
from app.tests.test_functions import (
    create_user_payload,
    create_one_answer,
    create_multiple_choice,
    ENDPOINT,
)


def create_one_answer():
    return {
        "title": "Test One-Answer Question",
        "description": "simple test question, nothing fancy",
        "type": "ONE-ANSWER",
        "answer": "Never Gonna Give You Up",
    }


def create_multiple_choice():
    return {
        "title": "Test Multiple Choice Question",
        "description": "simple MC question",
        "type": "MULTIPLE-CHOICE",
        "choices": ["Hello", "World", "Goodbye"],
        "answer": 1,
    }


def test_question_create_one_answer():
    payload = create_one_answer()
    create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    question_data = create_response.json()
    question_id = question_data["id"]

    assert question_data["title"] == payload["title"]
    assert question_data["description"] == payload["description"]
    assert question_data["type"] == payload["type"]
    assert question_data["answer"] == payload["answer"]

    payload_for_get = {"mode": "no answer"}
    get_response = requests.get(
        f"{ENDPOINT}/questions/{question_id}", json=payload_for_get
    )
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["title"] == payload["title"]
    assert get_response.json()["description"] == payload["description"]
    assert get_response.json()["type"] == payload["type"]
    assert get_response.json()["answer"] == "hidden"

    delete_response = requests.delete(f"{ENDPOINT}/questions/{question_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["title"] == payload["title"]
    assert delete_response.json()["description"] == payload["description"]
    assert delete_response.json()["type"] == payload["type"]
    assert delete_response.json()["answer"] == payload["answer"]


def test_question_create_multiple_choice():
    payload = create_multiple_choice()
    create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    question_data = create_response.json()
    question_id = question_data["id"]

    assert question_data["title"] == payload["title"]
    assert question_data["description"] == payload["description"]
    assert question_data["type"] == payload["type"]
    assert question_data["choices"] == payload["choices"]
    assert question_data["answer"] == payload["answer"]

    payload_for_get = {"mode": "no answer"}
    get_response = requests.get(
        f"{ENDPOINT}/questions/{question_id}", json=payload_for_get
    )
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["title"] == payload["title"]
    assert get_response.json()["description"] == payload["description"]
    assert get_response.json()["type"] == payload["type"]
    assert question_data["choices"] == payload["choices"]
    assert get_response.json()["answer"] == "hidden"

    delete_response = requests.delete(f"{ENDPOINT}/questions/{question_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["title"] == payload["title"]
    assert delete_response.json()["description"] == payload["description"]
    assert delete_response.json()["type"] == payload["type"]
    assert question_data["choices"] == payload["choices"]
    assert delete_response.json()["answer"] == payload["answer"]


def test_get_random_question():
    n = 3
    test_questions = []
    for _ in range(n):
        payload = create_multiple_choice()
        create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
        assert create_response.status_code == HTTPStatus.CREATED
        test_questions.append(create_response.json()["id"])
        payload = create_one_answer()
        create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
        assert create_response.status_code == HTTPStatus.CREATED
        test_questions.append(create_response.json()["id"])

    create_response = requests.get(f"{ENDPOINT}/questions/random")
    assert create_response.status_code == HTTPStatus.OK
    question_data = create_response.json()
    question_id = question_data["id"]
    question_reward = question_data["reward"]

    payload_for_get = {"mode": "no answer"}
    get_response = requests.get(
        f"{ENDPOINT}/questions/{question_id}", json=payload_for_get
    )
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["reward"] == question_reward

    for question_id in test_questions:
        delete_response = requests.delete(f"{ENDPOINT}/questions/{question_id}")
        assert delete_response.status_code == HTTPStatus.OK


def test_solve_question():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]

    payload = create_one_answer()
    create_response = requests.post(f"{ENDPOINT}/questions/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    question_data = create_response.json()
    question_id = question_data["id"]

    # for user_answer in [correct, wrong]
    for user_answer in [question_data["answer"], "test_wrong_answer"]:
        get_user_response = requests.get(f"{ENDPOINT}/user/{user_id}")
        user_score = get_user_response.json()["score"]
        payload = {
            "user_id": user_id,
            "user_answer": user_answer,
        }
        get_response = requests.post(
            f"{ENDPOINT}/questions/{question_id}/solve", json=payload
        )
        assert get_response.status_code == HTTPStatus.OK
        data = get_response.json()
        reward = data["reward"]
        result = "wrong" if user_answer == "test_wrong_answer" else "correct"
        assert data["result"] == result

        get_user_response = requests.get(f"{ENDPOINT}/user/{user_id}")
        if user_answer == "test_wrong_answer":
            reward = 0
        assert get_user_response.json()["score"] == user_score + reward

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK

    delete_response = requests.delete(f"{ENDPOINT}/questions/{question_id}")
    assert delete_response.status_code == HTTPStatus.OK
