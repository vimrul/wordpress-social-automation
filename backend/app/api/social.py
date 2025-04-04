from fastapi import APIRouter, HTTPException
from tweepy import Client
from app.core.database import database
from app.models.credentials import credentials
from pydantic import BaseModel
from app.services.hashtag_service import generate_hashtags

router = APIRouter(prefix="/social", tags=["Social"])

class TwitterPost(BaseModel):
    title: str
    seo_description: str
    link: str

async def get_twitter_credentials():
    await database.connect()
    query = credentials.select().where(credentials.c.platform == "twitter")
    twitter_cred = await database.fetch_one(query)
    await database.disconnect()
    return twitter_cred

@router.post("/twitter")
async def twitter_post(data: TwitterPost):
    hashtags = generate_hashtags(f"{data.title} {data.seo_description}")
    status_text = f"{data.seo_description}\n{data.link}\n{' '.join(hashtags)}"

    creds = await get_twitter_credentials()
    if not creds:
        raise HTTPException(status_code=403, detail="Twitter OAuth2 credentials not found. Please authenticate.")

    try:
        print("🚀 Attempting to post to Twitter...")
        print("📝 Tweet Content:\n", status_text)

        # ✅ Only use access_token here for OAuth2 user context
        client = Client(access_token=creds.oauth_token)

        print("📡 Sending tweet...")
        response = client.create_tweet(text=status_text)
        print("✅ Tweet posted! Response:", response)

        return {"message": "✅ Tweet posted!", "response": response.data}

    except Exception as e:
        print("❌ Failed to post tweet.")
        print("💥 Exception:", e)
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/debug/twitter-token")
async def debug_twitter_token():
    await database.connect()
    result = await database.fetch_one(credentials.select().where(credentials.c.platform == "twitter"))
    await database.disconnect()

    if result:
        return {"twitter_credentials": dict(result)}
    return {"message": "No Twitter credentials found"}