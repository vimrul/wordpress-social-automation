from tweepy import Client
from app.core.database import database
from app.models.credentials import credentials

async def get_twitter_credentials():
    await database.connect()
    query = credentials.select().where(credentials.c.platform == "twitter")
    twitter_cred = await database.fetch_one(query)
    await database.disconnect()
    return twitter_cred

async def post_to_twitter(status_text: str):
    creds = await get_twitter_credentials()
    if not creds:
        raise Exception("Twitter OAuth2 credentials not found. Please authenticate.")

    print("🚀 Attempting to post to Twitter...")
    print("📝 Tweet Content:\n", status_text)
    print("🔐 Initializing Tweepy client...")

    try:
        client = Client(
            access_token=creds.oauth_token  # Using OAuth2 access token
        )

        print("📡 Sending tweet...")
        response = client.create_tweet(text=status_text)
        print("✅ Tweet posted! Response:", response)

        return response.data

    except Exception as e:
        print("❌ Failed to post tweet.")
        print("💥 Exception:", e)
        raise e
