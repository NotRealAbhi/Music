from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager
from Main import voice_chat_manager  # Import the initialized instance

@Client.on_message(filters.command(["queue", "q"]) & filters.group)
async def queue_command(client: Client, message):
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    queue = voice_chat_manager.get_queue(message.chat.id)
    if not queue:
        await message.reply_text("The queue is empty.")
        return

    queue_list = [f"{i+1}. {item['title']} (requested by {item['requested_by']})" for i, item in enumerate(queue)]
    await message.reply_text("Current Queue:\n" + "\n".join(queue_list))

# Implement /remove, /skipto commands here
