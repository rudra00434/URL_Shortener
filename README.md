# URL Shortener API

A basic URL Shortener REST API built using **FastAPI, PostgreSQL, and SQLAlchemy**.

The API accepts a long URL, generates a unique short code, stores the URL mapping in PostgreSQL, and redirects users from the shortened URL to the original URL.

## Features

* Create shortened URLs
* Generate random 8-character short codes
* Collision checking for generated short codes
* Store URL mappings in PostgreSQL
* Redirect shortened URLs to the original URL
* URL validation using Pydantic
* UUID-based primary key
* HTTP 404 handling for non-existent short URLs
* Interactive API documentation using Swagger UI
* Environment-based database configuration

## Technology Stack

| Technology      | Purpose                      |
| --------------- | ---------------------------- |
| Python          | Programming language         |
| FastAPI         | REST API framework           |
| PostgreSQL      | Relational database          |
| SQLAlchemy      | ORM and database interaction |
| Pydantic        | Request validation           |
| Uvicorn         | ASGI server                  |
| psycopg2-binary | PostgreSQL database driver   |

## Project Structure

```text
url_shortener/
│
├── shortener_app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### File Responsibilities

**`main.py`**

Defines the FastAPI application and API endpoints.

**`database.py`**

Configures the PostgreSQL connection, SQLAlchemy engine, session factory, and database dependency.

**`models.py`**

Defines the SQLAlchemy database model for storing URL information.

**`schemas.py`**

Defines Pydantic request and response schemas and validates incoming URLs.

**`crud.py`**

Contains short-code generation, collision checking, URL creation, and URL retrieval operations.

**`.env.example`**

Provides a template for the database connection configuration without exposing credentials.

**`.gitignore`**

Prevents sensitive files, virtual environments, cache files, and IDE files from being included.

**`requirements.txt`**

Contains the Python dependencies required to run the application.

## Database Design

The application uses a PostgreSQL database named:

```text
url_shortener
```

The application creates a table named:

```text
urls
```

### `urls` Table

| Column          | Type        | Constraints               | Description                    |
| --------------- | ----------- | ------------------------- | ------------------------------ |
| `id`            | UUID        | Primary Key               | Unique identifier for each URL |
| `original_url`  | TEXT        | NOT NULL                  | Original long URL              |
| `shortened_url` | VARCHAR(10) | UNIQUE, NOT NULL, INDEXED | Generated short code           |

Example:

```text
id                                    original_url             shortened_url
--------------------------------------------------------------------------------
UUID                                  https://google.com       aB72xK9p
```

The UUID is used as the internal database identifier, while the generated short code is used as the public shortened identifier.

## API Endpoints

### 1. Create Short URL

**POST `/shorten`**

Creates a shortened URL.

#### Request

```http
POST /shorten
Content-Type: application/json
```

Request body:

```json
{
  "original_url": "https://www.google.com"
}
```

#### Response

Status:

```text
201 Created
```

Example:

```json
{
  "original_url": "https://www.google.com",
  "shortened_url": "aB72xK9p"
}
```

The actual short code will be randomly generated.

---

### 2. Redirect to Original URL

**GET `/{shortened_url}`**

Retrieves the original URL associated with the supplied short code and redirects the client.

Example:

```http
GET /aB72xK9p
```

If the short code exists, the API returns:

```text
307 Temporary Redirect
```

and redirects the client to the original URL.

If the short code does not exist:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Short URL not found"
}
```

## URL Validation

The API uses Pydantic's `HttpUrl` type to validate the submitted URL.

A valid request:

```json
{
  "original_url": "https://www.google.com"
}
```

An invalid request such as:

```json
{
  "original_url": "hello"
}
```

will be rejected by FastAPI's validation system.

## Short Code Generation

The application generates an 8-character short code using:

* Uppercase letters
* Lowercase letters
* Digits

Python's `secrets` module is used for generating the characters.

Example:

```text
aB72xK9p
```

Before storing the generated code, the application checks whether the code already exists in the database.

If a collision occurs, another code is generated.

The database also has a `UNIQUE` constraint on `shortened_url` as an additional integrity constraint.

## Application Flow

### Creating a Short URL

```text
Client
  |
  | POST /shorten
  v
FastAPI
  |
  | Request validation
  v
Pydantic
  |
  v
CRUD Layer
  |
  | Generate short code
  | Check collision
  v
SQLAlchemy
  |
  v
PostgreSQL
  |
  v
JSON Response
```

### Redirecting a Short URL

```text
Client
  |
  | GET /short_code
  v
FastAPI
  |
  v
CRUD Layer
  |
  v
PostgreSQL
  |
  | Find original URL
  v
RedirectResponse
  |
  v
Original URL
```

## Setup Instructions

### Prerequisites

Make sure the following are installed:

* Python 3.10 or higher
* PostgreSQL
* pip

### 1. Create the PostgreSQL Database

Create a database named:

```text
url_shortener
```

For example:

```sql
CREATE DATABASE url_shortener;
```

### 2. Create a Virtual Environment

From the project root:

```powershell
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener
```

Replace `username` and `password` with the PostgreSQL credentials configured on your system.

For security reasons, the actual `.env` file should not be committed or shared.

The project provides `.env.example` as a configuration template.

### 5. Run the Application

From the project root:

```powershell
uvicorn shortener_app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The alternative ReDoc documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

## Testing

The API can be tested using Swagger UI, Postman, or a web browser.

### Test 1 — Create a Short URL

Send:

```http
POST /shorten
```

with:

```json
{
  "original_url": "https://www.google.com"
}
```

Expected:

```text
201 Created
```

### Test 2 — Redirect

Use the returned `shortened_url`:

```text
http://127.0.0.1:8000/<shortened_url>
```

The API should redirect to the original URL.

Expected status:

```text
307 Temporary Redirect
```

### Test 3 — Invalid Short Code

Request a code that does not exist:

```text
http://127.0.0.1:8000/doesnotexist
```

Expected:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Short URL not found"
}
```

### Test 4 — Invalid URL

Send an invalid URL to `/shorten`:

```json
{
  "original_url": "hello"
}
```

Pydantic validation should reject the request.

## Security and Configuration

Database credentials are stored in environment variables rather than being hardcoded in the application.

The `.env` file is excluded using `.gitignore`.

Only `.env.example`, containing placeholder credentials, should be included in the submitted project.

## URL Shortener Architecture
```text

                         CLIENT
                           │
                           │ HTTP Request
                           ▼
                    ┌───────────────┐
                    │    FastAPI    │
                    │   API Layer   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Pydantic   │
                    │   Validation  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   CRUD Layer  │
                    │ Business Logic│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   SQLAlchemy  │
                    │      ORM      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  PostgreSQL   │
                    │    Database   │
                    └───────────────┘
```
## Future Improvements

For a production-scale URL shortener, the following features could be considered:

* Redis caching for frequently accessed URLs
* URL expiration
* Custom short aliases
* Click and usage analytics
* Rate limiting
* Authentication and authorization
* Database migrations using Alembic
* Automated unit and integration tests
* Docker containerization
* HTTPS and production deployment

These features are outside the scope of this basic assessment.

## Conclusion

This project demonstrates a basic RESTful URL Shortener API using **FastAPI and PostgreSQL**.

It implements URL validation, UUID-based database identification, unique short-code generation, collision checking, PostgreSQL persistence, and HTTP redirection while maintaining a clean separation between API routes, validation, database models, and CRUD operations.
