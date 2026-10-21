import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from app.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Database connected:", result.scalar())