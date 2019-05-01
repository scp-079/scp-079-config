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
from typing import Optional

from pyrogram import Client, InlineKeyboardButton, InlineKeyboardMarkup

from .. import glovar
from .channel import share_data
from .etc import button_data, code, general_link, thread
from .telegram import edit_message_text

# Enable logging
logger = logging.getLogger(__name__)


def check_commit(client: Client, config_key: str) -> bool:
    # Check whether the config session is committed or not
    try:
        if glovar.configs.get(config_key):
            if not glovar.configs[config_key]["commit"]:
                # If it is not committed, edit the session message to update the status (invalid)
                text = get_config_text(config_key)
                text += f"状态：{code('会话已失效')}"
                mid = glovar.configs[config_key]["message_id"]
                thread(edit_message_text, (client, glovar.config_channel_id, mid, text))

            # Pop this config data
            glovar.configs.pop(config_key, "")
            return True
    except Exception as e:
        logger.warning(f"Check commit error: {e}", exc_info=True)

    return False


def commit_change(client: Client, config_key: str) -> bool:
    try:
        if glovar.configs.get(config_key):
            # Change commit status
            glovar.configs[config_key]["commit"] = True
            # Use config type to get the right receiver
            config_type = glovar.configs[config_key]["type"]
            group_id = glovar.configs[config_key]["group_id"]
            # The config session message id
            message_id = glovar.configs[config_key]["message_id"]
            config_data = glovar.configs[config_key]["config"]
            # Edit config session message
            text = get_config_text(config_key)
            text += f"结果：{code('已更新设置')}"
            thread(edit_message_text, (client, glovar.config_channel_id, message_id, text))
            # Commit changes to exchange channel
            receivers = [config_type.upper()]
            share_data(
                client=client,
                receivers=receivers,
                action="config",
                action_type="commit",
                data={
                    "group_id": group_id,
                    "config": config_data
                }
            )
            return True
    except Exception as e:
        logger.warning(f"Commit change error: {e}")

    return False


def get_config_message(config_key: str) -> (str, Optional[InlineKeyboardMarkup]):
    # Get a config session message (text + reply markup)
    text = ""
    markup = None
    if glovar.configs.get(config_key):
        config_type = glovar.configs[config_key]["type"]
        config_data = glovar.configs[config_key]["config"]
        # For each config type, use different function to generate reply markup buttons
        markup = eval(f"{config_type}_button")(config_data)
        text = get_config_text(config_key)
        text += f"说明：{code('请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效')}"

    return text, markup


def get_config_text(config_key: str) -> str:
    # Get a config session message text
    project_name = glovar.configs[config_key]["project_name"]
    project_link = glovar.configs[config_key]["project_link"]
    group_id = glovar.configs[config_key]["group_id"]
    group_name = glovar.configs[config_key]["group_name"]
    group_link = glovar.configs[config_key]["group_link"]
    user_id = glovar.configs[config_key]["user_id"]

    text = (f"设置编号：{code(config_key)}\n"
            f"项目编号：{general_link(project_name, project_link)}\n"
            f"群组 ID：{code(group_id)}\n"
            f"群组名称：{general_link(group_name, group_link)}\n"
            f"用户 ID：{code(user_id)}\n")

    return text


def noporn_button(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for NOPORN
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "默认设置",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                    callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                              None,
                                              not config.get('default'))
                )
            ],
            [
                InlineKeyboardButton(
                    "过滤频道",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('channel'))}",
                    callback_data=button_data("channel", None, not config.get('channel'))
                )
            ],
            [
                InlineKeyboardButton(
                    "媒体复查",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('recheck'))}",
                    callback_data=button_data("recheck", None, not config.get('recheck'))
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


def set_default(config_key: str) -> bool:
    glovar.configs[config_key]["config"] = deepcopy(glovar.configs[config_key]["default"])

    return True


def warn_button(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for WARN
    if not config.get("limit"):
        config["limit"] = 3

    if not config.get("report"):
        config["report"] = {}

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "默认设置",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                    callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                              None,
                                              not config.get('default'))
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
                    f"{(lambda x: '✅' if x else '☑️')(config.get('mention'))}",
                    callback_data=button_data("mention", None, not config.get('mention'))
                )
            ],
            [
                InlineKeyboardButton(
                    "自动举报",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['report'].get('auto'))}",
                    callback_data=button_data("report", "auto", not config['report'].get('auto'))
                )
            ],
            [
                InlineKeyboardButton(
                    "手动举报",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config['report'].get('manual'))}",
                    callback_data=button_data("report", "manual", not config['report'].get('manual'))
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
