from asyncio import Event, wait_for, wrap_future, gather
from functools import partial
from pyrogram.filters import regex, user
from pyrogram.handlers import CallbackQueryHandler
from time import time

from bot import bot, VID_MODE
from bot.helper.ext_utils.bot_utils import new_task, new_thread
from bot.helper.ext_utils.status_utils import get_readable_time
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.message_utils import editMessage, sendMessage


class AudioSelect():
    def __init__(self, listener: 'TaskListener'):
        self._is_cancelled = False
        self._reply = None
        self._time = time()
        self.listener = listener
        self.aud_streams = {}
        self.event = Event()
        self.message = listener.message
        self.streams = -1

    @new_thread
    async def _event_handler(self):
        pfunc = partial(cb_audiosel, obj=self)
        handler = self.listener.client.add_handler(CallbackQueryHandler(pfunc, filters=regex('^audiosel') & user(self.listener.user_id)), group=-1)
        try:
            await wait_for(self.event.wait(), timeout=180)
        except:
            self._is_cancelled = True
            self.event.set()
        finally:
            self.listener.client.remove_handler(*handler)

    async def get_buttons(self, streams):
        self.streams = streams
        for stream in self.streams:
            if stream['codec_type'] == 'audio':
                self.aud_streams[stream['index']] = {'map': stream['index'],
                                                     'title': stream['tags'].get('title'),
                                                     'lang': stream['tags'].get('language')}

        if not self.aud_streams or len(self.aud_streams) < 2:
            return -1, -1

        future = self._event_handler()
        await gather(self._send_message(), wrap_future(future))
        if self._is_cancelled:
            await editMessage('Task has been cancelled!', self._reply)
            return -1, -1
        await self._reply.delete()
        maps = [i['map'] for i in self.aud_streams.values()]
        return maps, self.aud_streams

    async def _send_message(self):
        buttons = ButtonMaker()
        text = f"<b>CHOOSE AUDIO STREAM TO SWAP</b>\n\n<b>Audio Streams: {len(self.aud_streams)}</b>"
        for index, stream in self.aud_streams.items():
            buttons.button_data(f"{stream['lang'] or 'und'} | {stream['title'] or 'No Title'}", f"audiosel none {index}")
            buttons.button_data("▲", f"audiosel up {index}")
            buttons.button_data("⇅", f"audiosel swap {index}")
            buttons.button_data("▼", f"audiosel down {index}")
        buttons.button_data('Done', 'audiosel done', 'footer')
        buttons.button_data('Cancel', 'audiosel cancel', 'footer')
        if not self._reply:
            self._reply = await sendMessage(text, self.message, buttons.build_menu(4))
        else:
            await editMessage(text, self._reply, buttons.build_menu(4))
        await self._create_streams_view(self._reply)

    async def _create_streams_view(self, reply):
        text = f"<b>STREAMS ORDER</b>"
        for index, stream in self.aud_streams.items():
            text += f"\n{stream['lang'] or 'und'} | {stream['title'] or 'No Title'}"
        text += f'\n\nTime Out: {get_readable_time(180 - (time()-self._time))}'

        if (stream_view := bot.stream_view.get(reply.id)) and stream_view.text != text:
            await editMessage(text, stream_view)
        elif not stream_view:
            bot.stream_view[reply.id] = await sendMessage(text, self.message)


@new_task
async def cb_audiosel(_, query, obj: AudioSelect):
    data = query.data.split()
    if data[1] == 'cancel':
        obj._is_cancelled = True
    elif data[1] == 'done':
        pass
    elif data[1] == 'none':
        return
    else:
        aud_list = list(obj.aud_streams.keys())
        if data[1] == 'swap':
            pos = aud_list.index(int(data[2]))
            if pos != 0:
                aud_list[pos], aud_list[pos-1] = aud_list[pos-1], aud_list[pos]
        elif data[1] == 'up':
            pos = aud_list.index(int(data[2]))
            if pos != 0:
                aud_list.insert(pos-1, aud_list.pop(pos))
        elif data[1] == 'down':
            pos = aud_list.index(int(data[2]))
            if pos != len(aud_list)-1:
                aud_list.insert(pos+1, aud_list.pop(pos))
        new_aud_streams = {}
        for aud in aud_list:
            new_aud_streams[aud] = obj.aud_streams[aud]
        obj.aud_streams = new_aud_streams

    if not obj._is_cancelled and data[1] != 'done':
        await obj._send_message()
    else:
        obj.event.set()
