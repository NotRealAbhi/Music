import asyncio
import logging
import os
from dotenv import load_dotenv
from pyrogram import Client
from Music.Call.Calls import CallHandler
from Music.Call.Core import VoiceChatManager

load_dotenv()

API_ID = int(os.environ.get("TELEGRAM_API_ID", 25024171))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7889585262:AAG99xMVwF163xHxeOV4Tqug1Xfe_BWiFZw")
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", -1002678147540)  # Replace with your log group ID

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

if not API_ID or not API_HASH or not BOT_TOKEN:
    LOGGER.error("TELEGRAM_API_ID, TELEGRAM_API_HASH, or TELEGRAM_BOT_TOKEN not set.")
    exit()

bot = Client(
    "MusicUserBot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Music/Plugins")
)

call_handler = None
voice_chat_manager = None

async def send_startup_message():
    try:
        await bot.send_message(LOG_GROUP_ID, "✅ Bot started successfully!")
        LOGGER.info(f"Startup message sent to log group: {LOG_GROUP_ID}")
    except Exception as e:
        LOGGER.error(f"Failed to send startup message to log group {LOG_GROUP_ID}: {e}")

async def main():
    global call_handler, voice_chat_manager
    LOGGER.info("Starting Music User Bot...")
    await bot.start()
    LOGGER.info("Pyrogram client started.")
    call_handler = CallHandler(bot)
    await call_handler.start()
    LOGGER.info("PyTgCalls started.")
    voice_chat_manager = VoiceChatManager(call_handler)
    LOGGER.info("Voice Chat Manager initialized.")
    await send_startup_message()
    LOGGER.info("Music User Bot has started and startup message sent!")
    await asyncio.sleep(float('inf'))

if __name__ == "__main__":
    asyncio.run(main())
