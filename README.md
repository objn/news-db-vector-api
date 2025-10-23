# NEWS-DB-VECTOR-API

A FastAPI application for news embedding generation and semantic similarity search using Google's Generative AI (text-embedding-004) and PostgreSQL with pgvector extension.

## Features

- 🚀 **News Embedding Generation** - Generate vector embeddings from news descriptions using Google's text-embedding-004 model
- 🔍 **Semantic Similarity Search** - Find similar news articles using cosine similarity
- 📦 **Batch Processing** - Generate embeddings for multiple news items at once
- 🐳 **Docker Ready** - Complete Docker and Docker Compose setup
- 🗄️ **PostgreSQL + pgvector** - Vector database support for efficient similarity search
- 📊 **Health Monitoring** - Built-in health check endpoints

## Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension
- Google Gemini API Key
- Docker & Docker Compose (for containerized deployment)

## Quick Start with Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/objn/news-db-vector-api.git
cd news-db-vector-api
```

2. **Set up environment variables**
```bash
copy .env.example .env
```
Edit `.env` with your configuration:
```env
NODE_ENV=production
DATABASE_URL=postgresql://postgres:your_password@postgres:5432/news_db
POSTGRES_DB=news_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Check the logs**
```bash
docker-compose logs -f api
```

The API will be available at `http://localhost:8000`

### Docker Commands

```bash
# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View running containers
docker-compose ps

# Access API container shell
docker-compose exec api bash

# View PostgreSQL logs
docker-compose logs -f postgres
```

## Local Development Setup

1. **Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
copy .env.example .env
```
Edit `.env` with your local database configuration.

4. **Run database migrations** (if applicable)
```bash
alembic upgrade head
```

5. **Start the development server**
```bash
# Development mode (with auto-reload)
uvicorn main:app --reload

# Or run directly
python main.py
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### General

- `GET /` - Root endpoint, welcome message
- `GET /health` - Health check endpoint
- `GET /config` - Get current configuration (sanitized)
- `GET /db/test` - Test database connection

### Embedding Generation

- `POST /news-embedding` - Generate embedding from text
  ```json
  {
    "news_desc": "Your news description text here"
  }
  ```

- `POST /news-embedding-id/` - Generate and save embedding for a specific news ID
  ```json
  {
    "news_id": "NEWS123"
  }
  ```

- `POST /news-embedding/batch/all` - Generate embeddings for all news without embeddings

### Similarity Search

- `POST /news-similarity-compare` - Compare embeddings and find similar news
  ```json
  {
    "news_desc": "Search query text",
    "embedding": "[optional embedding array]",
    "threshold": 0.7,
    "top_k": 10
  }
  ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GEMINI_API_KEY` | Google Gemini API key for embeddings | Yes |
| `NODE_ENV` | Environment (development/production) | No (default: development) |
| `POSTGRES_DB` | PostgreSQL database name (Docker only) | Yes (Docker) |
| `POSTGRES_USER` | PostgreSQL username (Docker only) | Yes (Docker) |
| `POSTGRES_PASSWORD` | PostgreSQL password (Docker only) | Yes (Docker) |

## Database Setup

The application requires PostgreSQL with the pgvector extension. See `PGVECTOR_SETUP.sql` for the database schema.

When using Docker Compose, the database is automatically set up with pgvector.

For manual setup:
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE news_db;

# Enable pgvector extension
\c news_db
CREATE EXTENSION vector;

# Run the setup script
\i PGVECTOR_SETUP.sql
```

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server implementation
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **pgvector** - Vector similarity search extension
- **Google Generative AI** - Text embedding model (text-embedding-004)
- **Pydantic** - Data validation using Python type annotations
- **Docker** - Containerization platform

## Project Structure

```
NEWS-DB-VECTOR-API/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment variables
├── database.py            # Database connection and session management
├── models.py              # SQLAlchemy models
├── embedding_service.py   # Embedding generation and similarity logic
├── request_class.py       # Pydantic request/response models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose orchestration
├── .dockerignore         # Docker build context exclusions
├── .env.example          # Environment variables template
├── PGVECTOR_SETUP.sql    # Database schema and setup
└── README.md             # This file
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

## Production Deployment

### Using Docker

1. Build the image:
```bash
docker build -t news-db-vector-api:latest .
```

2. Run the container:
```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name news-vector-api \
  news-db-vector-api:latest
```

### Using Docker Compose

Simply use the provided `docker-compose.yml`:
```bash
docker-compose up -d
```

## Health Checks

The application includes built-in health checks:

- **HTTP**: `GET /health`
- **Docker**: Automatic health check configured in Dockerfile
- **Docker Compose**: Health check with dependency management

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres

# Test connection manually
docker-compose exec postgres psql -U postgres -d news_db
```

### API Container Issues
```bash
# View API logs
docker-compose logs api

# Restart API service
docker-compose restart api

# Rebuild and restart
docker-compose up -d --build api
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Contact

[Add contact information here]
