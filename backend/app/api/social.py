# app/api/social.py
from fastapi import APIRouter, HTTPException
from tweepy import Client
from app.core.database import database
from app.models.credentials import credentials
from pydantic import BaseModel
from app.services.hashtag_service import generate_hashtags
from app.core.config import settings

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
        raise HTTPException(status_code=403, detail="❌ Twitter OAuth2 credentials not found. Please authenticate.")

    try:
        print("🚀 Attempting to post to Twitter...")
        print("📝 Tweet Content:\n", status_text)

        # ✅ Correct usage: ONLY access_token + client_id + client_secret
        client = Client(
            access_token=creds.oauth_token,
            client_id=settings.TWITTER_CLIENT_ID,
            client_secret=settings.TWITTER_CLIENT_SECRET
        )

        print("📡 Sending tweet...")
        response = client.create_tweet(text=status_text)

        print("✅ Tweet posted! Response:", response)
        return {"message": "✅ Tweet posted!", "response": response.data}

    except Exception as e:
        print("❌ Failed to post tweet.")
        print("💥 Exception:", e)
        raise HTTPException(status_code=400, detail=str(e))
