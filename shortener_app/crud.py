import secrets
import string
from sqlalchemy.orm import Session 
from .models import Url
def generate_shortened_url(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

def create_shortened_url(db: Session, original_url: str) -> Url:
    while True:
        shortened_url = generate_shortened_url()
        existing_url = db.query(Url).filter(Url.shortened_url == shortened_url).first()
        if not existing_url :
            break 
    
    new_url = Url(original_url=original_url,shortened_url=shortened_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url
    
def get_original_url(db: Session, shortened_url: str) -> Url:
    return db.query(Url).filter(Url.shortened_url == shortened_url).first()

        