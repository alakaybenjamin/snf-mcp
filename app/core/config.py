from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Snowflake MCP Server"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A FastAPI server that provides Snowflake database access via MCP"
    DEBUG: bool = True

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8008
    
    # Snowflake settings
    SNOWFLAKE_ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT", "").strip()
    SNOWFLAKE_USER: str = os.getenv("SNOWFLAKE_USER", "").strip()
    SNOWFLAKE_PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD", "").strip()
    SNOWFLAKE_WAREHOUSE: str = os.getenv("SNOWFLAKE_WAREHOUSE", "").strip()
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "").strip()
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "").strip()
    SNOWFLAKE_ROLE: str = os.getenv("SNOWFLAKE_ROLE", "").strip()

    print(f"**************** - {SNOWFLAKE_ACCOUNT}")
    print(f"**************** - {SNOWFLAKE_USER}")
    print(f"**************** - {SNOWFLAKE_PASSWORD}")
    print(f"**************** - {SNOWFLAKE_WAREHOUSE}")
    print(f"**************** - {SNOWFLAKE_DATABASE}")
    print(f"**************** - {SNOWFLAKE_SCHEMA}")
    print(f"**************** - {SNOWFLAKE_ROLE}")

    class Config:
        case_sensitive = True

settings = Settings() 