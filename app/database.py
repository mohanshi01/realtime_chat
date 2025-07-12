import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://postgres:postgres@db:5432/chatdb"

#retry loop: to wait 10 times for db to be ready
for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        break
    except OperationalError:
        print("Waiting for PostgreSQL to be ready...")
        time.sleep(2)
else:
    raise Exception("Could not connect to the database.")

SessionLocal = sessionmaker(bind=engine)
