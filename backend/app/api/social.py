from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.social_service import post_to_twitter
from app.services.hashtag_service import generate_hashtags

router = APIRouter(prefix="/social", tags=["Social"])

class TwitterPost(BaseModel):
    title: str
    seo_description: str
    link: str

@router.post("/twitter")
async def twitter_post(data: TwitterPost):
    hashtags = generate_hashtags(data.title + " " + data.seo_description)
    status_text = f"{data.seo_description}\n{data.link}\n{' '.join(hashtags)}"

    try:
        response = await post_to_twitter(status_text)
        return {"message": "Successfully posted!", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
