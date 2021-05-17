from typing import Optional

from poc.helpers.helpers import Helpers
from poc.models.auth import UserModel


class UserService:
    def __init__(self, collection) -> None:
        self.collection = collection

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"email": email})
        if user:
            return Helpers.load_model(UserModel, user)

    async def get_by_token(self, token: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"token": token})
        if user:
            return Helpers.load_model(UserModel, user)

    async def add(self, user: UserModel):
        await self.collection.insert_one(user.dict())
