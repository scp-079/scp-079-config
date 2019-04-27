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

from pyrogram import Client

from .. import glovar
from .etc import code, general_link, send_data, thread
from .telegram import get_admins, get_group_info, send_document, send_message

# Enable logging
logger = logging.getLogger(__name__)


def update_status(client: Client) -> bool:
    try:
        exchange_text = send_data(
            sender="WARN",
            receivers=["MANAGE"],
            action="update",
            action_type="status",
            data="awake"
        )
        thread(send_message, (client, glovar.exchange_channel_id, exchange_text))
        return True
    except Exception as e:
        logger.warning(f"Update status error: {e}")

    return False
