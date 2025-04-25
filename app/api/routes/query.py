from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from ...services.snowflake import snowflake_service
from ...core.logging import logger

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/read", operation_id="execute_read_query")
async def read_query(query: str) -> Dict[str, Any]:
    """
    Execute a SELECT query on the Snowflake database
    
    Args:
        query: The SELECT SQL query to execute
    
    Returns:
        Query results as array of objects
    """
    logger.info(f"Executing read query: {query}")
    try:
        data, data_id = await snowflake_service.execute_query(query)
        return {
            "type": "data",
            "data_id": data_id,
            "data": data,
        }
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing query: {str(e)}"
        ) 