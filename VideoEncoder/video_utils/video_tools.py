from aiofiles.os import path as aiopath
from asyncio import sleep
from pyrogram import Client
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from secrets import token_urlsafe

from bot import bot, config_dict, LOGGER
from bot.helper.ext_utils.bot_utils import new_task, arg_parser, is_premium_user
from bot.helper.ext_utils.commons_check import UseCheck
from bot.helper.ext_utils.links_utils import is_url, get_url_name, get_link
from bot.helper.listeners.tasks_listener import TaskListener
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage, auto_delete_message
from bot.helper.video_utils.executor import VidEcxecutor, get_metavideo
from bot.helper.video_utils.selector import SelectMode


class VidTools(TaskListener):
    def __init__(self, client: Client, message: Message, _=False, __=False, isLeech=False, ___=None, ____=None, bulk=None, multiTag=None, options=''):
        if bulk is None:
            bulk = []
        self.message = message
        self.client = client
        self.sameDir = {}
        self.multiTag = multiTag
        self.options = options
        self.bulk = bulk
        super().__init__()
        self.isLeech = isLeech

    @new_task
    async def newEvent(self):
        text = (self.message.text or self.message.caption or "").split('\n')
        await self.getTag(text)

        if fmsg := await UseCheck(self.message, self.isLeech).run(True, daily=True, ml_chek=True, session=True, send_pm=True):
            await auto_delete_message(self.message, fmsg, self.message.reply_to_message)
            return

        arg_base = {'-i': 0,
                    '-sp': 0,
                    '-b': False,
                    '-gf': False,
                    '-sv': False,
                    '-z': False,
                    '-n': '',
                    '-rcf': '',
                    '-t': '',
                    '-up': '',
                    'link': ''}
        input_list = text[0].split(' ')
        args = arg_parser(input_list[1:], arg_base)

        self.link = args['link']
        self.compress = args['-z']
        self.isGofile = args['-gf']
        self.name = args['-n'].replace('/', '')
        self.rcFlags = args['-rcf']
        self.sampleVideo = args['-sv']
        self.splitSize = args['-sp']
        self.thumb = args['-t']
        self.upDest = args['-up']

        isBulk = args['-b']
        bulk_start = bulk_end = 0

        try:
            self.multi = int(args['-i'])
        except:
            self.multi = 0

        if not isinstance(isBulk, bool):
            dargs = isBulk.split(':')
            bulk_start = dargs[0] or None
            if len(dargs) == 2:
                bulk_end = dargs[1] or None
            isBulk = True

        if config_dict['PREMIUM_MODE'] and not is_premium_user(self.user_id) and (self.multi > 0 or isBulk):
            await sendMessage(f'Upss {self.tag}, multi/bulk mode for premium user only', self.message)
            return

        if isBulk:
            await self.initBulk(input_list, bulk_start, bulk_end, VidTools)
            return

        if self.bulk:
            del self.bulk[0]

        self.link = self.link or get_link(self.message)

        if not is_url(self.link):
            await sendMessage('Send command along with link or by reply to the link!', self.message)
            self.run_multi(input_list, '', VidTools)
            return

        if not (metadata := await get_metavideo(self.link)) and not metadata[0]:
            await sendMessage('Failed getting metadata!', self.message)
            self.run_multi(input_list, '', VidTools)
            return

        self.vidMode = await SelectMode(self, True).get_buttons()
        if not self.vidMode:
            self.run_multi(input_list, '', VidTools)
            return

        if not self.vidMode[1] and self.name:
            self.vidMode[1] = self.name

        self.name = get_url_name(self.link)
        self.run_multi(input_list, '', VidTools)
        self.editable = await sendMessage('<i>Checking request, please wait...</i>', self.message)
        await sleep(1)

        try:
            await self.beforeStart()
        except Exception as e:
            await editMessage(str(e), self.editable)
            return

        await deleteMessage(self.editable)
        LOGGER.info(self.link)
        gid = token_urlsafe(12)
        out_pah = await VidEcxecutor(self, self.link, gid, metadata).execute()
        if not out_pah:
            return

        if not await aiopath.exists(str(out_pah)):
            self.name = self.vidMode[1] or self.name
            await self.onUploadError('No file(s) to upload')
            return
        self.vidMode = None
        await self.onDownloadComplete()


async def mirror_vidtools(client: Client, message: Message):
    VidTools(client, message).newEvent()


async def leech_vidtools(client: Client, message: Message):
    VidTools(client, message, isLeech=True).newEvent()


bot.add_handler(MessageHandler(mirror_vidtools, filters=command(BotCommands.MVidCommand) & CustomFilters.authorized))
bot.add_handler(MessageHandler(leech_vidtools, filters=command(BotCommands.LVidCommand) & CustomFilters.authorized))
