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
from typing import Union

from pyrogram import CallbackQuery, Filters, Message

from .. import glovar


# Enable logging
logger = logging.getLogger(__name__)


def is_config_channel(_, update: Union[CallbackQuery, Message]) -> bool:
    try:
        if isinstance(update, CallbackQuery):
            message = update.message
        else:
            message = update

        cid = message.chat.id
        if cid == glovar.config_channel_id:
            return True
    except Exception as e:
        logger.warning(f"Is class c error: {e}")

    return False


def is_exchange_channel(_, message: Message) -> bool:
    cid = message.chat.id
    if cid == glovar.exchange_channel_id:
        return True

    return False


def is_test_group(_, message: Message) -> bool:
    cid = message.chat.id
    if cid == glovar.test_group_id:
        return True

    return False


class_c = Filters.create(
    name="Config Channel",
    func=is_config_channel
)

exchange_channel = Filters.create(
    name="Exchange Channel",
    func=is_exchange_channel
)

test_group = Filters.create(
    name="Test Group",
    func=is_test_group
)
