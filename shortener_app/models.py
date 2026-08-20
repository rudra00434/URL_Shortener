import uuid
from sqlalchemy import Column , String , Text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
class Url(Base):
    __tablename__ = "urls"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    original_url = Column(Text,nullable= False)
    shortened_url = Column(String(10),nullable=False,unique=True,index=True)
    