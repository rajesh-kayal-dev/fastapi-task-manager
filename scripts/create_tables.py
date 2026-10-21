import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import Base, engine
from app.models import Task, User

Base.metadata.create_all(bind=engine)

print("Tables created successfully")