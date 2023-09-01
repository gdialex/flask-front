# models.py
import re


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_valid_phone(phone):
        if re.match(r"^\+?[1-9][0-9]{7,14}$", phone):
            return True
        return False


class Expression:
    def __init__(self, id, operation, *values):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()

    def __evaluate(self):
        return eval(self.to_string())

    def to_string(self):
        expr_str = str(self.values[0]) + "".join(
            f" {self.operation} {value}" for value in self.values[1:]
        )
        return expr_str
