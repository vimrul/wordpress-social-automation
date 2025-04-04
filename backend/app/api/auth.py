from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from app.core.config import settings
from app.core.database import database
from app.models.credentials import credentials
import tweepy
import secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/twitter")
async def twitter_login(request: Request):
    try:
        # Generate a secure code_verifier
        code_verifier = secrets.token_urlsafe(64)

        # Initialize the OAuth2 handler
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.TWITTER_CLIENT_ID,
            redirect_uri=settings.TWITTER_REDIRECT_URI,
            scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
            client_secret=settings.TWITTER_CLIENT_SECRET
        )

        # Assign code_verifier after init
        oauth2_handler.code_verifier = code_verifier

        # Generate the authorization URL
        authorization_url = oauth2_handler.get_authorization_url()

        # ✅ Only store serializable values in session
        request.session["code_verifier"] = code_verifier
        request.session["state"] = oauth2_handler.state

        return RedirectResponse(authorization_url)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/twitter/callback")
async def twitter_callback(request: Request, code: str, state: str):
    try:
        # Retrieve saved state and code_verifier from session
        code_verifier = request.session.get("code_verifier")
        saved_state = request.session.get("state")

        if not code_verifier or saved_state != state:
            return JSONResponse(status_code=400, content={"error": "Invalid state or missing verifier"})

        # Rebuild the handler
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.TWITTER_CLIENT_ID,
            redirect_uri=settings.TWITTER_REDIRECT_URI,
            scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
            client_secret=settings.TWITTER_CLIENT_SECRET
        )

        oauth2_handler.code_verifier = code_verifier

        # Exchange code for tokens
        token_data = oauth2_handler.fetch_token(
            code=code
        )

        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")

        # Save to database
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
            "message": "✅ Twitter OAuth2 authentication successful!",
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
