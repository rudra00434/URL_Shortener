from pydantic import BaseModel, HttpUrl
class UrlCreate(BaseModel):
    original_url: HttpUrl
class UrlResponse(BaseModel):
    original_url: HttpUrl
    shortened_url: str