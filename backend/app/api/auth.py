from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth1Session
from app.core.config import settings
from app.core.database import database
from app.models.credentials import credentials

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/twitter")
async def twitter_login():
    oauth = OAuth1Session(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
    authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
    return RedirectResponse(authorization_url)

@router.get("/twitter/callback")
async def twitter_callback(oauth_token: str, oauth_verifier: str):
    oauth = OAuth1Session(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        oauth_token,
        oauth_verifier
    )

    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    oauth_token = oauth_tokens.get("oauth_token")
    oauth_token_secret = oauth_tokens.get("oauth_token_secret")

    # Securely store tokens in database
    query = credentials.insert().values(
        platform="twitter",
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret
    )
    await database.connect()
    await database.execute(query)
    await database.disconnect()

    return {"message": "Twitter authentication successful!"}
