# Snowflake FastAPI MCP Server

A FastAPI server that provides Snowflake database access via MCP protocol. This project integrates with the `fastapi-mcp` library to expose Snowflake database operations through structured endpoints.

## Features

### Available MCP Tools

- **list_databases** - List all databases in the Snowflake instance
- **list_tables** - List all tables within a specific database and schema
- **execute_read_query** - Execute SELECT queries to read data from the database

## Getting Started

### Prerequisites
- Python 3.12+
- Snowflake account and credentials
- Docker and Docker Compose (optional)

### Local Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd snowflake-fastapi-mcp
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

3. Copy the environment template and update with your Snowflake credentials:
   ```bash
   cp env.example .env
   ```

4. Edit the `.env` file with your Snowflake account details:
   ```
   SNOWFLAKE_ACCOUNT=your_account_id
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   SNOWFLAKE_ROLE=your_role
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

   The server will be available at http://localhost:8008

### Running with Docker

You can also run the application using Docker:

#### Using Docker Compose

Build and start the container:

```bash
docker compose up --build
```

The server will be available at http://localhost:8008

#### Using Docker Directly

1. Build the Docker image:
   ```bash
   docker build -t snowflake-mcp-server .
   ```

2. Run the container:
   ```bash
   docker run -p 8008:8008 --env-file .env snowflake-mcp-server
   ```

## MCP Protocol

This server implements the MCP (Managed Chat Protocol) specification, which allows it to be used with various MCP-compatible clients. The MCP endpoint is available at:

```
http://localhost:8008/mcp
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8008/docs
- ReDoc: http://localhost:8008/redoc

## Configuration Options

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| SNOWFLAKE_ACCOUNT | Your Snowflake account identifier | - |
| SNOWFLAKE_USER | Snowflake username | - |
| SNOWFLAKE_PASSWORD | Snowflake password | - |
| SNOWFLAKE_WAREHOUSE | Default warehouse to use | - |
| SNOWFLAKE_DATABASE | Default database to use | - |
| SNOWFLAKE_SCHEMA | Default schema to use | - |
| SNOWFLAKE_ROLE | Role to assume when connecting | - |
| PORT | Server port | 8008 |
| HOST | Server host | 0.0.0.0 |
| LOG_LEVEL | Logging level (INFO, DEBUG, etc.) | INFO |

## Architecture

The application is structured as follows:

- `app/api/routes/` - Contains API route definitions
  - `query.py` - Endpoints for executing queries
  - `schema.py` - Endpoints for database schema operations
- `app/services/` - Service layer
  - `snowflake.py` - Service for Snowflake database operations
- `app/core/` - Core application modules
  - `config.py` - Configuration settings
  - `logging.py` - Logging setup

## Timeouts and Connection Settings

The Snowflake connection is configured with the following timeout settings:

- `login_timeout`: 60 seconds
- `network_timeout`: 60 seconds
- `socket_timeout`: 60 seconds

The MCP server is configured with a timeout of 180 seconds for API requests.

## Troubleshooting

- **Connection Timeout Issues**: If you experience timeout issues with API requests, you may need to adjust the timeout values in `app/main.py` and `app/services/snowflake.py`.

- **Container Logs**: View logs with `docker compose logs` or `docker logs <container-id>`.

- **Database Connectivity**: Ensure your Snowflake credentials are correct and that your network allows connections to Snowflake.

## License

[MIT License](LICENSE) 