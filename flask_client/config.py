import os
from dotenv import load_dotenv

# Load environment variables from the .env file securely
load_dotenv()

class Config:
    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5001")
    DATABASE_URL = os.getenv("DATABASE_URL")  # No default here to enforce its presence in the .env

# Raise an exception if DATABASE_URL is not set
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set in the .env file")

    DEFAULT_API_VERSION = os.getenv("DEFAULT_API_VERSION", "v2")