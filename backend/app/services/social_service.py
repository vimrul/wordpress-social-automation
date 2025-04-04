import tweepy
from app.core.database import database
from app.models.credentials import credentials
from app.core.config import settings

async def get_twitter_credentials():
    await database.connect()
    query = credentials.select().where(credentials.c.platform == "twitter")
    twitter_cred = await database.fetch_one(query)
    await database.disconnect()
    return twitter_cred

async def post_to_twitter(status_text: str):
    creds = await get_twitter_credentials()
    if not creds:
        raise Exception("Twitter credentials not found.")

    client = tweepy.Client(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=creds.oauth_token,
        access_token_secret=creds.oauth_token_secret
    )

    response = client.create_tweet(text=status_text)

    return response.data


# async def post_to_twitter(status_text: str):
#     creds = await get_twitter_credentials()
#     if not creds:
#         raise Exception("Twitter credentials not found.")

#     oauth = OAuth1Session(
#         settings.TWITTER_API_KEY,
#         settings.TWITTER_API_SECRET,
#         creds.oauth_token,
#         creds.oauth_token_secret
#     )

#     url = "https://api.twitter.com/1.1/statuses/update.json"
#     payload = {"status": status_text}

#     response = oauth.post(url, params=payload)
#     response.raise_for_status()
#     return response.json()
