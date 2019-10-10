# SCP-079-CONFIG - Manage the settings of each bot
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-CONFIG.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pickle
from json import loads
from typing import Any

from pyrogram import Client, Message

from .. import glovar
from .channel import share_data
from .config import get_config_message
from .etc import code, general_link, get_now, get_text, lang, message_link, random_str, thread, user_mention
from .file import crypt_file, delete_file, get_downloaded_path, get_new_path, save
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def receive_config_ask(client: Client, sender: str, data: dict) -> bool:
    # Receive config ask
    try:
        # Generate a new config key
        key = random_str(8)
        while glovar.configs.get(key):
            key = random_str(8)

        # Set basic data
        glovar.configs[key] = data
        glovar.configs[key]["type"] = sender.lower()
        glovar.configs[key]["lock"] = False
        glovar.configs[key]["commit"] = False
        glovar.configs[key]["time"] = get_now()

        # Send the config session message
        text, markup = get_config_message(key)
        sent_message = send_message(client, glovar.config_channel_id, text, None, markup)

        if sent_message:
            # If message is sent, initiate the check process
            glovar.configs[key]["message_id"] = sent_message.message_id
            # Reply the bot in the exchange channel, let it send a report in the group
            group_id = glovar.configs[key]["group_id"]
            user_id = glovar.configs[key]["user_id"]
            share_data(
                client=client,
                receivers=[sender],
                action="config",
                action_type="reply",
                data={
                    "group_id": group_id,
                    "user_id": user_id,
                    "config_link": message_link(sent_message)
                }
            )
            save("configs")
        else:
            # If something goes wrong, pop the config
            glovar.configs.pop(key, {})

        return True
    except Exception as e:
        logger.warning(f"Receive config ask error: {e}", exc_info=True)

    return False


def receive_file_data(client: Client, message: Message, decrypt: bool = True) -> Any:
    # Receive file's data from exchange channel
    data = None
    try:
        if not message.document:
            return None

        file_id = message.document.file_id
        file_ref = message.document.file_ref
        path = get_downloaded_path(client, file_id, file_ref)

        if not path:
            return None

        if decrypt:
            # Decrypt the file, save to the tmp directory
            path_decrypted = get_new_path()
            crypt_file("decrypt", path, path_decrypted)
            path_final = path_decrypted
        else:
            # Read the file directly
            path_decrypted = ""
            path_final = path

        with open(path_final, "rb") as f:
            data = pickle.load(f)

        for f in {path, path_decrypted}:
            thread(delete_file, (f,))
    except Exception as e:
        logger.warning(f"Receive file error: {e}", exc_info=True)

    return data


def receive_rollback(client: Client, message: Message, data: dict) -> bool:
    # Receive rollback data
    try:
        # Basic data
        aid = data["admin_id"]
        the_type = data["type"]
        the_data = receive_file_data(client, message)

        if the_data:
            exec(f"glovar.{the_type} = the_data")
            save(the_type)

        # Send debug message
        text = (f"{lang('project')}{lang('colon')}{general_link(glovar.project_name, glovar.project_link)}\n"
                f"{lang('admin_project')}{lang('colon')}{user_mention(aid)}\n"
                f"{lang('action')}{lang('colon')}{code(lang('rollback'))}\n"
                f"{lang('more')}{lang('colon')}{code(the_type)}\n")
        thread(send_message, (client, glovar.debug_channel_id, text))
    except Exception as e:
        logger.warning(f"Receive rollback error: {e}", exc_info=True)

    return False


def receive_text_data(message: Message) -> dict:
    # Receive text's data from exchange channel
    data = {}
    try:
        text = get_text(message)
        if text:
            data = loads(text)
    except Exception as e:
        logger.warning(f"Receive data error: {e}")

    return data
