from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
class Settings(BaseSettings):
    database_url : str
    model_config = SettingsConfigDict(env_file = ".env")
    
settings = Settings()
engine = create_engine(settings.database_url)
sessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False ,
    bind = engine
)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try :
        yield db
    finally:
        db.close()
    