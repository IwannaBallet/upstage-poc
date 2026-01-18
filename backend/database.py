from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@localhost:5432/askup_voc"

# In Docker optimization, it might be "db" instead of localhost, 
# but for local running (which we might do) localhost is needed if ports are mapped.
# Ideally, we read from env.

import os
DB_HOST = os.getenv("DB_HOST", "localhost")
SQLALCHEMY_DATABASE_URL = f"postgresql://admin:password@{DB_HOST}:5432/askup_voc"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
