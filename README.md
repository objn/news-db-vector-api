# NEWS-DB-VECTOR-API

A FastAPI application for news embedding generation and similarity search using Google's Gemini AI and PostgreSQL with pgvector extension.

## Features

- 🚀 **News Embedding Generation** - Generate embeddings using Google's text-embedding-004 model
- 🔍 **Semantic Similarity Search** - Find similar news articles using cosine similarity
- 📊 **Batch Processing** - Generate embeddings for multiple news items at once
- 🐳 **Docker Support** - Containerized deployment with Docker and Docker Compose
- 📦 **PostgreSQL with pgvector** - Vector similarity search in database
- 🔒 **Production Ready** - Security best practices, health checks, and error handling

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Setup and Run

1. **Clone the repository** (if not already done)

2. **Configure environment variables:**
```cmd
copy .env.example .env
```

Edit `.env` file with your actual values:
```env
NODE_ENV=production
DATABASE_URL=postgresql://postgres:your_password@postgres:5432/news_db
POSTGRES_PASSWORD=your_secure_password
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Start the application:**
```cmd
docker-compose up -d
```

4. **Check if services are running:**
```cmd
docker-compose ps
docker-compose logs -f api
```

5. **Access the API:**
- API: http://localhost:8000
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

### Docker Commands

**Stop services:**
```cmd
docker-compose down
```

**Rebuild after code changes:**
```cmd
docker-compose up -d --build
```

**View logs:**
```cmd
docker-compose logs -f api
docker-compose logs -f postgres
```

**Restart services:**
```cmd
docker-compose restart
```

**Remove all (including volumes):**
```cmd
docker-compose down -v
```

## Jenkins/CI-CD Deployment

For production deployment with Jenkins, see the complete guide: **[JENKINS_DEPLOYMENT.md](JENKINS_DEPLOYMENT.md)**

### Quick Jenkins Deployment

**Using deployment scripts:**
```cmd
REM Windows
deploy.bat

REM Linux/Mac
chmod +x deploy.sh
./deploy.sh
```

**Using Docker Compose (Production):**
```cmd
docker-compose -f docker-compose.prod.yml up -d
```

The deployment scripts automatically:
- ✅ Create `.env` from environment variables or Jenkins credentials
- ✅ Build Docker image with proper tagging
- ✅ Mount `.env` file as volume for runtime configuration
- ✅ Deploy with health checks
- ✅ Verify deployment success

See **[JENKINS_DEPLOYMENT.md](JENKINS_DEPLOYMENT.md)** for:
- Complete Jenkinsfile pipeline
- Troubleshooting .env detection issues
- Volume mounting strategies
- Environment variable handling
- Best practices for CI/CD

## Local Development Setup (Without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL with pgvector extension
- Google Gemini API key

### Setup

1. **Create and activate virtual environment:**
```cmd
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

3. **Configure environment variables:**
```cmd
copy .env.example .env
```

Edit `.env` with your database and API credentials.

4. **Setup database:**
```cmd
REM Run the SQL setup script in your PostgreSQL database
psql -U postgres -d news_db -f PGVECTOR_SETUP.sql
```

### Running the Application

**Development Mode (with auto-reload):**
```cmd
uvicorn main:app --reload
```

**Production Mode:**
```cmd
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Run directly with Python:**
```cmd
python main.py
```

## API Endpoints

### Health & Info
- `GET /` - Root endpoint, welcome message
- `GET /health` - Health check endpoint
- `GET /config` - Get current configuration (sanitized)
- `GET /db/test` - Test database connection

### Embedding Generation
- `POST /news-embedding` - Generate embedding from text
  ```json
  {
    "news_desc": "Your news text here"
  }
  ```

- `POST /news-embedding-id/` - Generate and save embedding by news ID
  ```json
  {
    "news_id": "news_id_here"
  }
  ```

- `POST /news-embedding/batch/all` - Generate embeddings for all news without embeddings

### Similarity Search
- `POST /news-similarity-compare` - Compare embeddings and find similar news
  ```json
  {
    "news_desc": "Text to find similar news",
    "embedding": "",  // Optional: provide pre-computed embedding
    "threshold": 0.7,  // Minimum similarity score (0-1)
    "top_k": 10  // Number of results to return
  }
  ```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
NEWS-DB-VECTOR-API/
├── main.py                 # FastAPI application and routes
├── config.py              # Configuration and environment variables
├── database.py            # Database connection and session management
├── models.py              # SQLAlchemy models
├── embedding_service.py   # Google Gemini embedding service
├── request_class.py       # Pydantic request/response models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker build context exclusions
├── .env.example          # Environment variables template
├── PGVECTOR_SETUP.sql    # PostgreSQL pgvector setup script
└── README.md             # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GEMINI_API_KEY` | Google Gemini API key for embeddings | Yes |
| `NODE_ENV` | Environment (development/production) | No (default: development) |
| `POSTGRES_DB` | PostgreSQL database name (Docker only) | No (default: news_db) |
| `POSTGRES_USER` | PostgreSQL user (Docker only) | No (default: postgres) |
| `POSTGRES_PASSWORD` | PostgreSQL password (Docker only) | Yes (for Docker) |

## Technologies

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Powerful relational database
- **pgvector** - PostgreSQL extension for vector similarity search
- **Google Gemini AI** - text-embedding-004 model for embeddings
- **Pydantic** - Data validation using Python type annotations
- **Docker** - Containerization platform

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
