import asyncio
import logging
from pyrogram import Client
from Config.Config import API_ID, API_HASH, BOT_TOKEN
from Call.Calls import CallHandler
from Call.Core import VoiceChatManager

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

bot = Client(
    "MusicUserBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Music/Plugins")
)

call_handler = None
voice_chat_manager = None

async def main():
    global call_handler, voice_chat_manager
    LOGGER.info("Starting Music User Bot...")
    await bot.start()
    call_handler = CallHandler(bot)
    await call_handler.start()
    voice_chat_manager = VoiceChatManager(call_handler)
    LOGGER.info("Music User Bot has started!")
    await asyncio.sleep(float('inf'))

if __name__ == "__main__":
    asyncio.run(main())
