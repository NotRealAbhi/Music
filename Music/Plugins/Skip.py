from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager
from Main import voice_chat_manager  # Import the initialized instance

@Client.on_message(filters.command(["skip", "n"]) & filters.group)
async def skip_command(client: Client, message):
    global voice_chat_manager
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    if voice_chat_manager.queue.get(message.chat.id):
        next_track = voice_chat_manager.queue[message.chat.id][0]
        await message.reply_text(f"Skipping to: {next_track['title']}")
        await voice_chat_manager.call_handler.play_audio(
            message.chat.id,
            next_track['path'],
            next_track['title']
        )
        if voice_chat_manager.queue.get(message.chat.id):
            voice_chat_manager.queue[message.chat.id].pop(0) # Remove the skipped song
    else:
        await message.reply_text("Queue is empty, nothing to skip to.")
