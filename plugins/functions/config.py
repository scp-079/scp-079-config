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
from typing import Optional

from pyrogram import Client, InlineKeyboardButton, InlineKeyboardMarkup

from .. import glovar
from .etc import button_data, code, general_link, send_data, thread
from .telegram import edit_message_text, send_message

# Enable logging
logger = logging.getLogger(__name__)


def check_commit(client: Client, config_key: str) -> bool:
    try:
        if glovar.configs.get(config_key):
            if not glovar.configs[config_key]["commit"]:
                text = get_config_text(config_key)
                text += f"状态：{code('会话已失效')}"
                mid = glovar.configs[config_key]["message_id"]
                thread(edit_message_text, (client, glovar.config_channel_id, mid, text))

            return True
    except Exception as e:
        logger.warning(f"Check commit error: {e}", exc_info=True)

    return False


def commit_change(client: Client, config_key: str) -> bool:
    try:
        if glovar.configs.get(config_key):
            glovar.configs[config_key]["commit"] = True
            config_type = glovar.configs[config_key]["type"]
            group_id = glovar.configs[config_key]["group_id"]
            message_id = glovar.configs[config_key]["message_id"]
            config_data = glovar.configs[config_key]["config"]
            # Edit config message
            text = get_config_text(config_key)
            text += f"结果：{code('已更新设置')}"
            thread(edit_message_text, (client, glovar.config_channel_id, message_id, text))
            # Commit changes to exchange channel
            receivers = []
            if config_type == "warn":
                receivers = ["WARN"]

            exchange_text = send_data(
                sender="CONFIG",
                receivers=receivers,
                action="config",
                action_type="commit",
                data={
                    "group_id": group_id,
                    "config": config_data
                }
            )
            thread(send_message, (client, glovar.exchange_channel_id, exchange_text))
            return True
    except Exception as e:
        logger.warning(f"Commit change error: {e}")

    return False


def get_config_message(config_key: str) -> (str, Optional[InlineKeyboardMarkup]):
    text = ""
    markup = None
    if glovar.configs.get(config_key):
        config_type = glovar.configs[config_key]["type"]
        config_data = glovar.configs[config_key]["config"]
        if config_type == "warn":
            markup = warn_button(config_data)

        text = get_config_text(config_key)
        text += f"说明：{code('请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效')}"

    return text, markup


def get_config_text(config_key: str) -> str:
    config_type = glovar.configs[config_key]["type"]
    project_name = ""
    project_link = ""
    group_id = glovar.configs[config_key]["group_id"]
    group_name = glovar.configs[config_key]["group_name"]
    group_link = glovar.configs[config_key]["group_link"]
    user_id = glovar.configs[config_key]["user_id"]
    if config_type == "warn":
        project_name = glovar.warn_name
        project_link = glovar.warn_link

    text = (f"设置编号：{code(config_key)}\n"
            f"项目编号：{general_link(project_name, project_link)}\n"
            f"群组 ID：{code(group_id)}\n"
            f"群组名称：{general_link(group_name, group_link)}\n"
            f"用户 ID：{code(user_id)}\n")

    return text


def warn_button(config: dict) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "默认设置",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['default'])}",
                    callback_data=button_data("default", None, not config['default'])
                )
            ],
            [
                InlineKeyboardButton(
                    "警告上限",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{config['limit']}",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '-️' if x > 2 else '*')(config['limit'])}",
                    callback_data=button_data("limit",
                                              (lambda x: "set" if x > 2 else None)(config['limit']),
                                              config['limit'] - 1)
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '+️' if x < 5 else '*')(config['limit'])}",
                    callback_data=button_data("limit",
                                              (lambda x: "set" if x < 5 else None)(config['limit']),
                                              config['limit'] + 1)
                )
            ],
            [
                InlineKeyboardButton(
                    "呼叫管理",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['mention'])}",
                    callback_data=button_data("mention", None, not config['mention'])
                )
            ],
            [
                InlineKeyboardButton(
                    "自动举报",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['report']['auto'])}",
                    callback_data=button_data("report", "auto", not config['report']['auto'])
                )
            ],
            [
                InlineKeyboardButton(
                    "手动举报",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['report']['manual'])}",
                    callback_data=button_data("report", "manual", not config['report']['manual'])
                )
            ],
            [
                InlineKeyboardButton(
                    "提交",
                    callback_data=button_data("commit")
                )
            ]
        ]
    )

    return markup


def warn_default(config_key: str) -> bool:
    if glovar.configs.get(config_key):
        glovar.configs[config_key]["config"] = {
            "default": True,
            "limit": 3,
            "locked": 0,
            "mention": False,
            "report": {
                "auto": False,
                "manual": False
            }
        }

    return True
