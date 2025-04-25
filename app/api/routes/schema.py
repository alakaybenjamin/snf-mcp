from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from ...services.snowflake import snowflake_service
from ...core.logging import logger

router = APIRouter(prefix="/schema", tags=["Schema"])

@router.get("/databases", operation_id="list_databases")
async def list_databases() -> Dict[str, Any]:
    """
    List all databases in the Snowflake instance
    
    Returns:
        Array of database names
    """
    logger.info("Listing databases")
    try:
        query = "SELECT DATABASE_NAME FROM INFORMATION_SCHEMA.DATABASES"
        data, data_id = await snowflake_service.execute_query(query)
        return {
            "type": "data",
            "data_id": data_id,
            "data": data,
        }
    except Exception as e:
        logger.error(f"Error listing databases: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing databases: {str(e)}"
        )

@router.get("/tables/{database}/{schema}", operation_id="list_tables")
async def list_tables(database: str, schema: str) -> Dict[str, Any]:
    """
    List all tables within a specific database and schema
    
    Args:
        database: Name of the database
        schema: Name of the schema
    
    Returns:
        Array of table metadata
    """
    logger.info(f"Listing tables for database: {database}, schema: {schema}")
    try:
        query = f"""
            SELECT table_catalog, table_schema, table_name, comment 
            FROM {database}.information_schema.tables 
            WHERE table_schema = '{schema.upper()}'
        """
        data, data_id = await snowflake_service.execute_query(query)
        return {
            "type": "data",
            "data_id": data_id,
            "database": database,
            "schema": schema,
            "data": data,
        }
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tables: {str(e)}"
        ) 