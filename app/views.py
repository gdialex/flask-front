from app import app, USERS, EXPRS, QUEST, models
from flask import request, Response
import json
from http import HTTPStatus
import random


@app.route("/")
def index():
    return "<h1>Hello world</h1>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, phone, email)

    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/user/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/expression")
def generate_expr():
    data = request.get_json()
    expr_id = len(EXPRS)
    count_nums = data["count_nums"]
    operation = data["operation"]  # expect +,*,-,//,**,
    if operation == "random":
        operation = random.choice(["+", "*", "-", "//", "**"])
    min_num = data["min"]
    max_num = data["max"]

    if count_nums <= 1 or (count_nums > 2 and operation not in {"+", "*"}):
        return Response(status=HTTPStatus.BAD_REQUEST)

    values = [random.randint(min_num, max_num) for _ in range(count_nums)]
    expression = models.Expression(expr_id, operation, *values)
    EXPRS.append(expression)

    response = Response(
        json.dumps(
            {
                "id": expression.id,
                "operation": expression.operation,
                "values": expression.values,
                "string_expression": expression.to_string(),
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/<int:expr_id>")
def get_expr(expr_id):
    if not models.Expression.is_valid_id(expr_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    expression = EXPRS[expr_id]

    response = Response(
        json.dumps(
            {
                "id": expression.id,
                "operation": expression.operation,
                "values": expression.values,
                "string_expression": expression.to_string(),
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/math/<int:expr_id>/solve")
def solve_expr(expr_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    if not models.Expression.is_valid_id(expr_id):
        return Response(status=HTTPStatus.NOT_FOUND)

    expression = EXPRS[expr_id]
    user = USERS[user_id]

    if user_answer == expression.answer:
        user.increase_score(expression.reward)
        result = "correct"
    else:
        result = "wrong"

    return Response(
        json.dumps(
            {
                "expression_id": expr_id,
                "result": result,
                "reward": expression.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/questions/create")
def create_question():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = len(QUEST)
    question = None
    if question_type == "ONE-ANSWER":
        answer = data["answer"]  # expect string
        if not models.OneAnswer.is_valid(answer):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.OneAnswer(question_id, title, description, answer, reward=1)
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # list of choices
        answer = data["answer"]  # expect number
        if not models.MultipleChoice.is_valid(answer, choices):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.MultipleChoice(
            question_id, title, description, answer, choices, reward=1
        )

    QUEST.append(question)
    return Response(
        json.dumps(
            {
                "id": question.id,
                "title": question.title,
                "description": question.description,
                "type": question_type,
                "answer": question.answer,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
