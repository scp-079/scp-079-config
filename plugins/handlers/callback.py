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

from pyrogram import Client

from .. import glovar
from ..functions.config import commit_change, get_config_message, set_default
from ..functions.etc import thread
from ..functions.telegram import answer_callback, edit_message_reply_markup

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_callback_query()
def answer(client, callback_query):
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
        if action != "none":
            config_key = callback_query.message.text.split("\n")[0].split("：")[1]
            if glovar.configs.get(config_key):
                # Check whether the config is locked
                if not glovar.configs[config_key].get("locked"):
                    try:
                        # Lock the config status until bot answers callback, avoid multiple responses
                        glovar.configs[config_key]["locked"] = True
                        # Check user's permission with this config session
                        aid = glovar.configs[config_key]["user_id"]
                        if uid == aid:
                            # Commit the changes if user press commit button, else change some settings
                            if action == "commit":
                                commit_change(client, config_key)
                            else:
                                config_type = glovar.configs[config_key]["type"]
                                if action == "default":
                                    set_default(config_key)
                                else:
                                    glovar.configs[config_key]["config"]["default"] = False
                                    # CAPTCHA
                                    if config_type == "captcha":
                                        glovar.configs[config_key]["config"][action] = data
                                    # CLEAN
                                    elif config_type == "clean":
                                        glovar.configs[config_key]["config"][action] = data
                                    # LANG
                                    elif config_type == "lang":
                                        glovar.configs[config_key]["config"][action] = data
                                        if (glovar.configs[config_key]["config"]["name"]
                                                and glovar.configs[config_key]["config"]["text"]):
                                            glovar.configs[config_key]["default"] = True
                                    # NOFLOOD
                                    elif config_type == "noflood":
                                        if action == "limit":
                                            glovar.configs[config_key]["config"][action] = data
                                    # NOPORN
                                    elif config_type == "noporn":
                                        glovar.configs[config_key]["config"][action] = data
                                    # NOSPAM
                                    elif config_type == "nospam":
                                        glovar.configs[config_key]["config"][action] = data
                                    # WARN
                                    elif config_type == "warn":
                                        if action in {"limit", "mention"}:
                                            glovar.configs[config_key]["config"][action] = data
                                        elif action == "report":
                                            # Key "report" was created when generate the button first time
                                            glovar.configs[config_key]["config"]["report"][action_type] = data

                                _, markup = get_config_message(config_key)
                                edit_message_reply_markup(client, cid, mid, markup)
                                thread(answer_callback, (client, callback_query.id, ""))
                    finally:
                        glovar.configs[config_key]["locked"] = False
                else:
                    thread(answer_callback, (client, callback_query.id, ""))
            else:
                thread(answer_callback, (client, callback_query.id, "已提交或失效"))
        else:
            thread(answer_callback, (client, callback_query.id, ""))
    except Exception as e:
        logger.warning(f"Answer callback error: {e}", exc_info=True)
