import hashlib
import uuid

from pydantic import BaseModel
from typing import Type, TypeVar

from poc.models.auth import UserModel

Model = TypeVar("Model", bound=BaseModel)


class Helpers:

    @staticmethod
    #  https://gist.github.com/henriklindgren/f0f05034ac4b36eafdb7c877e5088f33
    def load_model(t: Type[Model], o: dict) -> Model:
        populated_keys = o.keys()
        required_keys = set(t.schema()["required"])
        missing_keys = required_keys.difference(populated_keys)
        if missing_keys:
            raise ValueError(f"Required keys missing: {missing_keys}")
        all_definition_keys = t.schema()["properties"].keys()
        return t(**{k: v for k, v in o.items() if k in all_definition_keys})

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return f"{hashlib.sha256(salt.encode() + password.encode()).hexdigest()}:{salt}"

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(":")
        return (
            password
            == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        )