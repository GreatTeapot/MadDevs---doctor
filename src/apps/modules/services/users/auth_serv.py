import datetime as dt

from jwt import ExpiredSignatureError, DecodeError, MissingRequiredClaimError

from core.security import Security
from modules.const.users import const as resp_exc
from modules.exceptions.users import exception as error
from modules.services.users.user_serv import UserService
from modules.unit_of_works.users.auth_uow import AuthUOW


class AuthService(UserService):
    """Service for handling authentication"""

    @staticmethod
    def __verify_password_and_check_deletion(
            password: str,
            hash_password: bytes,
            is_user_deleted: bool,
    ):
        """Verify the provided password matches the stored one and check if the user is deleted."""
        if not Security.verify_password(password, hashed_password=hash_password):
            raise error.AuthBadRequestException(detail=resp_exc.CREDENTIALS_BAD_REQUEST)
        if is_user_deleted:
            raise error.AuthBadRequestException(detail=resp_exc.USER_REMOVED_REQUEST)

    @classmethod
    async def user_authenticate(cls,
                                uow: AuthUOW,
                                credentials: str,
                                password: str):
        """Authenticate a user with their email or username and password."""
        async with uow:
            user = await uow.repo.get_by_email_or_username(credentials)
            if not user:
                raise error.UserNotFoundException()
            cls.__verify_password_and_check_deletion(
                password=password,
                hash_password=user.password_hash,
                is_user_deleted=user.deleted,
            )

            return user

    @classmethod
    async def get_user_for_update_tokens(
            uow: AuthUOW, refresh_token: str
    ) -> tuple[str, dt.datetime]:
        """Retrieve user details for token refresh."""
        async with uow:
            try:
                payload = Security.decode_token(refresh_token)
            except ExpiredSignatureError:

                payload = Security.decode_token_not_verify_signature(refresh_token)
                login, expire = payload["sub"], payload["exp"]
                expire_timestamp = dt.datetime.fromtimestamp(expire, dt.timezone.utc)
                await uow.repo.delete_expire_device(login, expire_timestamp)

                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_EXPIRED_FORBIDDEN
                )
            except DecodeError:
                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_INVALID_FORBIDDEN
                )
            except MissingRequiredClaimError:
                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_REQUIRED_FIELD_FORBIDDEN,
                )

            if payload["type"] == "refresh":
                login = payload["sub"]
                user = await uow.repo.get(login)
                if user.deleted:
                    raise error.AuthBadRequestException(detail=resp_exc.USER_REMOVED_REQUEST)
                return login
            else:
                raise error.AuthBadRequestException(detail=resp_exc.TOKEN_BAD_REQUEST)
