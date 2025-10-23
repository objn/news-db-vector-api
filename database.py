from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create database engine with proper encoding
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.NODE_ENV == "development",  # Log SQL queries in development
    pool_pre_ping=True,  # Test connection before using
    pool_size=5,
    max_overflow=10,
    connect_args={
        "client_encoding": "utf8"
    }
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Metadata for reflection
metadata = MetaData()


def get_db():
    """
    Dependency function to get database session.
    Use this in FastAPI endpoints with Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            print("✓ Database connection successful!")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
