from requests_oauthlib import OAuth1Session
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

    if len(status_text) > 280:
        status_text = status_text[:277] + "..."

    status_text = status_text.encode("utf-8", "ignore").decode("utf-8")

    oauth = OAuth1Session(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        creds.oauth_token,
        creds.oauth_token_secret
    )

    url = "https://api.twitter.com/1.1/statuses/update.json"
    payload = {"status": status_text}

    response = oauth.post(url, params=payload)

    # Log response even if it's an error
    if response.status_code != 200:
        # Print to console
        print("❌ Twitter API Error:")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        # Optional: Write to a file
        with open("twitter_error_response.txt", "w") as f:
            f.write(f"Status: {response.status_code}\n")
            f.write(response.text)

        raise Exception(f"Twitter post failed with status {response.status_code}")

    return response.json()


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
