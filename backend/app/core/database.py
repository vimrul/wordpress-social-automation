from databases import Database
from sqlalchemy import create_engine, MetaData

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
if __name__ == "__main__":
    metadata.create_all(engine)