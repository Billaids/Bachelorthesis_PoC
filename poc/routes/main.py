from loguru import logger
from fastapi import APIRouter

from ..models.common import APIResponse

router = APIRouter()


@logger.catch
@router.get("/")
async def main_page():
    """Main page. Just for example."""

    return APIResponse(status=200, message="ok")
