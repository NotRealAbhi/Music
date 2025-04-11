from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager
from Main import voice_chat_manager  # Import the initialized instance
from pytgcalls.types import AudioPiped

@Client.on_message(filters.command("radio") & filters.group)
async def radio_command(client: Client, message):
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide a radio URL.")
        return

    radio_url = message.command[1]
    await voice_chat_manager.stop(message.chat.id) # Stop any existing playback
    await voice_chat_manager.call_handler.join_call(message.chat.id)
    await voice_chat_manager.call_handler.play_media(message.chat.id, AudioPiped(radio_url))
    await message.reply_text(f"Playing radio stream from: {radio_url}")

@Client.on_message(filters.command("stopradio") & filters.group)
async def stop_radio_command(client: Client, message):
    global voice_chat_manager
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    await voice_chat_manager.stop(message.chat.id)
    await message.reply_text("Radio stream stopped.")
