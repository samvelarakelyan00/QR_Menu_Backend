from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/mydatabase"
# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Define the Base
Base = declarative_base()
