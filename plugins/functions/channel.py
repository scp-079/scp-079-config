# SCP-079-CONFIG - Manage the settings of each bot
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
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
from json import dumps
from typing import List, Union

from pyrogram import Client

from .. import glovar
from .decorators import threaded
from .etc import code, code_block, lang, thread
from .file import crypt_file, delete_file, get_new_path
from .telegram import send_document, send_message

# Enable logging
logger = logging.getLogger(__name__)


def exchange_to_hide(client: Client) -> bool:
    # Let other bots exchange data in the hide channel instead
    result = False

    try:
        # Transfer the channel
        glovar.should_hide = True
        share_data(
            client=client,
            receivers=["EMERGENCY"],
            action="backup",
            action_type="hide",
            data=True
        )

        # Send debug message
        text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('issue')}{lang('colon')}{code(lang('exchange_invalid'))}\n"
                f"{lang('auto_fix')}{lang('colon')}{code(lang('protocol_1'))}\n")
        thread(send_message, (client, glovar.critical_channel_id, text))

        result = True
    except Exception as e:
        logger.warning(f"Exchange to hide error: {e}", exc_info=True)

    return result


def format_data(sender: str, receivers: List[str], action: str, action_type: str,
                data: Union[bool, dict, int, str] = None) -> str:
    # Get exchange string
    result = ""

    try:
        data = {
            "from": sender,
            "to": receivers,
            "action": action,
            "type": action_type,
            "data": data
        }
        result = code_block(dumps(data, indent=4))
    except Exception as e:
        logger.warning(f"Format data error: {e}", exc_info=True)

    return result


@threaded()
def share_data(client: Client, receivers: List[str], action: str, action_type: str,
               data: Union[bool, dict, int, str] = None, file: str = None, encrypt: bool = True) -> bool:
    # Use this function to share data in the channel
    result = False

    try:
        if glovar.sender in receivers:
            receivers.remove(glovar.sender)

        if not receivers:
            return False

        if glovar.should_hide:
            channel_id = glovar.hide_channel_id
        else:
            channel_id = glovar.exchange_channel_id

        # Plain text
        if not file:
            text = format_data(
                sender=glovar.sender,
                receivers=receivers,
                action=action,
                action_type=action_type,
                data=data
            )
            result = send_message(client, channel_id, text)
            return ((result is not False or glovar.should_hide)
                    or share_data_failed(client, receivers, action, action_type, data, file, encrypt))

        # Share with a file
        text = format_data(
            sender=glovar.sender,
            receivers=receivers,
            action=action,
            action_type=action_type,
            data=data
        )

        if encrypt:
            # Encrypt the file, save to the tmp directory
            file_path = get_new_path()
            crypt_file("encrypt", file, file_path)
        else:
            # Send directly
            file_path = file

        result = send_document(client, channel_id, file_path, None, text)

        if not result:
            return ((result is not False or glovar.should_hide)
                    or share_data_failed(client, receivers, action, action_type, data, file, encrypt))

        # Delete the tmp file
        for f in {file, file_path}:
            f.startswith("tmp/") and thread(delete_file, (f,))

        result = bool(result)
    except Exception as e:
        logger.warning(f"Share data error: {e}", exc_info=True)

    return result


@threaded()
def share_data_failed(client: Client, receivers: List[str], action: str, action_type: str,
                      data: Union[bool, dict, int, str] = None, file: str = None, encrypt: bool = True) -> bool:
    # Sharing data failed, use the exchange channel instead
    result = False

    try:
        exchange_to_hide(client)
        result = share_data(
            client=client,
            receivers=receivers,
            action=action,
            action_type=action_type,
            data=data,
            file=file,
            encrypt=encrypt
        )
    except Exception as e:
        logger.warning(f"Share data failed error: {e}", exc_info=True)

    return result
