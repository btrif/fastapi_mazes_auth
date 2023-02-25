#  Created by btrif Trif on 25-02-2023 , 12:17 PM.

from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
# from database import Base, get_db
from src.mazes.database import Base, get_db

from src.mazes.main import mazes_app

# Create a test DB session
SQLALCHEMY_DATABASE_URL = "sqlite:///../test_mazes_app.db"
test_db_engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False}
        )

this_session = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
test_current_session_local = this_session()

Base.metadata.create_all(bind=test_db_engine)

def override_get_db():
    try:
        db = test_current_session_local()
        yield db
    finally:
        db.close()

mazes_app.dependency_overrides[get_db] = override_get_db

client = TestClient(mazes_app)
