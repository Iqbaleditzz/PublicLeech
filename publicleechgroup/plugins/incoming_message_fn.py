#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2020 PublicLeech Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import os

from publicleechgroup import (
    DOWNLOAD_LOCATION
)


import time
import aria2p
import asyncio
from publicleechgroup.helper_funcs.extract_link_from_message import extract_link
from publicleechgroup.helper_funcs.download_aria_p_n import (
    call_apropriate_function, aria_start,
    fake_etairporpa_call
)
from publicleechgroup.helper_funcs.download_from_link import request_download
from publicleechgroup.helper_funcs.display_progress import progress_for_pyrogram
from publicleechgroup.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from publicleechgroup.helper_funcs.admin_check import AdminCheck
from publicleechgroup.helper_funcs.create_r_o_m import get_markup
from publicleechgroup.helper_funcs.icntaosrtsba import leech_btn_k
from publicleechgroup.helper_funcs.fix_tcerrocni_images import proc_ess_image_aqon

        
async def incoming_purge_message_f(client, message):
    """/purge command"""
    i_m_sefg2 = await message.reply_text("Purging...", quote=True)
    if await AdminCheck(client, message.chat.id, message.from_user.id):
        aria_i_p = await aria_start()
        # Show All Downloads
        downloads = aria_i_p.get_downloads()
        for download in downloads:
            LOGGER.info(download.remove(force=True))
    await i_m_sefg2.delete()


async def incoming_message_f(client, message):
    """/leech command"""
    i_m_sefg = await message.reply_text("checking ", quote=True)
    t_, rm_ = await get_markup(message)
    await i_m_sefg.edit_text(
        text=t_,
        reply_markup=rm_,
        disable_web_page_preview=True
    )


async def leech_commandi_f(client, message):
    m_ = await message.reply_text(
        "checking",
        quote=True
    )
    force_doc = True
    m_sgra = " ".join(message.command[1:])
    if "file" in m_sgra.lower():
        force_doc = True
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(
        message.reply_to_message, "LEECH"
    )
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await m_.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        current_user_id = message.reply_to_message.from_user.id
        # create an unique directory
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(message.reply_to_message.message_id)
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        if "_" in m_sgra:
            await m_.edit_text("trying to download")
            # try to download the "link"
            sagtus, err_message = await fake_etairporpa_call(
                aria_i_p,
                dl_url,
                new_download_location,
                m_,
                int(m_sgra.split("_")[2])
                # maybe IndexError / ValueError might occur,
                # we don't know, yet!!
            )
            if not sagtus:
                # if FAILED, display the error message
                await m_.edit_text(err_message)
        else:
            is_zip = False
            if "a" in m_sgra:
                is_zip = True
            await m_.edit_text("trying to download")
            # try to download the "link"
            sagtus, err_message = await call_apropriate_function(
                aria_i_p,
                dl_url,
                new_download_location,
                m_,
                is_zip,
                force_doc=force_doc,
                cfn=cf_name
            )
            if not sagtus:
                # if FAILED, display the error message
                await m_.edit_text(err_message)


async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
        message.reply_to_message, "YTDL"
    )
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(message.reply_to_message.message_id)
        )
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            # cf_name,
            yt_dl_user_name,
            yt_dl_pass_word,
            user_working_dir
        )
        if thumb_image is not None:
            thumb_image = await proc_ess_image_aqon(
                thumb_image,
                user_working_dir
            )
            await message.reply_photo(
                photo=thumb_image,
                quote=True,
                caption=text_message,
                reply_to_message_id=message.reply_to_message.message_id,
                reply_markup=reply_markup
            )
            os.remove(thumb_image)
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(
                text=text_message,
                reply_markup=reply_markup
            )
    else:
        await i_m_sefg.edit_text(
            "**തേങ്ങ**! എന്തൊക്കെയാട നീ ഈ പറയുന്നെ. \nPlease read /help \n"
            f"<b>API Error</b>: {cf_name}"
        )
