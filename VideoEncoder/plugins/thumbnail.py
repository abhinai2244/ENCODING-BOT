from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from ..utils.database.access_db import db
import logging

@Client.on_message(filters.command("thumb"))
async def thumb_command(client, message):
    try:
        user_id = message.from_user.id
        thumbnail = await db.get_thumbnail(user_id)
        buttons = [
            [
                InlineKeyboardButton("Set/Replace Thumbnail", callback_data="set_thumb"),
                InlineKeyboardButton("Delete Thumbnail", callback_data="del_thumb")
            ]
        ]
        if thumbnail:
            await message.reply_photo(
                photo=thumbnail,
                caption="Your current custom thumbnail.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await message.reply_text(
                "You don't have a custom thumbnail set.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    except Exception as e:
        logging.error(f"Error in thumb_command: {e}")
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    """
    Single callback handler that processes both set_thumb and del_thumb
    Using the same logic pattern for both actions
    """
    data = query.data
    user_id = query.from_user.id
    
    try:
        if data == "set_thumb":
            # Same logic as set_thumb: Just prompt the user to send a photo
            await query.answer("Please send a photo now", show_alert=False)
            await query.message.edit_text(
                "Send me a photo to set as your custom thumbnail."
            )
            
        elif data == "del_thumb":
            # Same logic pattern: Direct action with confirmation
            await db.set_thumbnail(user_id, None)
            await query.answer("Thumbnail deleted!", show_alert=True)
            await query.message.delete()
            
    except Exception as e:
        logging.error(f"Error in cb_handler for {data}: {e}")
        try:
            await query.answer(f"Error: {str(e)}", show_alert=True)
        except:
            pass

@Client.on_message(filters.photo & filters.private)
async def save_thumb(client, message):
    """
    Handles photo uploads for setting thumbnails
    This connects with the set_thumb callback through message reply checking
    """
    try:
        user_id = message.from_user.id
        file_id = message.photo.file_id
        
        # Method 1: Photo sent with /thumb or /setthumb caption
        if message.caption and (message.caption == "/thumb" or message.caption == "/setthumb"):
            await db.set_thumbnail(user_id, file_id)
            await message.reply_text("✅ Custom thumbnail saved!")
            
        # Method 2: Photo sent as a reply to the prompt message (connects to set_thumb callback)
        elif message.reply_to_message and message.reply_to_message.text == "Send me a photo to set as your custom thumbnail.":
            await db.set_thumbnail(user_id, file_id)
            await message.reply_text("✅ Custom thumbnail saved!")
            
    except Exception as e:
        logging.error(f"Error in save_thumb: {e}")
        await message.reply_text(f"❌ An error occurred: {str(e)}")
