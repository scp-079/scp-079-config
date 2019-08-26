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
from json import loads

from pyrogram import Client, Message

from .. import glovar
from .channel import share_data
from .config import check_commit, get_config_message
from .etc import delay, get_text, message_link, random_str
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def receive_config_ask(client: Client, sender: str, data: dict) -> bool:
    # Receive config ask
    try:
        # Generate a new config key
        config_key = random_str(8)
        while glovar.configs.get(config_key):
            config_key = random_str(8)

        # Set basic data
        glovar.configs[config_key] = data
        glovar.configs[config_key]["type"] = sender.lower()
        glovar.configs[config_key]["commit"] = False
        # Send the config session message
        text, markup = get_config_message(config_key)
        sent_message = send_message(client, glovar.config_channel_id, text, None, markup)
        if sent_message:
            # If message is sent, initiate the check process
            glovar.configs[config_key]["message_id"] = sent_message.message_id
            delay(300, check_commit, [client, config_key])
            # Reply the bot in the exchange channel, let it send a report in the group
            group_id = glovar.configs[config_key]["group_id"]
            user_id = glovar.configs[config_key]["user_id"]
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
        else:
            # If something goes wrong, pop the config
            glovar.configs.pop(config_key, None)

        return True
    except Exception as e:
        logger.warning(f"Receive config ask error: {e}", exc_info=True)

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
