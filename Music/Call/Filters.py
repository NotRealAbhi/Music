# You can define custom filters related to voice chat state here if needed
# For example, a filter to check if the bot is currently playing in a chat.
from pyrogram import filters

def is_playing(func):
    async def wrapper(client, message):
        from main import voice_chat_manager
        if voice_chat_manager and voice_chat_manager.get_now_playing(message.chat.id):
            return await func(client, message)
        else:
            await message.reply_text("Nothing is currently playing.")
            return
    return wrapper
