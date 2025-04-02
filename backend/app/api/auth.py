from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth1Session
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/twitter")
async def twitter_login():
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    fetch_response = oauth.fetch_request_token(request_token_url)
    
    resource_owner_key = fetch_response.get("oauth_token")
    
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    
    return RedirectResponse(authorization_url)
