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
from copy import deepcopy
from json import loads

from pyrogram import Client, CallbackQuery

from .. import glovar
from ..functions.config import commit_change, get_config_message, set_default
from ..functions.etc import lang, thread
from ..functions.file import save
from ..functions.filters import config_channel
from ..functions.telegram import answer_callback, edit_message_reply_markup

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_callback_query(config_channel)
def answer(client: Client, callback_query: CallbackQuery) -> bool:
    # Answer the callback query
    try:
        # Basic data about this callback
        cid = callback_query.message.chat.id
        uid = callback_query.from_user.id
        mid = callback_query.message.message_id
        callback_data = loads(callback_query.data)
        action = callback_data["a"]
        action_type = callback_data["t"]
        data = callback_data["d"]

        # Answer the callback
        if action == "none":
            thread(answer_callback, (client, callback_query.id, ""))
            return True

        # Get the key
        key = callback_query.message.text.split("\n")[0].split("：")[1]

        # Check the key
        if not glovar.configs.get(key):
            thread(answer_callback, (client, callback_query.id, lang("invalid_key")))
            return True

        # Check user's permission with this config session
        aid = glovar.configs[key]["user_id"]
        if uid != aid:
            return True

        # Check whether the config is locked
        if glovar.configs[key]["lock"] or glovar.configs[key]["commit"]:
            return True

        try:
            # Lock the config status until bot answers callback, avoid multiple responses
            glovar.configs[key]["lock"] = True

            # Commit the changes if user press commit button, else change some settings
            if action == "commit":
                commit_change(client, key)
                return True

            # Not default settings
            glovar.configs[key]["config"]["default"] = False
            config_type = glovar.configs[key]["type"]

            # Set to default settings
            if action == "default":
                set_default(key)

            # CAPTCHA
            elif config_type == "captcha":
                glovar.configs[key]["config"][action] = data

            # CLEAN
            elif config_type == "clean":
                glovar.configs[key]["config"][action] = data

            # LANG
            elif config_type == "lang":
                if action in {"name", "text", "sticker"}:
                    if action_type == "enable":
                        if not glovar.configs[key]["config"].get(action, {}):
                            glovar.configs[key]["config"][action] = {}
                        glovar.configs[key]["config"][action]["default"] = False
                        glovar.configs[key]["config"][action][action_type] = data
                    elif action_type == "default":
                        default_config = deepcopy(glovar.configs[key]["default"][action])
                        glovar.configs[key]["config"][action] = default_config
                else:
                    glovar.configs[key]["config"][action] = data

            # LONG
            elif config_type == "long":
                glovar.configs[key]["config"][action] = data

            # NOFLOOD
            elif config_type == "noflood":
                glovar.configs[key]["config"][action] = data

            # NOPORN
            elif config_type == "noporn":
                glovar.configs[key]["config"][action] = data

            # NOSPAM
            elif config_type == "nospam":
                glovar.configs[key]["config"][action] = data

                config_list = ["deleter", "reporter"]
                if action in config_list and data:
                    config_list.remove(action)
                    for other in config_list:
                        glovar.configs[key]["config"][other] = False

            # RECHECK
            elif config_type == "recheck":
                glovar.configs[key]["config"][action] = data

            # TIP
            elif config_type == "tip":
                glovar.configs[key]["config"][action] = data

            # USER
            elif config_type == "user":
                glovar.configs[key]["config"][action] = data

                config_list = ["gb", "gr", "gd"]
                if action in config_list and data:
                    config_list.remove(action)
                    for other in config_list:
                        glovar.configs[key]["config"][other] = False

                config_list = ["sb", "sr", "sd"]
                if action in config_list and data:
                    config_list.remove(action)
                    for other in config_list:
                        glovar.configs[key]["config"][other] = False

            # WARN
            elif config_type == "warn":
                if action in {"delete", "restrict", "limit", "mention"}:
                    glovar.configs[key]["config"][action] = data
                elif action == "report":
                    if not glovar.configs[key]["config"].get("report", {}):
                        glovar.configs[key]["config"]["report"] = {}
                    glovar.configs[key]["config"]["report"][action_type] = data

            _, markup = get_config_message(key)
            edit_message_reply_markup(client, cid, mid, markup)
        finally:
            glovar.configs[key]["lock"] = False
            save("configs")
            thread(answer_callback, (client, callback_query.id, ""))

        return True
    except Exception as e:
        logger.warning(f"Answer callback error: {e}", exc_info=True)

    return False
