from app import app, USERS, EXPRS, models
from flask import request, Response
import json
from http import HTTPStatus
import random


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
        reward = expression.reward
    else:
        result = "wrong"
        reward = 0

    user.solve(expression, user_answer)

    return Response(
        json.dumps(
            {
                "expression_id": expr_id,
                "result": result,
                "reward": reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
