import asyncio
import json
from app.core.database import database
from app.models.credentials import credentials

async def debug_token():
    await database.connect()
    result = await database.fetch_one(credentials.select().where(credentials.c.platform == "twitter"))
    await database.disconnect()

    if result:
        print("Stored Twitter Credential:\n", json.dumps(dict(result), indent=4))
    else:
        print("❌ No Twitter credentials found.")

# Run the async function
if __name__ == "__main__":
    asyncio.run(debug_token())
