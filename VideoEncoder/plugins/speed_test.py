import asyncio
from pyrogram import filters
from speedtest import Speedtest

from .. import app, LOGGER, sudo_users, owner
from ..utils.display_progress import humanbytes

async def sync_to_async(func, *args, **kwargs):
    return await asyncio.get_running_loop().run_in_executor(None, func, *args, **kwargs)

@app.on_message(filters.command("speedtest") & filters.user(sudo_users + owner))
async def speedtest(_, message):
    msg = await message.reply('<i>Running speed test...</i>')
    try:
        test = Speedtest()
        await sync_to_async(test.get_best_server)
        await sync_to_async(test.download)
        await sync_to_async(test.upload)
        await sync_to_async(test.results.share)
        result = await sync_to_async(test.results.dict)
        caption = f'''
<b>SPEEDTEST RESULT</b>
<b>┌ IP: </b>{result['client']['ip']}
<b>├ ISP: </b>{result['client']['isp']}
<b>├ Ping: </b>{int(result['ping'])} ms
<b>├ ISP Rating: </b>{result['client']['isprating']}
<b>├ Sponsor: </b>{result['server']['sponsor']}
<b>├ Upload: </b>{humanbytes(result['upload'] / 8)}/s
<b>├ Download: </b>{humanbytes(result['download'] / 8)}/s
<b>├ Server Name: </b>{result['server']['name']}
<b>├ Country: </b>{result['server']['country']}, {result['server']['cc']}
<b>└ LAT/LON </b>{result['client']['lat']}/{result['client']['lon']}
'''
        await msg.delete()
        await message.reply_photo(photo=result['share'], caption=caption)
    except Exception as e:
        LOGGER.error(e)
        await msg.edit(f'Failed running speedtest {e}')
