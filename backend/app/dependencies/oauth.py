from fastapi import Depends, status, HTTPException

from app.crud.user import current_active_verified_user
from app.models import UserModel


def is_oauth_linked(
        provider_name: str,
):
    def _(
            user: UserModel = Depends(current_active_verified_user),
    ):

        for oauth in user.oauth_accounts:
            if oauth.oauth_name == provider_name:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Linked.',
                )
        return user

    return _
