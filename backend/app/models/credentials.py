from sqlalchemy import Table, Column, String, Integer, DateTime
from datetime import datetime
from app.core.database import metadata

credentials = Table(
    "credentials",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("platform", String, nullable=False),
    Column("oauth_token", String, nullable=False),
    Column("oauth_token_secret", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
)
