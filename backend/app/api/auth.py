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
        # ✅ Generate your own code_verifier
        print("📦 Session keys at callback:", list(request.session.keys()))
        print("📦 code_verifier at callback:", request.session.get("code_verifier"))
        code_verifier = secrets.token_urlsafe(64)
        request.session["code_verifier"] = code_verifier  # ✅ this must be a string

        # ✅ Initialize handler WITHOUT code_verifier here
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.TWITTER_CLIENT_ID,
            redirect_uri=settings.TWITTER_REDIRECT_URI,
            scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
            client_secret=settings.TWITTER_CLIENT_SECRET,
        )

        # ✅ Set it explicitly
        oauth2_handler.code_verifier = code_verifier

        # ✅ Get URL
        authorization_url = oauth2_handler.get_authorization_url()

        # ✅ Save only string types
        request.session["state"] = str(oauth2_handler.state)
        request.session["code_verifier"] = str(code_verifier)

        return RedirectResponse(authorization_url)

    except Exception as e:
        print("💥 Error in /auth/twitter:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/twitter/callback")
async def twitter_callback(request: Request, code: str, state: str):
    try:
        code_verifier = request.session.get("code_verifier")
        print("📦 Session keys at callback:", list(request.session.keys()))
        print("📦 code_verifier at callback:", code_verifier)

        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.TWITTER_CLIENT_ID,
            redirect_uri=settings.TWITTER_REDIRECT_URI,
            scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
            client_secret=settings.TWITTER_CLIENT_SECRET,
        )
        # ✅ Must assign again
        oauth2_handler.code_verifier = code_verifier

        # 👇 Explicitly pass code_verifier here!
        token_data = oauth2_handler.fetch_token(
            authorization_response=f"{settings.TWITTER_REDIRECT_URI}?code={code}&state={state}",
            code_verifier=code_verifier
        )

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
        print("💥 Callback error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
