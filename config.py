import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    NODE_ENV: str = os.getenv("NODE_ENV", "development")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    def __init__(self):
        print("✓ Environment variables loaded:")
        print(f"  - DATABASE_URL: {'*' * 20 if self.DATABASE_URL else 'Not set'}")
        print(f"  - NODE_ENV: {self.NODE_ENV}")
        print(f"  - GEMINI_API_KEY: {'*' * 20 if self.GEMINI_API_KEY else 'Not set'}")


# Create a global settings instance
settings = Settings()
