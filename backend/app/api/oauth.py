from fastapi import APIRouter
from httpx_oauth.clients.facebook import FacebookOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.config import settings
from app.crud.user import (
    fastapi_users,
    auth_backend,
    SECRET,
)
from app.schemas.user import UserRead

router = APIRouter()

google_oauth_client = GoogleOAuth2(*settings.oauth.google)
github_oauth_client = GitHubOAuth2(*settings.oauth.github)
facebook_oauth_client = FacebookOAuth2(*settings.oauth.facebook)

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/google',
    tags=['OAuth'],
)

router.include_router(
    fastapi_users.get_oauth_associate_router(
        google_oauth_client,
        UserRead,
        SECRET,
        requires_verification=True,
    ),
    prefix='/auth/associate/google',
    tags=['OAuth'],
)

router.include_router(
    fastapi_users.get_oauth_router(
        github_oauth_client,
        auth_backend,
        SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/github',
    tags=['OAuth'],
)

router.include_router(
    fastapi_users.get_oauth_associate_router(
        github_oauth_client,
        UserRead,
        SECRET,
        requires_verification=True,
    ),
    prefix='/auth/associate/github',
    tags=['OAuth'],
)

router.include_router(
    fastapi_users.get_oauth_router(
        facebook_oauth_client,
        auth_backend,
        SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/facebook',
    tags=['OAuth'],
)

router.include_router(
    fastapi_users.get_oauth_associate_router(
        facebook_oauth_client,
        UserRead,
        SECRET,
        requires_verification=True,
    ),
    prefix='/auth/associate/facebook',
    tags=['OAuth'],
)
