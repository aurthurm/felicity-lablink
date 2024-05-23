import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = f"{BASE_DIR}/public/"

# DATABASE
DB_NAME = "astm_results" 
DB_USER = "nmrl"
DB_PASSWORD =  "password"
DB_HOST = "localhost:3306"

# SENAITE.JSONAPI
SEND_TO_QUEUE = False


