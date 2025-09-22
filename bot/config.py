from dotenv import load_dotenv
import os

# load enivonment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPERADMIN = int(os.getenv('SUPERADMIN'))
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')