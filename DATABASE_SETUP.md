# Database Setup Guide

## Auto-Generate Models from Database

This project includes tools to automatically pull your database schema and create SQLAlchemy models.

## Quick Start

### 1. Generate Models from Your Database

Run the model generator script:

```bash
python generate_models.py
```

This will:
- ✅ Connect to your PostgreSQL database
- ✅ Introspect all tables and columns
- ✅ Generate a `models.py` file with SQLAlchemy model classes
- ✅ Show you the database structure

### 2. What Gets Generated

The script creates:
- **models.py** - Complete SQLAlchemy models for all your tables
- Each table becomes a Python class
- All columns, types, and constraints are automatically mapped

### Example Output

```
📋 Table: users
   Columns:
     - id: INTEGER NOT NULL PRIMARY KEY
     - username: VARCHAR(50) NOT NULL
     - email: VARCHAR(100) NOT NULL
     - created_at: TIMESTAMP
```

## Using Generated Models

### Import Models
```python
from models import Users, Posts  # Your generated classes
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
```

### Example Endpoint
```python
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users
```

## Database Configuration

Your database connection is configured in `.env`:
```
DATABASE_URL=postgresql://postgres:password@host:port/database
```

## Test Database Connection

Visit: `http://localhost:9099/db/test`

Or the startup log will show:
```
✓ Database connection successful!
```

## Manual Model Editing

After generation, you can customize `models.py`:
- Add relationships
- Add methods
- Add custom validations
- Modify field types if needed

## Alembic Migrations (Optional)

If you want to manage schema changes:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Troubleshooting

**Connection Failed?**
- Check your DATABASE_URL in `.env`
- Ensure PostgreSQL is running
- Verify host, port, username, and password

**Models Not Found?**
- Make sure you ran `python generate_models.py` first
- Check that `models.py` was created

**Import Errors?**
- Install dependencies: `pip install -r requirements.txt`
