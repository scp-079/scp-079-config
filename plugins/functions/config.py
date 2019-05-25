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


def button_captcha(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for CAPTCHA
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
                    "自动免验证",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('auto'))}",
                    callback_data=button_data("auto", None, not config.get('auto'))
                )
            ]
        ]
    )

    return markup


def button_clean(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for CLEAN
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
                    f"联系人 {(lambda x: '✅' if x else '☑️')(config.get('con'))}",
                    callback_data=button_data("con", None, not config.get('con'))
                ),
                InlineKeyboardButton(
                    f"通过 Bot {(lambda x: '✅' if x else '☑️')(config.get('via'))}",
                    callback_data=button_data("via", None, not config.get('via'))
                ),
                InlineKeyboardButton(
                    f"动图 {(lambda x: '✅' if x else '☑️')(config.get('ani'))}",
                    callback_data=button_data("ani", None, not config.get('ani'))
                ),
                InlineKeyboardButton(
                    f"命令 {(lambda x: '✅' if x else '☑️')(config.get('bmd'))}",
                    callback_data=button_data("bmd", None, not config.get('bmd'))
                )
            ],
            [
                InlineKeyboardButton(
                    f"视频 {(lambda x: '✅' if x else '☑️')(config.get('vdi'))}",
                    callback_data=button_data("vdi", None, not config.get('vdi'))
                ),
                InlineKeyboardButton(
                    f"短视频 {(lambda x: '✅' if x else '☑️')(config.get('vdn'))}",
                    callback_data=button_data("vdn", None, not config.get('vdn'))
                ),
                InlineKeyboardButton(
                    f"贴纸 {(lambda x: '✅' if x else '☑️')(config.get('sti'))}",
                    callback_data=button_data("sti", None, not config.get('sti'))
                ),
                InlineKeyboardButton(
                    f"图片 {(lambda x: '✅' if x else '☑️')(config.get('pho'))}",
                    callback_data=button_data("pho", None, not config.get('pho'))
                )
            ],
            [
                InlineKeyboardButton(
                    f"音频 {(lambda x: '✅' if x else '☑️')(config.get('aud'))}",
                    callback_data=button_data("aud", None, not config.get('aud'))
                ),
                InlineKeyboardButton(
                    f"语音 {(lambda x: '✅' if x else '☑️')(config.get('voi'))}",
                    callback_data=button_data("voi", None, not config.get('voi'))
                ),
                InlineKeyboardButton(
                    f"游戏 {(lambda x: '✅' if x else '☑️')(config.get('gam'))}",
                    callback_data=button_data("gam", None, not config.get('gam'))
                ),
                InlineKeyboardButton(
                    f"服务 {(lambda x: '✅' if x else '☑️')(config.get('ser'))}",
                    callback_data=button_data("url", None, not config.get('ser'))
                )
            ],
            [
                InlineKeyboardButton(
                    f"定时动图 {(lambda x: '✅' if x else '☑️')(config.get('tan'))}",
                    callback_data=button_data("tan", None, not config.get('tan'))
                ),
                InlineKeyboardButton(
                    f"定时贴纸 {(lambda x: '✅' if x else '☑️')(config.get('tst'))}",
                    callback_data=button_data("tst", None, not config.get('tst'))
                ),
                InlineKeyboardButton(
                    f"定位 {(lambda x: '✅' if x else '☑️')(config.get('loc'))}",
                    callback_data=button_data("loc", None, not config.get('loc'))
                ),
                InlineKeyboardButton(
                    f"文件 {(lambda x: '✅' if x else '☑️')(config.get('doc'))}",
                    callback_data=button_data("doc", None, not config.get('doc'))
                )
            ],
            [
                InlineKeyboardButton(
                    f"EXE APK{(lambda x: '✅' if x else '☑️')(config.get('exe'))}",
                    callback_data=button_data("exe", None, not config.get('exe'))
                ),
                InlineKeyboardButton(
                    f"BAT CMD{(lambda x: '✅' if x else '☑️')(config.get('bat'))}",
                    callback_data=button_data("bat", None, not config.get('bat'))
                ),
                InlineKeyboardButton(
                    f"AFF 链接{(lambda x: '✅' if x else '☑️')(config.get('aff'))}",
                    callback_data=button_data("aff", None, not config.get('aff'))
                ),
                InlineKeyboardButton(
                    f"短链接{(lambda x: '✅' if x else '☑️')(config.get('cmd'))}",
                    callback_data=button_data("sho", None, not config.get('sho'))
                )
            ],
            [
                InlineKeyboardButton(
                    f"TG 链接 {(lambda x: '✅' if x else '☑️')(config.get('tgl'))}",
                    callback_data=button_data("tgl", None, not config.get('tgl'))
                ),
                InlineKeyboardButton(
                    f"TG 代理 {(lambda x: '✅' if x else '☑️')(config.get('tgp'))}",
                    callback_data=button_data("tgp", None, not config.get('tgp'))
                ),
                InlineKeyboardButton(
                    f"国内 IM{(lambda x: '✅' if x else '☑️')(config.get('cim'))}",
                    callback_data=button_data("cim", None, not config.get('cim'))
                ),
                InlineKeyboardButton(
                    f"二维码{(lambda x: '✅' if x else '☑️')(config.get('qrc'))}",
                    callback_data=button_data("qrc", None, not config.get('qrc'))
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


def button_lang(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for LANG
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
                    "昵称默认",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('name'))}",
                    callback_data=button_data("name", None, not config.get('name'))
                )
            ],
            [
                InlineKeyboardButton(
                    "文字默认",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('text'))}",
                    callback_data=button_data("text", None, not config.get('text'))
                )
            ]
        ]
    )

    return markup


