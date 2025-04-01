from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.posts import PostsResponse
from app.services.wordpress_service import fetch_wordpress_posts

router = APIRouter(prefix="/wordpress", tags=["WordPress"])

@router.get("/posts", response_model=PostsResponse)
async def get_posts(json_url: str = Query(..., description="WordPress JSON API URL")):
    try:
        posts = await fetch_wordpress_posts(json_url)
        return {"count": len(posts), "posts": posts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching posts: {str(e)}")
