from typing import Union

from fastapi import APIRouter
from starlette.responses import Response

from api.dependencies.dependencies import UserServiceDep, UserUOWDep, UserDep
from core.constants import REFRESH
from core.security import Security
from modules.responses.users import user_res as responses
from modules.schemas.users.auth_schemas import TokenInfoSchema
from modules.schemas.users.user_schemas import (
    RegisterSchema, UserResponseSchema
)

user = APIRouter(prefix="/api/v1/user", tags=["User"])



@user.post("/register",
           summary="Register a new user",
           responses=responses.REGISTRATION_RESPONSES)
async def create_user(
    uow: UserUOWDep,
    service: UserServiceDep,
    model: RegisterSchema,
    response: Response,
) -> TokenInfoSchema:
    """Controller for registering a new user"""
    user_data = await service.create(uow, model)
    access_token = Security.create_access_token(user_data)
    refresh_token = Security.create_refresh_token(user_data)
    response.set_cookie(key=REFRESH,
                        value=refresh_token,
                        httponly=True,
                        secure=False)
    return TokenInfoSchema(access_token=access_token,)



@user.get("/profile",
          summary="User profile",
          responses=responses.GET_RESPONSES)
async def get_user_profile(
    uow: UserUOWDep,
    service: UserServiceDep,
    current_user: UserDep,
) -> UserResponseSchema:
    """Controller for retrieving the current user's profile"""
    user_data = await service.get_user(uow, current_user.id)
    return user_data