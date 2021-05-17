import time
import uuid

from loguru import logger
from fastapi import APIRouter

from .. import user_service
from poc.helpers.helpers import Helpers
from ..models.auth import AddUserRequest, LoginUserModel, UserModel
from ..models.common import APIResponse


router = APIRouter(prefix="/auth")

@logger.catch
@router.post("/login")
async def login(request: LoginUserModel) -> APIResponse:

    user = await user_service.get_by_email(request.email)

    if not user:
        return APIResponse(status=404, message="USER_NOT_FOUND")
    else:
        if Helpers.check_password(user.password, request.password):
            return APIResponse(status=200, message=user.token)
        else:
            return APIResponse(status=403, message="INVALID_CREDENTAILS")


@logger.catch
@router.post("/add_user")
async def add_user(request: AddUserRequest) -> APIResponse:

    request_user = await user_service.get_by_token(request.requester_token)

    if not request_user:
        return APIResponse(status=404, message="INVALID_TOKEN")
    else:
        if request_user.level == 1 or (
            request_user.level == 2 and request.user.level > 1
        ):
            return APIResponse(status=403, message="NOT_ENOUGH_PERMISSION")

        if request.user.level < 1 or request.user.level > 2:
            return APIResponse(status=400, message="INVALID_LEVEL")

        password = Helpers.hash_password(request.user.password)

        new_user = UserModel(
            name=request.user.name,
            email=request.user.email,
            password=password,
            level=request.user.level,
            token=uuid.uuid4().hex,
            reg_time=time.time(),
        )

        try:
            await user_service.add(new_user)
        except:
            return APIResponse(status=409, message="EMAIL_OR_USERNAME_EXISTS")

        return APIResponse(status=200, message="SUCCESS")
