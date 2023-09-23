from uuid import uuid4
import random

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pupkin" + str(uuid4()),
        "phone": "+79999999999",
        "email": "test@test.ru",
    }


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


def generate_expression_payload():
    n = random.choice([2, 5, 10])
    if n == 2:
        oper = random.choice(["+", "*", "-", "//", "**"])
    else:
        oper = random.choice(["+", "*"])
    return {
        "count_nums": 2,
        "operation": oper,
        "min": random.randint(1, 10),
        "max": random.randint(11, 20),
    }
