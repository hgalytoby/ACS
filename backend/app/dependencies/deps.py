from fastapi import Header, HTTPException, status, Depends, Request

from app.crud.user import current_active_verified_user
from app.models import UserModel
from app.utils.enums import SteinsGate


def valid_accept_token(divergence: str = Header()):
    if divergence != SteinsGate.DIVERGENCE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=SteinsGate.PLAN,
        )


async def authorize_api(
        request: Request,
        user: UserModel = Depends(current_active_verified_user),
):
    if user.is_superuser:
        return

    uri = request.scope['route'].path
    method = request.method

    for role in user.role_list:
        for api in role.api_list:
            if api.uri == uri and api.method == method:
                return

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