def button_noflood(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for NOFLOOD
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
                    "10 秒内消息上限",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{config['limit']}",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '-️' if x > 2 else '*')(config['limit'])}",
                    callback_data=button_data((lambda x: "limit" if x > 10 else "none")(config['limit']),
                                              None,
                                              config['limit'] - 10)
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '+️' if x < 5 else '*')(config['limit'])}",
                    callback_data=button_data((lambda x: "limit" if x < 50 else "none")(config['limit']),
                                              None,
                                              config['limit'] + 10)
                )
            ]
        ]
    )

    return markup


def button_noporn(config: dict) -> InlineKeyboardMarkup:
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


def button_nospam(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for NOSPAM
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
                    "试验特性",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('auto'))}",
                    callback_data=button_data("auto", None, not config.get('auto'))
                )
            ]
        ]
    )

    return markup


def button_tip(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for TIP
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
                    "OT 警告",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('ot'))}",
                    callback_data=button_data("ot", None, not config.get('ot'))
                )
            ],
            [
                InlineKeyboardButton(
                    "欢迎信息",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('welcome'))}",
                    callback_data=button_data("welcome", None, not config.get('welcome'))
                )
            ],
            [
                InlineKeyboardButton(
                    "RM 警告",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('rm'))}",
                    callback_data=button_data("rm", None, not config.get('rm'))
                )
            ],
            [
                InlineKeyboardButton(
                    "自定义关键词",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('custom'))}",
                    callback_data=button_data("custom", None, not config.get('custom'))
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


def button_user(config: dict) -> InlineKeyboardMarkup:
    # Get inline markup for USER
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
                    "订阅列表",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('subscribe'))}",
                    callback_data=button_data("subscribe", None, not config.get('subscribe'))
                )
            ],
            [
                InlineKeyboardButton(
                    "自助删除",
                    callback_data=button_data("none")
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '✅' if x else '☑️')(config.get('dafm'))}",
                    callback_data=button_data("dafm", None, not config.get('dafm'))
                )
            ]
        ]
    )

    return markup


def button_warn(config: dict) -> InlineKeyboardMarkup:
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
                    callback_data=button_data((lambda x: "limit" if x > 2 else "none")(config['limit']),
                                              None,
                                              config['limit'] - 1)
                ),
                InlineKeyboardButton(
                    f"{(lambda x: '+️' if x < 5 else '*')(config['limit'])}",
                    callback_data=button_data((lambda x: "limit" if x < 5 else "none")(config['limit']),
                                              None,
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
        markup = eval(f"button_{config_type}")(config_data)
        text = get_config_text(config_key)
        text += f"说明：{code('请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效')}"

    return text, markup


def get_config_text(config_key: str) -> str:
    # Get a config session message text prefix
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


def set_default(config_key: str) -> bool:
    glovar.configs[config_key]["config"] = deepcopy(glovar.configs[config_key]["default"])

    return True
