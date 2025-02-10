from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/qrmenu"
# Create the engine
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base
Base = declarative_base()

def get_session() -> Session:
    session = Session()

    try:
        yield session
    except Exception as err:
        raise err
    finally:
        session.close()
