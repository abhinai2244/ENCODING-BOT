from asyncio import gather
from psutil import cpu_percent, virtual_memory, disk_usage, net_io_counters
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from time import time
import os

from .. import app, botStartTime, download_dir, data, sudo_users, owner
from ..utils.display_progress import humanbytes, TimeFormatter
from ..utils.helper import check_chat

# Helper function for readable time
def get_readable_time(seconds):
    return TimeFormatter(seconds)

def get_readable_file_size(size):
    return humanbytes(size)

def get_task_info(task_msg):
    user = task_msg.from_user.first_name if task_msg.from_user else "Unknown User"
    user_id = task_msg.from_user.id if task_msg.from_user else "No ID"

    task_type = "Unknown Task"
    filename = "Unknown File"

    text_content = task_msg.text or task_msg.caption
    if text_content:
        parts = text_content.split(None, 1)
        cmd = parts[0].lower()
        if '/dl' in cmd:
            task_type = "Telegram Download"
        elif '/af' in cmd:
            task_type = "Audio Processing"
        elif '/ddl' in cmd:
            task_type = "Direct Download"
        elif '/batch' in cmd:
            task_type = "Batch Process"

    if task_msg.document:
        filename = task_msg.document.file_name or "Document"
        if task_type == "Unknown Task": task_type = "Telegram Download"
    elif task_msg.video:
        filename = task_msg.video.file_name or "Video"
        if task_type == "Unknown Task": task_type = "Telegram Download"
    elif text_content and ('/ddl' in text_content or '/batch' in text_content):
        # Attempt to extract filename or url
        filename = "URL Task"

    return f"{task_type}: {filename}\n   └ User: <a href='tg://user?id={user_id}'>{user}</a>"

@app.on_message(filters.command("status"))
async def mirror_status(client, message: Message):
    c = await check_chat(message, chat='Both')
    if not c:
        return

    count = len(data)

    # System Stats
    cpu = cpu_percent()
    mem = virtual_memory().percent
    disk = disk_usage(download_dir).free
    upload_speed = humanbytes(net_io_counters().bytes_sent)
    download_speed = humanbytes(net_io_counters().bytes_recv)
    uptime = get_readable_time(time() - botStartTime)

    msg = (
        f'<b>System Status</b>\n'
        f'<b>CPU:</b> {cpu}% | <b>RAM:</b> {mem}%\n'
        f'<b>FREE:</b> {get_readable_file_size(disk)}\n'
        f'<b>UP:</b> {upload_speed} | <b>DL:</b> {download_speed}\n'
        f'<b>Uptime:</b> {uptime}\n\n'
    )

    if count:
        msg += f"<b>Active Tasks:</b> {count}\n"
        for i, task_msg in enumerate(data):
             info = get_task_info(task_msg)
             msg += f"{i+1}. {info}\n"
    else:
        msg += "No Active Downloads!\n"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Refresh", callback_data="status ref")]
    ])

    await message.reply(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex('^status'))
async def status_pages(client, query: CallbackQuery):
    data_split = query.data.split()
    cmd = data_split[1]

    if cmd == 'ref':
        count = len(data)

        cpu = cpu_percent()
        mem = virtual_memory().percent
        disk = disk_usage(download_dir).free
        upload_speed = humanbytes(net_io_counters().bytes_sent)
        download_speed = humanbytes(net_io_counters().bytes_recv)
        uptime = get_readable_time(time() - botStartTime)

        msg = (
            f'<b>System Status</b>\n'
            f'<b>CPU:</b> {cpu}% | <b>RAM:</b> {mem}%\n'
            f'<b>FREE:</b> {get_readable_file_size(disk)}\n'
            f'<b>UP:</b> {upload_speed} | <b>DL:</b> {download_speed}\n'
            f'<b>Uptime:</b> {uptime}\n\n'
        )

        if count:
            msg += f"<b>Active Tasks:</b> {count}\n"
            for i, task_msg in enumerate(data):
                 info = get_task_info(task_msg)
                 msg += f"{i+1}. {info}\n"
        else:
            msg += "No Active Downloads!\n"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Refresh", callback_data="status ref")]
        ])

        try:
            await query.message.edit(text=msg, reply_markup=buttons)
            await query.answer("Refreshed!")
        except Exception as e:
            await query.answer(f"Error: {e}")
    else:
        await query.answer("Unknown command")
