from sqlalchemy import create_engine
from app.models.credentials import credentials, metadata
from app.core.config import settings

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    metadata.create_all(engine)
    print("✅ Table 'credentials' created successfully.")

if __name__ == "__main__":
    init_db()
