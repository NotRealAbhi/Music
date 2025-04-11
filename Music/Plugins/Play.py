from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Main import voice_chat_manager  # Import the initialized instance

@Client.on_message(filters.command(["play", "p"]) & filters.group)
async def play_command(client: Client, message):
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or URL to play.")
        return

    query = " ".join(message.command[1:])
    reply = await voice_chat_manager.enqueue(message.chat.id, query, message.from_user.mention)
    await message.reply_text(reply)
    if not voice_chat_manager.get_now_playing(message.chat.id):
        await voice_chat_manager.play_next(message.chat.id)

@Client.on_message(filters.command(["forceplay", "fp"]) & filters.group)
async def force_play_command(client: Client, message):
    if voice_chat_manager is None:
        await message.reply_text("Voice chat manager not initialized yet.")
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or URL to force play.")
        return

    query = " ".join(message.command[1:])
    await voice_chat_manager.stop(message.chat.id)
    reply = await voice_chat_manager.enqueue(message.chat.id, query, message.from_user.mention)
    await message.reply_text(reply)
    await voice_chat_manager.play_next(message.chat.id)

# Implement inline play logic here if needed
