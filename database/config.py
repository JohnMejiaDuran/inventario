import os

# Database configuration
DATABASE_URL = 'sqlite:///data/inventory.db'

# Application configuration
APP_NAME = "Inventory System"
DEBUG = True

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Create required directories
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)