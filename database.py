from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create SQLite database engine
engine = create_engine('sqlite:///l6l10picklists.db', echo=False)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a customized Session class
Session = sessionmaker(bind=engine)
