import httpx
from typing import List
from app.schemas.posts import Post
from bs4 import BeautifulSoup

async def fetch_wordpress_posts(url: str) -> List[Post]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        posts_json = response.json()

        posts = []
        for post in posts_json:
            excerpt = BeautifulSoup(post['excerpt']['rendered'], 'html.parser').text.strip()

            # SEO description fallback
            seo_description = post.get('yoast_head_json', {}).get('description', excerpt)

            # Featured image
            featured_media = post.get('jetpack_featured_media_url', None)

            posts.append(Post(
                id=post['id'],
                date=post['date'],
                title=BeautifulSoup(post['title']['rendered'], 'html.parser').text.strip(),
                excerpt=excerpt,
                link=post['link'],
                seo_description=seo_description,
                featured_image=featured_media
            ))

        return posts
