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


def button_captcha(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for CAPTCHA
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="自动免验证",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('auto'))}",
                        callback_data=button_data("auto", None, not config.get('auto'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button captcha error: {e}", exc_info=True)

    return markup


def button_clean(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for CLEAN
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"联系人 {(lambda x: '✅' if x else '☑️')(config.get('con'))}",
                        callback_data=button_data("con", None, not config.get('con'))
                    ),
                    InlineKeyboardButton(
                        text=f"定位 {(lambda x: '✅' if x else '☑️')(config.get('loc'))}",
                        callback_data=button_data("loc", None, not config.get('loc'))
                    ),
                    InlineKeyboardButton(
                        text=f"圆视频 {(lambda x: '✅' if x else '☑️')(config.get('vdn'))}",
                        callback_data=button_data("vdn", None, not config.get('vdn'))
                    ),
                    InlineKeyboardButton(
                        text=f"语音 {(lambda x: '✅' if x else '☑️')(config.get('voi'))}",
                        callback_data=button_data("voi", None, not config.get('voi'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"动态贴纸 {(lambda x: '✅' if x else '☑️')(config.get('ast'))}",
                        callback_data=button_data("ast", None, not config.get('ast'))
                    ),
                    InlineKeyboardButton(
                        text=f"音频 {(lambda x: '✅' if x else '☑️')(config.get('aud'))}",
                        callback_data=button_data("aud", None, not config.get('aud'))
                    ),
                    InlineKeyboardButton(
                        text=f"命令 {(lambda x: '✅' if x else '☑️')(config.get('bmd'))}",
                        callback_data=button_data("bmd", None, not config.get('bmd'))
                    ),
                    InlineKeyboardButton(
                        text=f"文件 {(lambda x: '✅' if x else '☑️')(config.get('doc'))}",
                        callback_data=button_data("doc", None, not config.get('doc'))
                    )
                ],
                [


                    InlineKeyboardButton(
                        text=f"游戏 {(lambda x: '✅' if x else '☑️')(config.get('gam'))}",
                        callback_data=button_data("gam", None, not config.get('gam'))
                    ),
                    InlineKeyboardButton(
                        text=f"动图 {(lambda x: '✅' if x else '☑️')(config.get('gif'))}",
                        callback_data=button_data("gif", None, not config.get('gif'))
                    ),
                    InlineKeyboardButton(
                        text=f"通过 Bot {(lambda x: '✅' if x else '☑️')(config.get('via'))}",
                        callback_data=button_data("via", None, not config.get('via'))
                    ),
                    InlineKeyboardButton(
                        text=f"视频 {(lambda x: '✅' if x else '☑️')(config.get('vdi'))}",
                        callback_data=button_data("vdi", None, not config.get('vdi'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"服务 {(lambda x: '✅' if x else '☑️')(config.get('ser'))}",
                        callback_data=button_data("ser", None, not config.get('ser'))
                    ),
                    InlineKeyboardButton(
                        text=f"贴纸 {(lambda x: '✅' if x else '☑️')(config.get('sti'))}",
                        callback_data=button_data("sti", None, not config.get('sti'))
                    ),
                    InlineKeyboardButton(
                        text=f"推广链接 {(lambda x: '✅' if x else '☑️')(config.get('aff'))}",
                        callback_data=button_data("aff", None, not config.get('aff'))
                    ),
                    InlineKeyboardButton(
                        text=f"执行文件 {(lambda x: '✅' if x else '☑️')(config.get('exe'))}",
                        callback_data=button_data("exe", None, not config.get('exe'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"IM 链接 {(lambda x: '✅' if x else '☑️')(config.get('iml'))}",
                        callback_data=button_data("iml", None, not config.get('iml'))
                    ),
                    InlineKeyboardButton(
                        text=f"短链接 {(lambda x: '✅' if x else '☑️')(config.get('sho'))}",
                        callback_data=button_data("sho", None, not config.get('sho'))
                    ),
                    InlineKeyboardButton(
                        text=f"TG 链接 {(lambda x: '✅' if x else '☑️')(config.get('tgl'))}",
                        callback_data=button_data("tgl", None, not config.get('tgl'))
                    ),
                    InlineKeyboardButton(
                        text=f"TG 代理 {(lambda x: '✅' if x else '☑️')(config.get('tgp'))}",
                        callback_data=button_data("tgp", None, not config.get('tgp'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"二维码{(lambda x: '✅' if x else '☑️')(config.get('qrc'))}",
                        callback_data=button_data("qrc", None, not config.get('qrc'))
                    ),
                    InlineKeyboardButton(
                        text=f"自助删除 {(lambda x: '✅' if x else '☑️')(config.get('sde'))}",
                        callback_data=button_data("sde", None, not config.get('sde'))
                    ),
                    InlineKeyboardButton(
                        text=f"定时清群 {(lambda x: '✅' if x else '☑️')(config.get('tcl'))}",
                        callback_data=button_data("tcl", None, not config.get('tcl'))
                    ),
                    InlineKeyboardButton(
                        text=f"定时贴纸 {(lambda x: '✅' if x else '☑️')(config.get('ttd'))}",
                        callback_data=button_data("ttd", None, not config.get('ttd'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button clean error: {e}", exc_info=True)

    return markup


def button_lang(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for LANG
    markup = None
    try:
        for the_type in ["name", "text"]:
            if not config.get(the_type):
                config[the_type] = {}

            if not config[the_type].get("enable"):
                config[the_type]["enable"] = True

        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="昵称过滤",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config['name']['enable'])}",
                        callback_data=button_data("name", None, not config['name']['enable'])
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="文字过滤",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config['text']['enable'])}",
                        callback_data=button_data("text", None, not config['text']['enable'])
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button lang error: {e}", exc_info=True)

    return markup


def button_long(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for LONG
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="消息字节长度",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{config['limit']}",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '-️' if x > 2000 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x > 2000 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] - 1000)
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '+️' if x < 10000 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x < 10000 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] + 1000)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button long error: {e}", exc_info=True)

    return markup


def button_noflood(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for NOFLOOD
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="5 秒内消息上限",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{config['limit']}",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '-️' if x > 5 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x > 5 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] - 5)
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '+️' if x < 15 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x < 15 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] + 5)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button noflood error: {e}", exc_info=True)

    return markup


def button_noporn(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for NOPORN
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="过滤频道",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('channel'))}",
                        callback_data=button_data("channel", None, not config.get('channel'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button noporn error: {e}", exc_info=True)

    return markup


def button_nospam(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for NOSPAM
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="试验特性",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('auto'))}",
                        callback_data=button_data("auto", None, not config.get('auto'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="消息字节上限",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{config['limit']}",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '-️' if x > 3000 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x > 3000 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] - 1000)
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '+️' if x < 9000 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x < 9000 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] + 1000)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button nospam error: {e}", exc_info=True)

    return markup


def button_tip(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for TIP
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="OT 警告",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('ot'))}",
                        callback_data=button_data("ot", None, not config.get('ot'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="欢迎信息",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('welcome'))}",
                        callback_data=button_data("welcome", None, not config.get('welcome'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="RM 警告",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('rm'))}",
                        callback_data=button_data("rm", None, not config.get('rm'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="自定义关键词",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('custom'))}",
                        callback_data=button_data("custom", None, not config.get('custom'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button tip error: {e}", exc_info=True)

    return markup


def button_user(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for USER
    markup = None
    try:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="订阅列表",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('subscribe'))}",
                        callback_data=button_data("subscribe", None, not config.get('subscribe'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="自助删除",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('dafm'))}",
                        callback_data=button_data("dafm", None, not config.get('dafm'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button user error: {e}", exc_info=True)

    return markup


def button_warn(config: dict) -> Optional[InlineKeyboardMarkup]:
    # Get inline markup for WARN
    markup = None
    try:
        if not config.get("limit"):
            config["limit"] = 3

        if not config.get("report"):
            config["report"] = {}

        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="默认设置",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('default'))}",
                        callback_data=button_data((lambda x: "default" if not x else "none")(config.get('default')),
                                                  None,
                                                  not config.get('default'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="警告上限",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{config['limit']}",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '-️' if x > 2 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x > 2 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] - 1)
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '+️' if x < 5 else '*')(config['limit'])}",
                        callback_data=button_data((lambda x: "limit" if x < 5 else "none")(config['limit']),
                                                  None,
                                                  config['limit'] + 1)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="呼叫管理",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config.get('mention'))}",
                        callback_data=button_data("mention", None, not config.get('mention'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="自动举报",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config['report'].get('auto'))}",
                        callback_data=button_data("report", "auto", not config['report'].get('auto'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="手动举报",
                        callback_data=button_data("none")
                    ),
                    InlineKeyboardButton(
                        text=f"{(lambda x: '✅' if x else '☑️')(config['report'].get('manual'))}",
                        callback_data=button_data("report", "manual", not config['report'].get('manual'))
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="提交",
                        callback_data=button_data("commit")
                    )
                ]
            ]
        )
    except Exception as e:
        logger.warning(f"Button warn error: {e}", exc_info=True)

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
    # Commit the new configuration
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
            edit_message_text(client, glovar.config_channel_id, message_id, text)
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
    try:
        if glovar.configs.get(config_key):
            config_type = glovar.configs[config_key]["type"]
            config_data = glovar.configs[config_key]["config"]
            # For each config type, use different function to generate reply markup buttons
            markup = eval(f"button_{config_type}")(config_data)
            text = get_config_text(config_key)
            text += f"说明：{code('请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效')}"
    except Exception as e:
        logger.warning(f"Get config message error: {e}", exc_info=True)

    return text, markup


def get_config_text(config_key: str) -> str:
    # Get a config session message text prefix
    text = ""
    try:
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
    except Exception as e:
        logger.warning(f"Get config text error: {e}", exc_info=True)

    return text


def set_default(config_key: str) -> bool:
    # Set the config to the default one
    try:
        glovar.configs[config_key]["config"] = deepcopy(glovar.configs[config_key]["default"])

        return True
    except Exception as e:
        logger.warning(f"Set default error: {e}", exc_info=True)

    return False
