import os

# --- db configuration
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = int(os.environ.get('DB_PORT', 27017))

# --- swagger configuration
SWAGGER_URL = '/swagger'
API_SCHEMA_URL = '/api_schema'

