from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Заменить myuser, mypassword и mydatabase на реальные данные
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
