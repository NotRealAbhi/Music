from pyrogram import Client, filters
from Music.Call.Core import VoiceChatManager

voice_chat_manager = None # Initialize in main

@Client.on_message(filters.command(["volume", "vol"]) & filters.group)
async def volume_command(client: Client, message):
    global voice_chat_manager
    if voice_chat_manager is None:
        from Main import voice_chat_manager

    if len(message.command) < 2:
        await message.reply_text("Please provide a volume level (0-100).")
        return

    try:
        level = int(message.command[1])
        if 0 <= level <= 100:
            reply = await voice_chat_manager.volume(message.chat.id, level)
            await message.reply_text(reply)
        else:
            await message.reply_text("Volume level must be between 0 and 100.")
    except ValueError:
        await message.reply_text("Invalid volume level.")

@Client.on_message(filters.command(["mute"]) & filters.group)
async def mute_command(client: Client, message):
    global voice_chat_manager
    if voice_chat_manager is None:
        from Main import voice_chat_manager

    await voice_chat_manager.volume(message.chat.id, 0)
    await message.reply_text("Muted.")

@Client.on_message(filters.command(["unmute"]) & filters.group)
async def unmute_command(client: Client, message):
    global voice_chat_manager
    if voice_chat_manager is None:
        from Main import voice_chat_manager

    await voice_chat_manager.volume(message.chat.id, 100) # Or a default volume
    await message.reply_text("Unmuted.")
