from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from app.core.config import settings
from app.core.database import database
from app.models.credentials import credentials
import tweepy

router = APIRouter(prefix="/auth", tags=["Auth"])

# Twitter login route - redirects user to Twitter for authorization
@router.get("/twitter")
async def twitter_login(request: Request):
    try:
        oauth_handler = tweepy.OAuth1UserHandler(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            callback="http://localhost:8000/auth/twitter/callback"
        )

        authorization_url = oauth_handler.get_authorization_url()

        # Save request token in session
        request.session["request_token"] = oauth_handler.request_token

        return RedirectResponse(authorization_url)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Twitter callback route - Twitter redirects back here after user authorizes
@router.get("/twitter/callback")
async def twitter_callback(request: Request, oauth_token: str, oauth_verifier: str):
    try:
        request_token = request.session.get("request_token")
        if not request_token:
            return JSONResponse(status_code=400, content={"error": "Missing request token in session"})

        oauth_handler = tweepy.OAuth1UserHandler(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET
        )
        oauth_handler.request_token = request_token

        access_token, access_token_secret = oauth_handler.get_access_token(oauth_verifier)

        # Save credentials to DB
        query = credentials.insert().values(
            platform="twitter",
            oauth_token=access_token,
            oauth_token_secret=access_token_secret
        )

        await database.connect()
        await database.execute(query)
        await database.disconnect()

        return JSONResponse(content={
            "message": "Twitter authentication successful!",
            "access_token": access_token,
            "access_token_secret": access_token_secret
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# from fastapi import APIRouter, Request, HTTPException
# from fastapi.responses import RedirectResponse
# from requests_oauthlib import OAuth1Session
# from app.core.config import settings
# from app.core.database import database
# from app.models.credentials import credentials

# router = APIRouter(prefix="/auth", tags=["Auth"])

# # In-memory store for temporary credentials (use secure store like Redis in production)
# temporary_tokens = {}

# @router.get("/twitter")
# async def twitter_login():
#     try:
#         oauth = OAuth1Session(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
#         fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")

#         # Save the temporary token & secret
#         temp_oauth_token = fetch_response.get("oauth_token")
#         temp_oauth_token_secret = fetch_response.get("oauth_token_secret")
#         temporary_tokens[temp_oauth_token] = temp_oauth_token_secret

#         authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
#         return RedirectResponse(authorization_url)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Twitter login failed: {str(e)}")


# @router.get("/twitter/callback")
# async def twitter_callback(oauth_token: str, oauth_verifier: str):
#     try:
#         temp_secret = temporary_tokens.get(oauth_token)
#         if not temp_secret:
#             raise HTTPException(status_code=400, detail="Missing temporary token secret.")

#         # Rebuild the session using the temp credentials and verifier
#         oauth = OAuth1Session(
#             settings.TWITTER_API_KEY,
#             settings.TWITTER_API_SECRET,
#             resource_owner_key=oauth_token,
#             resource_owner_secret=temp_secret,
#             verifier=oauth_verifier
#         )

#         access_token_url = "https://api.twitter.com/oauth/access_token"
#         oauth_tokens = oauth.fetch_access_token(access_token_url)

#         final_oauth_token = oauth_tokens.get("oauth_token")
#         final_oauth_token_secret = oauth_tokens.get("oauth_token_secret")

#         # Save access tokens to DB
#         query = credentials.insert().values(
#             platform="twitter",
#             oauth_token=final_oauth_token,
#             oauth_token_secret=final_oauth_token_secret
#         )
#         await database.connect()
#         await database.execute(query)
#         await database.disconnect()

#         return {"message": "✅ Twitter authentication successful!"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Twitter callback failed: {str(e)}")

