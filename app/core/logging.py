import logging
from .config import settings

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
    )
    
    # Create logger
    logger = logging.getLogger("snowflake-mcp-server")
    return logger

logger = setup_logging() 