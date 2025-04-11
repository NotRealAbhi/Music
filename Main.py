import logging
import time
from pyrogram import Client
from Config.Config import API_ID, API_HASH, BOT_TOKEN
from Music.Call.Calls import CallHandler
from Music.Call.Core import VoiceChatManager

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

call_handler = None
voice_chat_manager = None

bot = Client(
    "Music",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Music/Plugins")
)

if __name__ == "__main__":
    LOGGER.info("Starting Music User Bot...")
    bot.start()

    call_handler = CallHandler(bot)
    bot.loop.run_until_complete(call_handler.start())

    voice_chat_manager = VoiceChatManager(call_handler)
    LOGGER.info("Music User Bot has started!")

    # Keeps the script running like idle()
    try:
        while True:
            time.sleep(86400)  # Sleep for a day in each loop
    except KeyboardInterrupt:
        LOGGER.info("Stopping Music User Bot...")
        bot.stop()
