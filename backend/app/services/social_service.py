import tweepy
import json
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
    print("\n🚀 Attempting to post to Twitter...")

    creds = await get_twitter_credentials()
    if not creds:
        print("❌ Twitter credentials not found in DB.")
        raise Exception("Twitter credentials not found.")

    # Clean and limit tweet text
    if len(status_text) > 280:
        print(f"⚠️ Tweet is too long ({len(status_text)} chars), truncating...")
        status_text = status_text[:277] + "..."

    status_text = status_text.encode("utf-8", "ignore").decode("utf-8")
    print(f"📝 Tweet Content:\n{status_text}\n")

    try:
        print("🔐 Initializing Tweepy client...")
        client = tweepy.Client(
            bearer_token=settings.TWITTER_BEARER_TOKEN,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=creds.oauth_token,
            access_token_secret=creds.oauth_token_secret
        )

        print("📡 Sending tweet...")
        response = client.create_tweet(text=status_text)

        print("✅ Tweet posted successfully!")
        print(f"📄 Twitter Response: {json.dumps(response.data, indent=2)}")

        return response.data

    except Exception as e:
        print("❌ Failed to post tweet.")
        print(f"💥 Exception: {str(e)}")

        # Try to log Twitter response if available
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_text = e.response.text
                print("🧾 Twitter API Response:")
                print(error_text)

                with open("twitter_error_response.txt", "w") as f:
                    f.write(f"Status: {e.response.status_code}\n")
                    f.write(error_text)
        except Exception as log_error:
            print(f"⚠️ Failed to log error details: {log_error}")

        raise Exception("Twitter post failed.") from e


# import tweepy
# from app.core.database import database
# from app.models.credentials import credentials
# from app.core.config import settings

# async def get_twitter_credentials():
#     await database.connect()
#     query = credentials.select().where(credentials.c.platform == "twitter")
#     twitter_cred = await database.fetch_one(query)
#     await database.disconnect()
#     return twitter_cred

# async def post_to_twitter(status_text: str):
#     creds = await get_twitter_credentials()
#     if not creds:
#         raise Exception("Twitter credentials not found.")

#     # Tweepy Client initialization with bearer token
#     client = tweepy.Client(
#         bearer_token=settings.TWITTER_BEARER_TOKEN,  # clearly add this line
#         consumer_key=settings.TWITTER_API_KEY,
#         consumer_secret=settings.TWITTER_API_SECRET,
#         access_token=creds.oauth_token,
#         access_token_secret=creds.oauth_token_secret
#     )

#     response = client.create_tweet(text=status_text)

#     return response.data



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
