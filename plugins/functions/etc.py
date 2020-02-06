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
from html import escape
from json import dumps
from random import choice, uniform
from string import ascii_letters, digits
from threading import Thread, Timer
from time import sleep, time
from typing import Any, Callable, Optional, Union

from pyrogram import Message
from pyrogram.errors import FloodWait

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def bold(text: Any) -> str:
    # Get a bold text
    try:
        text = str(text).strip()

        if text:
            return f"<b>{escape(text)}</b>"
    except Exception as e:
        logger.warning(f"Bold error: {e}", exc_info=True)

    return ""


def button_data(action: str, action_type: str = None, data: Union[int, str] = None) -> Optional[bytes]:
    # Get a button's bytes data
    result = None
    try:
        button = {
            "a": action,
            "t": action_type,
            "d": data
        }
        result = dumps(button).replace(" ", "").encode("utf-8")
    except Exception as e:
        logger.warning(f"Button data error: {e}", exc_info=True)

    return result


def code(text: Any) -> str:
    # Get a code text
    try:
        text = str(text).strip()

        if text:
            return f"<code>{escape(text)}</code>"
    except Exception as e:
        logger.warning(f"Code error: {e}", exc_info=True)

    return ""


def code_block(text: Any) -> str:
    # Get a code block text
    try:
        text = str(text).rstrip()

        if text:
            return f"<pre>{escape(text)}</pre>"
    except Exception as e:
        logger.warning(f"Code block error: {e}", exc_info=True)

    return ""


def delay(secs: int, target: Callable, args: list) -> bool:
    # Call a function with delay
    try:
        t = Timer(secs, target, args)
        t.daemon = True
        t.start()

        return True
    except Exception as e:
        logger.warning(f"Delay error: {e}", exc_info=True)

    return False


def general_link(text: Union[int, str], link: str) -> str:
    # Get a general link
    result = ""
    try:
        text = str(text).strip()
        link = link.strip()

        if text and link:
            result = f'<a href="{link}">{escape(text)}</a>'
    except Exception as e:
        logger.warning(f"General link error: {e}", exc_info=True)

    return result


def get_channel_link(message: Union[int, Message]) -> str:
    # Get a channel reference link
    text = ""
    try:
        text = "https://t.me/"

        if isinstance(message, int):
            text += f"c/{str(message)[4:]}"
        else:
            if message.chat.username:
                text += f"{message.chat.username}"
            else:
                cid = message.chat.id
                text += f"c/{str(cid)[4:]}"
    except Exception as e:
        logger.warning(f"Get channel link error: {e}", exc_info=True)

    return text


def get_now() -> int:
    # Get time for now
    result = 0
    try:
        result = int(time())
    except Exception as e:
        logger.warning(f"Get now error: {e}", exc_info=True)

    return result


def get_text(message: Message) -> str:
    # Get message's text
    text = ""
    try:
        if not message:
            return ""

        the_text = message.text or message.caption

        if the_text:
            text += the_text
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return text


def lang(text: str) -> str:
    # Get the text
    result = ""
    try:
        result = glovar.lang.get(text, text)
    except Exception as e:
        logger.warning(f"Lang error: {e}", exc_info=True)

    return result


def mention_id(uid: int) -> str:
    # Get a ID mention string
    result = ""
    try:
        result = general_link(f"{uid}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention id error: {e}", exc_info=True)

    return result


def message_link(message: Message) -> str:
    # Get a message link in a channel
    text = ""
    try:
        mid = message.message_id
        text = f"{get_channel_link(message)}/{mid}"
    except Exception as e:
        logger.warning(f"Message link error: {e}", exc_info=True)

    return text


def random_str(i: int) -> str:
    # Get a random string
    text = ""
    try:
        text = "".join(choice(ascii_letters + digits) for _ in range(i))
    except Exception as e:
        logger.warning(f"Random str error: {e}", exc_info=True)

    return text


def thread(target: Callable, args: tuple) -> bool:
    # Call a function using thread
    try:
        t = Thread(target=target, args=args)
        t.daemon = True
        t.start()

        return True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return False


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    try:
        sleep(e.x + uniform(0.5, 1.0))

        return True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return False
