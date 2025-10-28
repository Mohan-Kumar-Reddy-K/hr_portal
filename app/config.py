import os # to read environment variables stored in the OS.
from pydantic import BaseModel # validates data automatically and provides helpful error messages
from dotenv import load_dotenv # loads environment variables from a .env file into the system environment

load_dotenv() # Loads .env variables into system environment (so os.getenv() can read them)

class Settings(BaseModel):
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017") # reads the environment variable
    MONGODB_DB: str = os.getenv("MONGODB_DB", "resume_portal")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

settings = Settings()
