import snowflake.connector
from typing import Dict, Any, Tuple, List
import uuid
from ..core.logging import logger
from ..core.config import settings

class SnowflakeService:
    def __init__(self):
        self.session = None
        
        self.config = {
            "account": settings.SNOWFLAKE_ACCOUNT, 
            "user": settings.SNOWFLAKE_USER,
            "password": settings.SNOWFLAKE_PASSWORD,
            "warehouse": settings.SNOWFLAKE_WAREHOUSE,
            "database": settings.SNOWFLAKE_DATABASE,
            "schema": settings.SNOWFLAKE_SCHEMA,
            "role": settings.SNOWFLAKE_ROLE,
            "login_timeout": 60,
            "network_timeout": 60,
            "socket_timeout": 60,
            "client_session_keep_alive": True,
            "client_session_keep_alive_heartbeat_frequency": 3600
        }
        self._insights = []
        logger.debug(f"Initialized Snowflake config with account: {self.config['account']}")

    def start_init_connection(self):
        """Initialize connection to Snowflake"""
        try:
            logger.info("Connecting to Snowflake...")
            logger.debug(f"Using account: {self.config['account']}")
            self.session = snowflake.connector.connect(**self.config)
            logger.info("Successfully connected to Snowflake")
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake database: {e}")
            raise

    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], str]:
        """Execute a query and return results"""
        if not self.session:
            self.start_init_connection()

        try:
            logger.debug(f"Executing query: {query}")
            cursor = self.session.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [col[0] for col in cursor.description] if cursor.description else []
            
            # Convert results to list of dicts
            results = []
            for row in cursor:
                results.append(dict(zip(columns, row)))
            
            data_id = str(uuid.uuid4())
            logger.info(f"Query executed successfully. Data ID: {data_id}")
            
            return results, data_id
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def add_insight(self, insight: str):
        """Add a new insight to the memo"""
        self._insights.append(insight)
        logger.info(f"Added new insight: {insight}")

    def get_memo(self) -> str:
        """Get all insights as a formatted memo"""
        return "\n".join([f"- {insight}" for insight in self._insights])

# Create a global instance
snowflake_service = SnowflakeService() 