from typing import Optional
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback as _OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2Token
from fastapi import Request, HTTPException, status, Query


class OAuth2AuthorizeCallback(_OAuth2AuthorizeCallback):
    async def __call__(
            self,
            request: Request,
            code: Optional[str] = None,
            code_verifier: Optional[str] = None,
            state: Optional[str] = None,
            error: Optional[str] = None,
            redirect_url: Optional[str] = Query(
                default=None,
                description='前端的 authorize redirect_url',
                title='前端的 authorize redirect_url',
            )
    ) -> tuple[OAuth2Token, Optional[str]]:
        if code is None or error is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error if error is not None else None,
            )
        if redirect_url is None:
            redirect_url = self.route_name
        access_token = await self.client.get_access_token(
            code, redirect_url, code_verifier
        )
        return access_token, state
