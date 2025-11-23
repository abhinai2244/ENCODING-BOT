

import datetime
import json
import os

from pyrogram import Client
from pyrogram.types import CallbackQuery

from .. import app, download_dir, log, owner, sudo_users, LOGGER
from ..plugins.queue import queue_answer
from ..utils.database.access_db import db
from ..utils.settings import (AudioSettings, ExtraSettings, OpenSettings,
                              VideoSettings)
from .start import showw_status
from ..video_utils.audio_selector import sessions


@app.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    try:
        # Close Button

        if cb.data == "closeMeh":
            await cb.message.delete(True)

        # Settings

        elif cb.data == "VideoSettings":
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "OpenSettings":
            await OpenSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "AudioSettings":
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "ExtraSettings":
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerMode":
            if await db.get_drive(cb.from_user.id) is True:
                await db.set_drive(cb.from_user.id, drive=False)
            else:
                await db.set_drive(cb.from_user.id, drive=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerUploadMode":
            if await db.get_upload_as_doc(cb.from_user.id) is True:
                await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
            else:
                await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerResize":
            if await db.get_resize(cb.from_user.id) is True:
                await db.set_resize(cb.from_user.id, resize=False)
            else:
                await db.set_resize(cb.from_user.id, resize=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # Watermark
        elif cb.data == "Watermark":
            await cb.answer("Sir, this button not works XD\n\nPress Bottom Buttons.", show_alert=True)

        # Metadata
        elif cb.data == "triggerMetadata":
            if await db.get_metadata_w(cb.from_user.id):
                await db.set_metadata_w(cb.from_user.id, metadata=False)
            else:
                await db.set_metadata_w(cb.from_user.id, metadata=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # Watermark
        elif cb.data == "triggerVideo":
            if await db.get_watermark(cb.from_user.id):
                await db.set_watermark(cb.from_user.id, watermark=False)
            else:
                await db.set_watermark(cb.from_user.id, watermark=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # Subtitles
        elif cb.data == "triggerHardsub":
            if await db.get_hardsub(cb.from_user.id):
                await db.set_hardsub(cb.from_user.id, hardsub=False)
            else:
                await db.set_hardsub(cb.from_user.id, hardsub=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerSubtitles":
            if await db.get_subtitles(cb.from_user.id):
                await db.set_subtitles(cb.from_user.id, subtitles=False)
            else:
                await db.set_subtitles(cb.from_user.id, subtitles=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # Extension
        elif cb.data == "triggerextensions":
            ex = await db.get_extensions(cb.from_user.id)
            if ex == 'MP4':
                await db.set_extensions(cb.from_user.id, extensions='MKV')
            elif ex == 'MKV':
                await db.set_extensions(cb.from_user.id, extensions='AVI')
            else:
                await db.set_extensions(cb.from_user.id, extensions='MP4')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Frame
        elif cb.data == "triggerframe":
            fr = await db.get_frame(cb.from_user.id)
            if fr == 'ntsc':
                await db.set_frame(cb.from_user.id, frame='source')
            elif fr == 'source':
                await db.set_frame(cb.from_user.id, frame='pal')
            elif fr == 'pal':
                await db.set_frame(cb.from_user.id, frame='film')
            elif fr == 'film':
                await db.set_frame(cb.from_user.id, frame='23.976')
            elif fr == '23.976':
                await db.set_frame(cb.from_user.id, frame='30')
            elif fr == '30':
                await db.set_frame(cb.from_user.id, frame='60')
            else:
                await db.set_frame(cb.from_user.id, frame='ntsc')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Preset
        elif cb.data == "triggerPreset":
            p = await db.get_preset(cb.from_user.id)
            if p == 'uf':
                await db.set_preset(cb.from_user.id, preset='sf')
            elif p == 'sf':
                await db.set_preset(cb.from_user.id, preset='vf')
            elif p == 'vf':
                await db.set_preset(cb.from_user.id, preset='f')
            elif p == 'f':
                await db.set_preset(cb.from_user.id, preset='m')
            elif p == 'm':
                await db.set_preset(cb.from_user.id, preset='s')
            else:
                await db.set_preset(cb.from_user.id, preset='uf')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # sample rate
        elif cb.data == "triggersamplerate":
            sr = await db.get_samplerate(cb.from_user.id)
            if sr == '44.1K':
                await db.set_samplerate(cb.from_user.id, sample='48K')
            elif sr == '48K':
                await db.set_samplerate(cb.from_user.id, sample='source')
            else:
                await db.set_samplerate(cb.from_user.id, sample='44.1K')
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        # bitrate
        elif cb.data == "triggerbitrate":
            bit = await db.get_bitrate(cb.from_user.id)
            if bit == '400':
                await db.set_bitrate(cb.from_user.id, bitrate='320')
            elif bit == '320':
                await db.set_bitrate(cb.from_user.id, bitrate='256')
            elif bit == '256':
                await db.set_bitrate(cb.from_user.id, bitrate='224')
            elif bit == '224':
                await db.set_bitrate(cb.from_user.id, bitrate='192')
            elif bit == '192':
                await db.set_bitrate(cb.from_user.id, bitrate='160')
            elif bit == '160':
                await db.set_bitrate(cb.from_user.id, bitrate='128')
            elif bit == '128':
                await db.set_bitrate(cb.from_user.id, bitrate='source')
            else:
                await db.set_bitrate(cb.from_user.id, bitrate='400')
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        # Audio Codec
        elif cb.data == "triggerAudioCodec":
            a = await db.get_audio(cb.from_user.id)
            if a == 'dd':
                await db.set_audio(cb.from_user.id, audio='copy')
            elif a == 'copy':
                await db.set_audio(cb.from_user.id, audio='aac')
            elif a == 'aac':
                await db.set_audio(cb.from_user.id, audio='opus')
            elif a == 'opus':
                await db.set_audio(cb.from_user.id, audio='alac')
            elif a == 'alac':
                await db.set_audio(cb.from_user.id, audio='vorbis')
            else:
                await db.set_audio(cb.from_user.id, audio='dd')
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        # Audio Channel
        elif cb.data == "triggerAudioChannels":
            c = await db.get_channels(cb.from_user.id)
            if c == 'source':
                await db.set_channels(cb.from_user.id, channels='1.0')
            elif c == '1.0':
                await db.set_channels(cb.from_user.id, channels='2.0')
            elif c == '2.0':
                await db.set_channels(cb.from_user.id, channels='2.1')
            elif c == '2.1':
                await db.set_channels(cb.from_user.id, channels='5.1')
            elif c == '5.1':
                await cb.answer("7.1 is for bluray only.", show_alert=True)
                await db.set_channels(cb.from_user.id, channels='7.1')
            else:
                await db.set_channels(cb.from_user.id, channels='source')
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        # Resolution
        elif cb.data == "triggerResolution":
            r = await db.get_resolution(cb.from_user.id)
            if r == 'OG':
                await db.set_resolution(cb.from_user.id, resolution='1080')
            elif r == '1080':
                await db.set_resolution(cb.from_user.id, resolution='720')
            elif r == '720':
                await db.set_resolution(cb.from_user.id, resolution='480')
            elif r == '480':
                await db.set_resolution(cb.from_user.id, resolution='576')
            else:
                await db.set_resolution(cb.from_user.id, resolution='OG')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Video Bits
        elif cb.data == "triggerBits":
            b = await db.get_bits(cb.from_user.id)
            if await db.get_hevc(cb.from_user.id):
                if b:
                    await db.set_bits(cb.from_user.id, bits=False)
                else:
                    await db.set_bits(cb.from_user.id, bits=True)
            else:
                if b:
                    await db.set_bits(cb.from_user.id, bits=False)
                else:
                    await cb.answer("H264 don't support 10 bits in this bot.",
                                    show_alert=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # HEVC
        elif cb.data == "triggerHevc":
            if await db.get_hevc(cb.from_user.id):
                await db.set_hevc(cb.from_user.id, hevc=False)
            else:
                await db.set_hevc(cb.from_user.id, hevc=True)
                await cb.answer("H265 need more time for encoding video", show_alert=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Tune
        elif cb.data == "triggertune":
            if await db.get_tune(cb.from_user.id):
                await db.set_tune(cb.from_user.id, tune=False)
            else:
                await db.set_tune(cb.from_user.id, tune=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Reframe
        elif cb.data == "triggerreframe":
            rf = await db.get_reframe(cb.from_user.id)
            if rf == '4':
                await db.set_reframe(cb.from_user.id, reframe='8')
            elif rf == '8':
                await db.set_reframe(cb.from_user.id, reframe='16')
                await cb.answer("Reframe 16 maybe not support", show_alert=True)
            elif rf == '16':
                await db.set_reframe(cb.from_user.id, reframe='pass')
            else:
                await db.set_reframe(cb.from_user.id, reframe='4')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # CABAC
        elif cb.data == "triggercabac":
            if await db.get_cabac(cb.from_user.id):
                await db.set_cabac(cb.from_user.id, cabac=False)
            else:
                await db.set_cabac(cb.from_user.id, cabac=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Aspect
        elif cb.data == "triggeraspect":
            if await db.get_aspect(cb.from_user.id):
                await db.set_aspect(cb.from_user.id, aspect=False)
            else:
                await db.set_aspect(cb.from_user.id, aspect=True)
                await cb.answer("This will help to force video to 16:9", show_alert=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerCRF":
            crf = await db.get_crf(cb.from_user.id)
            nextcrf = int(crf) + 1
            if nextcrf > 30:
                await db.set_crf(cb.from_user.id, crf=18)
            else:
                await db.set_crf(cb.from_user.id, crf=nextcrf)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # Audio Selector Callbacks
        elif "audiosel" in cb.data:
            user_id = cb.from_user.id
            if user_id in sessions:
                await sessions[user_id].resolve_callback(cb)
            else:
                await cb.answer("Session expired. Please try again.", show_alert=True)

        # Cancel

        elif cb.data == "cancel":
            status = download_dir + "status.json"
            try:
                with open(status, 'r+') as f:
                    statusMsg = json.load(f)
                    user = cb.from_user.id
                    if user != statusMsg['user']:
                        if user == 885190545:
                            pass
                        elif user in sudo_users or user in owner:
                            pass
                        else:
                            return
                    statusMsg['running'] = False
                    f.seek(0)
                    json.dump(statusMsg, f, indent=2)
                    os.remove('VideoEncoder/utils/extras/downloads/process.txt')
                    try:
                        await cb.message.edit_text("🚦🚦 Process Cancelled 🚦🚦")
                        chat_id = log
                        utc_now = datetime.datetime.utcnow()
                        ist_now = utc_now + \
                            datetime.timedelta(minutes=30, hours=5)
                        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                        bst_now = utc_now + \
                            datetime.timedelta(minutes=00, hours=6)
                        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                        await bot.send_message(chat_id, f"**Last Process Cancelled, Bot is Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
                    except:
                        pass
            except FileNotFoundError:
                 await cb.answer("Nothing to cancel or process already finished!", show_alert=True)

        # Stats
        elif 'stats' in cb.data:
            stats = await showw_status(bot)
            stats = stats.replace('<b>', '')
            stats = stats.replace('</b>', '')
            await cb.answer(stats, show_alert=True)

        # Queue
        elif "queue+" in cb.data:
            await queue_answer(app, cb)
    except Exception as e:
        LOGGER.error(f"Error in callback_handlers: {e}")
        try:
            await cb.answer("An error occurred. Please try again later.", show_alert=True)
        except:
            pass
