from fastapi import APIRouter
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.config import settings
from app.utils.oauth import get_oauth_router, get_oauth_associate_router

router = APIRouter(tags=['OAuth'])

google_oauth_client = GoogleOAuth2(*settings.oauth.google)
github_oauth_client = GitHubOAuth2(*settings.oauth.github)
github_associate_oauth_client = GitHubOAuth2(*settings.oauth.github_associate)
microsoft_oauth_client = MicrosoftGraphOAuth2(*settings.oauth.microsoft)

router.include_router(
    get_oauth_router(
        oauth_client=google_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/google',
)

router.include_router(
    get_oauth_associate_router(
        oauth_client=google_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/google',
)

router.include_router(
    get_oauth_router(
        oauth_client=github_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/github',
)

router.include_router(
    get_oauth_associate_router(
        oauth_client=github_associate_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/github',
)

router.include_router(
    get_oauth_router(
        microsoft_oauth_client,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix='/auth/microsoft',
)

router.include_router(
    get_oauth_associate_router(
        oauth_client=microsoft_oauth_client,
        requires_verification=True,
    ),
    prefix='/auth/associate/microsoft',
)
