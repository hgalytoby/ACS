from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi_users.authentication import Strategy
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users.jwt import decode_jwt
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.router.oauth import (
    STATE_TOKEN_AUDIENCE,
    OAuth2AuthorizeResponse,
    generate_state_token,
)
from httpx_oauth.integrations.fastapi import (
    OAuth2AuthorizeCallback as _OAuth2AuthorizeCallback,
)
from httpx_oauth.oauth2 import BaseOAuth2, OAuth2Token
import jwt

from app.crud.user import (
    SECRET,
    UserManager,
    auth_backend,
    fastapi_users,
    get_user_manager,
)
from app.dependencies.oauth import is_oauth_linked
from app.models import UserModel
from app.schemas.user import UserRead

redirect_url_query = Query(
    default=None,
    description='前端的 authorize redirect_url',
    title='前端的 authorize redirect_url',
)


class OAuth2AuthorizeCallback(_OAuth2AuthorizeCallback):
    async def __call__(
        self,
        request: Request,
        code: Optional[str] = None,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        error: Optional[str] = None,
        redirect_url: Optional[str] = redirect_url_query,
    ) -> tuple[OAuth2Token, Optional[str]]:
        if code is None or error is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error if error is not None else None,
            )

        if redirect_url is None:
            redirect_url = str(request.url_for(self.route_name))

        access_token = await self.client.get_access_token(
            code, redirect_url, code_verifier
        )
        return access_token, state


def get_oauth_router(
    oauth_client: BaseOAuth2,
    associate_by_email: bool = False,
    is_verified_by_default: bool = False,
) -> APIRouter:
    """Generate a router with the OAuth routes."""
    router = APIRouter()
    callback_route_name = (
        f'oauth:{oauth_client.name}.{auth_backend.name}.callback'
    )
    oauth2_authorize_callback = OAuth2AuthorizeCallback(
        client=oauth_client,
        route_name=callback_route_name,
    )

    @router.get(
        '/authorize',
        name=f'oauth:{oauth_client.name}.{auth_backend.name}.authorize',
        response_model=OAuth2AuthorizeResponse,
    )
    async def authorize(
        request: Request,
        scopes: list[str] = Query(None),
        redirect_url: Optional[str] = redirect_url_query,
    ) -> OAuth2AuthorizeResponse:
        if redirect_url is not None:
            authorize_redirect_url = redirect_url
        else:
            authorize_redirect_url = str(request.url_for(callback_route_name))

        state_data: dict[str, str] = {}
        state = generate_state_token(state_data, SECRET)
        authorization_url = await oauth_client.get_authorization_url(
            authorize_redirect_url,
            state,
            scopes,
        )
        return OAuth2AuthorizeResponse(authorization_url=authorization_url)

    @router.get(
        '/callback',
        name=callback_route_name,
        description='The response varies based on the authentication backend used.',
        responses={
            status.HTTP_400_BAD_REQUEST: {
                'model': ErrorModel,
                'content': {
                    'application/json': {
                        'examples': {
                            'INVALID_STATE_TOKEN': {
                                'summary': 'Invalid state token.',
                                'value': None,
                            },
                            ErrorCode.LOGIN_BAD_CREDENTIALS: {
                                'summary': 'User is inactive.',
                                'value': {
                                    'detail': ErrorCode.LOGIN_BAD_CREDENTIALS,
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def callback(
        request: Request,
        access_token_state: tuple[OAuth2Token, str] = Depends(
            oauth2_authorize_callback,
        ),
        user_manager: UserManager = Depends(get_user_manager),
        strategy: Strategy = Depends(auth_backend.get_strategy),
    ):
        token, state = access_token_state
        account_id, account_email = await oauth_client.get_id_email(
            token['access_token']
        )

        if account_email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.OAUTH_NOT_AVAILABLE_EMAIL,
            )

        try:
            decode_jwt(state, SECRET, [STATE_TOKEN_AUDIENCE])
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        try:
            user = await user_manager.oauth_callback(
                oauth_client.name,
                token['access_token'],
                account_id,
                account_email,
                token.get('expires_at'),
                token.get('refresh_token'),
                request,
                associate_by_email=associate_by_email,
                is_verified_by_default=is_verified_by_default,
            )
        except UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.OAUTH_USER_ALREADY_EXISTS,
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        response = await auth_backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    return router


def get_oauth_associate_router(
    oauth_client: BaseOAuth2,
    requires_verification: bool = False,
) -> APIRouter:
    """
    Generate a router with the OAuth routes to associate an authenticated user.
    """
    router = APIRouter()

    callback_route_name = f'oauth-associate:{oauth_client.name}.callback'
    oauth2_authorize_callback = OAuth2AuthorizeCallback(
        client=oauth_client,
        route_name=callback_route_name,
    )
    get_current_active_user = fastapi_users.authenticator.current_user(
        active=True,
        verified=requires_verification,
    )

    @router.get(
        '/authorize',
        name=f'oauth-associate:{oauth_client.name}.authorize',
        response_model=OAuth2AuthorizeResponse,
    )
    async def authorize(
        request: Request,
        scopes: list[str] = Query(None),
        user: UserModel = Depends(is_oauth_linked(oauth_client.name)),
        redirect_url: Optional[str] = redirect_url_query,
    ) -> OAuth2AuthorizeResponse:
        if redirect_url is not None:
            authorize_redirect_url = redirect_url
        else:
            authorize_redirect_url = str(request.url_for(callback_route_name))

        state_data: dict[str, str] = {'sub': str(user.id)}
        state = generate_state_token(state_data, SECRET)
        authorization_url = await oauth_client.get_authorization_url(
            authorize_redirect_url,
            state,
            scopes,
        )

        return OAuth2AuthorizeResponse(authorization_url=authorization_url)

    @router.get(
        '/callback',
        response_model=UserRead,
        name=callback_route_name,
        description='The response varies based on the authentication backend used.',
        responses={
            status.HTTP_400_BAD_REQUEST: {
                'model': ErrorModel,
                'content': {
                    'application/json': {
                        'examples': {
                            'INVALID_STATE_TOKEN': {
                                'summary': 'Invalid state token.',
                                'value': None,
                            },
                        }
                    }
                },
            },
        },
    )
    async def callback(
        request: Request,
        user: UserModel = Depends(get_current_active_user),
        access_token_state: tuple[OAuth2Token, str] = Depends(
            oauth2_authorize_callback
        ),
        user_manager: UserManager = Depends(get_user_manager),
    ):
        token, state = access_token_state
        account_id, account_email = await oauth_client.get_id_email(
            token['access_token']
        )

        if account_email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.OAUTH_NOT_AVAILABLE_EMAIL,
            )

        try:
            state_data = decode_jwt(state, SECRET, [STATE_TOKEN_AUDIENCE])
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if state_data['sub'] != str(user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        user = await user_manager.oauth_associate_callback(
            user,
            oauth_client.name,
            token['access_token'],
            account_id,
            account_email,
            token.get('expires_at'),
            token.get('refresh_token'),
            request,
        )

        return UserRead.from_orm(user)

    return router
