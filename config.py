import os
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env from multiple locations for Jenkins/Docker compatibility
env_locations = [
    Path(__file__).parent / '.env',  # Same directory as config.py
    Path('/app/.env'),                # Docker volume mount location
    Path.cwd() / '.env',              # Current working directory
]

env_loaded = False
for env_path in env_locations:
    if env_path.exists():
        print(f"✓ Loading .env from: {env_path}")
        load_dotenv(dotenv_path=env_path, override=True)
        env_loaded = True
        break

if not env_loaded:
    print("⚠ No .env file found, using environment variables only")
    load_dotenv()  # Try to load from default location anyway


class Settings:
    """Application settings loaded from environment variables"""
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    NODE_ENV: str = os.getenv("NODE_ENV", "development")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    STARTUP_API_PATH: str = os.getenv("STARTUP_API_PATH", "/api/v1/news/vec")
    
    def __init__(self):
        print("\n" + "="*50)
        print("✓ Environment variables loaded:")
        print(f"  - DATABASE_URL: {'✓ Set (' + '*' * 20 + ')' if self.DATABASE_URL else '✗ Not set'}")
        print(f"  - NODE_ENV: {self.NODE_ENV}")
        print(f"  - GEMINI_API_KEY: {'✓ Set (' + '*' * 20 + ')' if self.GEMINI_API_KEY else '✗ Not set'}")
        print("="*50 + "\n")


# Create a global settings instance
settings = Settings()
