from http import HTTPStatus
import requests
import random
from app.tests.test_functions import (
    create_user_payload,
    generate_expression_payload,
    ENDPOINT,
)


def test_generate_expression():
    payload = generate_expression_payload()
    create_response = requests.get(f"{ENDPOINT}/math/expression", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    expr_data = create_response.json()
    expr_id = expr_data["id"]
    assert expr_data["operation"] == payload["operation"]
    assert len(expr_data["values"]) == payload["count_nums"]
    for value in expr_data["values"]:
        assert payload["min"] <= value <= payload["max"]

    get_response = requests.get(f"{ENDPOINT}//math/{expr_id}")
    get_data = get_response.json()
    assert get_data["operation"] == payload["operation"]
    assert len(get_data["values"]) == payload["count_nums"]
    assert get_data["values"] == expr_data["values"]

    delete_response = requests.delete(f"{ENDPOINT}/math/{expr_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["operation"] == payload["operation"]
    assert len(delete_response.json()["values"]) == payload["count_nums"]
    assert delete_response.json()["values"] == expr_data["values"]


def test_generate_expression_bad_data():
    payload = generate_expression_payload()
    payload["count_nums"] = 4
    payload["operation"] = random.choice(
        ["-", "**", "//"]
    )  # wrong operation and count_num
    create_response = requests.get(f"{ENDPOINT}/math/expression", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_solve_expr():
    payload = generate_expression_payload()
    create_response = requests.get(f"{ENDPOINT}/math/expression", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    expr_data = create_response.json()
    expr_id = expr_data["id"]
    string_expression = expr_data["string_expression"]

    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]

    user_answer = eval(string_expression)  # correct answer!!!
    user_score = user_data["score"]
    payload = {
        "user_id": user_id,
        "user_answer": user_answer,
    }
    get_response = requests.post(f"{ENDPOINT}/math/{expr_id}/solve", json=payload)
    assert get_response.status_code == HTTPStatus.OK
    data = get_response.json()
    reward = data["reward"]
    assert data["result"] == "correct"

    get_user_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_user_response.json()["score"] == user_score + reward

    user_answer = eval(string_expression) + 1  # wrong answer!!! +1
    user_score = get_user_response.json()["score"]
    payload = {
        "user_id": user_id,
        "user_answer": user_answer,
    }
    get_response = requests.post(f"{ENDPOINT}/math/{expr_id}/solve", json=payload)
    data = get_response.json()
    reward = data["reward"]
    assert data["result"] == "wrong"
    assert reward == 0

    get_user_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_user_response.json()["score"] == user_score

    delete_response = requests.delete(f"{ENDPOINT}/math/{expr_id}")
    assert delete_response.status_code == HTTPStatus.OK

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
