import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")
print(f"Python path: {sys.path}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

# Change relative imports to absolute imports
from app.core.config import settings
from app.core.logging import logger
from app.services.snowflake import snowflake_service
from app.api.routes import query, schema

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router)
app.include_router(schema.router)

# Initialize and mount FastAPI MCP
logger.info("Initializing FastAPI MCP")
mcp = FastApiMCP(
    app,
    name=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
)
logger.info("Mounting MCP server")
mcp.mount()
logger.info("MCP server mounted successfully")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    """Initialize connection to Snowflake on startup"""
    logger.info("Application startup event triggered")
    logger.info("Initializing connection to Snowflake")
    snowflake_service.start_init_connection()
    logger.info("Snowflake connection initialization completed")

@app.on_event("shutdown")
async def shutdown_event():
    """Close connection to Snowflake on shutdown"""
    logger.info("Application shutdown event triggered")
    logger.info("Closing connection to Snowflake")
    if snowflake_service.session:
        snowflake_service.session.close()
        logger.info("Snowflake connection closed successfully")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server")
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    ) 