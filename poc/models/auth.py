from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    level: int
    token: str
    password: str
    email: str
    reg_time: float


class LoginUserModel(BaseModel):
    email: str
    password: str


class AddUserModel(BaseModel):
    email: str
    name: str
    level: int
    password: str


class AddUserRequest(BaseModel):
    requester_token: str
    user: AddUserModel
