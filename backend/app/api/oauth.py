from fastapi import APIRouter
from httpx_oauth.clients.facebook import FacebookOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.config import settings
from app.utils.oauth import get_oauth_router, get_oauth_associate_router

router = APIRouter()

google_oauth_client = GoogleOAuth2(*settings.oauth.google)
github_oauth_client = GitHubOAuth2(*settings.oauth.github)
facebook_oauth_client = FacebookOAuth2(*settings.oauth.facebook)

router.include_router(
    get_oauth_router(
        oauth_client=google_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/google',
    tags=['OAuth'],
)

router.include_router(
    get_oauth_associate_router(
        oauth_client=google_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/google',
    tags=['OAuth'],
)

router.include_router(
    get_oauth_router(
        oauth_client=github_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/github',
    tags=['OAuth'],
)


router.include_router(
    get_oauth_associate_router(
        oauth_client=github_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/github',
    tags=['OAuth'],
)

router.include_router(
    get_oauth_router(
        facebook_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/facebook',
    tags=['OAuth'],
)

router.include_router(
    get_oauth_associate_router(
        oauth_client=facebook_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/facebook',
    tags=['OAuth'],
)
