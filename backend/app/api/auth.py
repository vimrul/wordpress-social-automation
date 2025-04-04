from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from app.core.config import settings
from app.core.database import database
from app.models.credentials import credentials
import secrets
import requests
import urllib.parse

router = APIRouter(prefix="/auth", tags=["Auth"])

TWITTER_AUTHORIZE_URL = "https://twitter.com/i/oauth2/authorize"
TWITTER_TOKEN_URL = "https://api.twitter.com/2/oauth2/token"

@router.get("/twitter")
async def twitter_login(request: Request):
    try:
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = code_verifier  # Twitter uses plain PKCE, no SHA256

        state = secrets.token_urlsafe(16)
        request.session["state"] = state
        request.session["code_verifier"] = code_verifier

        params = {
            "response_type": "code",
            "client_id": settings.TWITTER_CLIENT_ID,
            "redirect_uri": settings.TWITTER_REDIRECT_URI,
            "scope": "tweet.read tweet.write users.read offline.access",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "plain"
        }

        url = f"{TWITTER_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
        return RedirectResponse(url)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/twitter/callback")
async def twitter_callback(request: Request, code: str, state: str):
    try:
        saved_state = request.session.get("state")
        code_verifier = request.session.get("code_verifier")

        if state != saved_state:
            return JSONResponse(status_code=400, content={"error": "State mismatch"})

        data = {
            "client_id": settings.TWITTER_CLIENT_ID,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.TWITTER_REDIRECT_URI,
            "code_verifier": code_verifier,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(TWITTER_TOKEN_URL, data=data, headers=headers, auth=(settings.TWITTER_CLIENT_ID, settings.TWITTER_CLIENT_SECRET))

        if response.status_code != 200:
            return JSONResponse(status_code=500, content={"error": response.json()})

        token_data = response.json()
        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")

        await database.connect()
        await database.execute(
            credentials.insert().values(
                platform="twitter",
                oauth_token=access_token,
                oauth_token_secret=refresh_token
            )
        )
        await database.disconnect()

        return JSONResponse({
            "message": "✅ Twitter OAuth2 success!",
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
