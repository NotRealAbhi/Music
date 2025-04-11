from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message):
    user_name = message.from_user.first_name if message.from_user else "User"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎶 Play Music", callback_data="play_menu"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help_menu"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_menu"),
            ],
        ]
    )
    await message.reply_text(
        f"Hello {user_name}! 👋\n\nWelcome to the Music Bot!\n\nUse the buttons below to explore the bot's features.",
        reply_markup=reply_markup
    )

# Example callback query handlers (you'll need to implement the logic for these)
@Client.on_callback_query(filters.regex("^play_menu$"))
async def play_menu_callback(client: Client, callback_query):
    await callback_query.answer()
    await callback_query.message.edit_text("🎵 Play Music Menu:\n\nUse /play <song name or URL> to start playing.", reply_markup=None)

@Client.on_callback_query(filters.regex("^settings_menu$"))
async def settings_menu_callback(client: Client, callback_query):
    await callback_query.answer()
    await callback_query.message.edit_text("⚙️ Settings Menu:\n\n(Settings options will be added here)", reply_markup=None)

@Client.on_callback_query(filters.regex("^help_menu$"))
async def help_menu_callback(client: Client, callback_query):
    await callback_query.answer()
    help_text = "❓ Help Menu:\n\nAvailable commands:\n"
    help_text += "/play <song> - Play a song.\n"
    help_text += "/queue - View the current queue.\n"
    help_text += "/skip - Skip the current song.\n"
    help_text += "/stop - Stop playback and clear the queue.\n"
    # Add more commands as you implement them
    await callback_query.message.edit_text(help_text, reply_markup=None)

@Client.on_callback_query(filters.regex("^about_menu$"))
async def about_menu_callback(client: Client, callback_query):
    await callback_query.answer()
    about_text = "ℹ️ About Music Bot:\n\nThis bot is created using Pyrogram and Pytgcalls.\n\nCreator: Your Name/Username\nVersion: 1.0 (or your version)"
    await callback_query.message.edit_text(about_text, reply_markup=None)
