import os

OWNER_ID = int(os.environ.get("OWNER_ID", 12345))  # Replace with your Telegram ID
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS", "12345 67890").split()))
API_ID = int(os.environ.get("TELEGRAM_API_ID", 12345))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "YOUR_MONGO_DB_URI") # If using MongoDB
