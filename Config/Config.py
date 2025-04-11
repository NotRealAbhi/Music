import os

OWNER_ID = int(os.environ.get("OWNER_ID", 12345))  # Replace with your Telegram ID
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS", "12345 67890").split()))
API_ID = int(os.environ.get("TELEGRAM_API_ID", 25024171))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7889585262:AAG99xMVwF163xHxeOV4Tqug1Xfe_BWiFZw")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "YOUR_MONGO_DB_URI") # If using MongoDB
