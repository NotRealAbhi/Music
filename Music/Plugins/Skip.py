from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager
from Main import voice_chat_manager  # Import the initialized instance

@Client.on_message(filters.command(["skip", "n"]) & filters.group)
async def skip_command(client: Client, message):
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    reply = await voice_chat_manager.skip(message.chat.id)
    await message.reply_text(reply)
