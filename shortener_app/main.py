from fastapi import Depends , FastAPI , HTTPException , status 
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .import crud
from .database import Base,engine,get_db
from .schemas import UrlCreate , UrlResponse
from .models import Url

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title = "URL shortener API",
    description = "A simple URL shortener API built with FastAPI and PostgreSQL",
    version = "1.0.0"
)
@app.get("/")
def root():
      return {"message": "Welcome to the URL shortener API!"}
  
@app.post(
    "/shorten",
    response_model=UrlResponse,
    status_code=201
)
def shorten_url(
    request: UrlCreate,
    db: Session = Depends(get_db)
):
    url = crud.create_shortened_url(
        db=db,
        original_url=str(request.original_url)
    )

    return UrlResponse(
        original_url=request.original_url,
        shortened_url=url.shortened_url
    )
@app.get("/{shortened_url}")
def redirect_to_original_url(
    shortened_url: str,
    db: Session = Depends(get_db)
):
    url = crud.get_original_url(
        db=db,
        shortened_url=shortened_url
    )

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )
