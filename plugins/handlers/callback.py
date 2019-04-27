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
from ..functions.config import commit_change, warn_default, warn_button
from ..functions.etc import thread
from ..functions.telegram import answer_callback, edit_message_reply_markup

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_callback_query()
def answer(client, callback_query):
    try:
        cid = callback_query.message.chat.id
        uid = callback_query.from_user.id
        mid = callback_query.message.message_id
        callback_data = loads(callback_query.data)
        logger.warning(callback_data)
        action = callback_data["a"]
        action_type = callback_data["t"]
        data = callback_data["d"]
        if action != "none":
            config_key = callback_query.message.text.split("\n")[0].split("：")[1]
            if glovar.configs.get(config_key):
                aid = glovar.configs[config_key]["user_id"]
                if uid == aid:
                    if not glovar.configs[config_key]["commit"]:
                        if action == "commit":
                            commit_change(client, config_key)
                        else:
                            config_type = glovar.configs[config_key]["type"]
                            if config_type == "warn":
                                if action == "default":
                                    if data:
                                        warn_default(config_key)
                                    else:
                                        glovar.configs[config_key]["config"]["default"] = False
                                elif action == "limit":
                                    if action_type:
                                        glovar.configs[config_key]["config"]["limit"] = data
                                    else:
                                        thread(answer_callback, (client, callback_query.id, ""))
                                elif action == "mention":
                                    glovar.configs[config_key]["mention"] = data
                                elif action == "report":
                                    if action_type == "auto":
                                        glovar.configs[config_key]["report"]["auto"] = data
                                    elif action_type == "manual":
                                        glovar.configs[config_key]["report"]["manual"] = data

                                markup = warn_button(glovar.configs[config_key]["config"])
                                thread(edit_message_reply_markup, (client, cid, mid, markup))
                else:
                    thread(answer_callback, (client, callback_query.id, "已提交或失效"))
        else:
            thread(answer_callback, (client, callback_query.id, ""))
    except Exception as e:
        logger.warning(f"Answer callback error: {e}", exc_info=True)
