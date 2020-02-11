# SCP-079-CONFIG - Manage the settings of each bot
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
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
import pickle
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from threading import Lock
from typing import Dict, List, Union

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
config_channel_id: int = 0
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
aio: Union[bool, str] = ""
backup: Union[bool, str] = ""
date_reset: str = ""
project_link: str = ""
project_name: str = ""
zh_cn: Union[bool, str] = ""

# [encrypt]
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))

    # [channels]
    config_channel_id = int(config["channels"].get("config_channel_id", config_channel_id))
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))

    # [custom]
    aio = config["custom"].get("aio", aio)
    aio = eval(aio)
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    date_reset = config["custom"].get("date_reset", date_reset)
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)

    # [encrypt]
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or config_channel_id == 0
        or critical_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or hide_channel_id == 0
        or test_group_id == 0
        or aio not in {False, True}
        or backup not in {False, True}
        or date_reset in {"", "[DATA EXPUNGED]"}
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or zh_cn not in {False, True}
        or password in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    "admin_group": (zh_cn and "群管理") or "Group Admin",
    # Basic
    "action": (zh_cn and "执行操作") or "Action",
    "colon": (zh_cn and "：") or ": ",
    "description": (zh_cn and "说明") or "Description",
    "reset": (zh_cn and "重置数据") or "Reset Data",
    "rollback": (zh_cn and "数据回滚") or "Rollback",
    "version": (zh_cn and "版本") or "Version",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Group
    "group_id": (zh_cn and "群组 ID") or "Group ID",
    "group_name": (zh_cn and "群组名称") or "Group Name",
    # Record
    "project": (zh_cn and "项目编号") or "Project",
    "status": (zh_cn and "状态") or "Status",
    # Common
    "default_config": (zh_cn and "默认设置") or "Default Settings",
    "delete": (zh_cn and "协助删除") or "Help Delete",
    "restrict": (zh_cn and "禁言模式") or "Restriction Mode",
    "commit": (zh_cn and "提交") or "Commit",
    # CAPTCHA
    "ban": (zh_cn and "封禁模式") or "Ban Mode",
    "forgive": (zh_cn and "自动解禁") or "Auto Forgive",
    "hint": (zh_cn and "入群提示") or "Hint for New Joined User",
    "pass": (zh_cn and "自动免验证") or "Auto Pass",
    "manual": (zh_cn and "仅手动") or "Manual Only",
    # CLEAN
    "friend": (zh_cn and "放行友链") or "Bypass Friend Links",
    "con": (zh_cn and "联系人") or "Contact",
    "loc": (zh_cn and "定位") or "Location",
    "vdn": (zh_cn and "圆视频") or "Round Video",
    "voi": (zh_cn and "语音") or "Voice",
    "ast": (zh_cn and "动态贴纸") or "Animated Sticker",
    "aud": (zh_cn and "音频") or "Audio",
    "bmd": (zh_cn and "命令") or "Bot Command",
    "doc": (zh_cn and "文件") or "Document",
    "gam": (zh_cn and "游戏") or "Game",
    "gif": (zh_cn and "动图") or "GIF",
    "via": (zh_cn and "通过 Bot") or "Via Bot",
    "vid": (zh_cn and "视频") or "Video",
    "ser": (zh_cn and "服务") or "Service",
    "sti": (zh_cn and "贴纸") or "Sticker",
    "aff": (zh_cn and "推广链接") or "AFF Link",
    "emo": (zh_cn and "多 Emoji") or "Too Many Emoji Characters",
    "exe": (zh_cn and "执行文件") or "Executable File",
    "iml": (zh_cn and "IM 链接") or "IM Link",
    "pho": (zh_cn and "电话号码") or "Phone Number",
    "sho": (zh_cn and "短链接") or "Short Link",
    "tgl": (zh_cn and "TG 链接") or "Telegram Link",
    "tgp": (zh_cn and "TG 代理") or "Telegram Proxy",
    "qrc": (zh_cn and "二维码") or "QR Code",
    "sde": (zh_cn and "自助删除") or "Self Delete Messages",
    "tcl": (zh_cn and "定时清群") or "Clean Members Everyday",
    "ttd": (zh_cn and "定时贴纸") or "Schedule to Delete Stickers",
    # LANG
    "name_default": (zh_cn and "默认名称设置") or "Default Name Setting",
    "name_enable": (zh_cn and "检查消息名称") or "Check Message's Name",
    "text_default": (zh_cn and "默认文字设置") or "Default text Setting",
    "text_enable": (zh_cn and "检查消息文字") or "Check Message's Text",
    "sticker_default": (zh_cn and "默认贴纸设置") or "Default Sticker Setting",
    "sticker_enable": (zh_cn and "检查贴纸标题") or "Check Sticker's Title",
    "bio_default": (zh_cn and "默认简介设置") or "Default Bio Setting",
    "bio_enable": (zh_cn and "检查用户简介") or "Check User's Bio",
    "spc": (zh_cn and "特殊中文") or "Special Chinese Characters",
    "spe": (zh_cn and "特殊英文") or "Special English Characters",
    # LONG
    "long_limit": (zh_cn and "消息字节上限") or "Bytes Length Limit",
    # NOFLOOD
    "noflood_time": (zh_cn and "检测时间秒数") or "Time in seconds",
    "noflood_limit": (zh_cn and "消息条数上限") or "Message Count Limit",
    "noflood_purge": (zh_cn and "清除所有消息") or "Purge All Messages",
    # NOPORN
    "noporn_channel": (zh_cn and "过滤频道") or "Filter Restricted Channel Message",
    # NOSPAM
    "bio": (zh_cn and "简介检查") or "Bio Examination",
    "bot": (zh_cn and "阻止机器人进群") or "Prevent Bot from Joining",
    "new": (zh_cn and "新入群限制") or "Limit the New Joined User",
    "deleter": (zh_cn and "仅删除") or "Delete Only",
    "reporter": (zh_cn and "仅举报") or "Report Only",
    "ml": (zh_cn and "机器学习") or "Machine Learning",
    # TIP
    "captcha": (zh_cn and "过审欢迎") or "Welcome After CAPTCHA",
    "clean": (zh_cn and "无痕模式") or "Clean Mode",
    "resend": (zh_cn and "每日重发入群链接") or "Resend Invite Link Everyday",
    "channel": (zh_cn and "入群频道") or "Entry Channel",
    "keyword": (zh_cn and "关键词提示") or "Custom Keywords",
    "ot": (zh_cn and "OT 警告") or "OT Warning by Members",
    "rm": (zh_cn and "RM 警告") or "RM Jokes Warning",
    "welcome": (zh_cn and "欢迎信息") or "Welcome Message",
    # USER
    "gb": (zh_cn and "全局封禁") or "Global Ban",
    "gr": (zh_cn and "全局禁言") or "Global Restrict",
    "gd": (zh_cn and "全局删除") or "Global Delete",
    "sb": (zh_cn and "订阅封禁") or "Subscribe Ban",
    "sr": (zh_cn and "订阅禁言") or "Subscribe Restrict",
    "sd": (zh_cn and "订阅删除") or "Subscribe Delete",
    # WARN
    "warn_limit": (zh_cn and "警告上限") or "Warn Limit",
    "warn_admin": (zh_cn and "呼叫管理") or "Call Admins",
    "report_auto": (zh_cn and "自动举报") or "Auto Report",
    "report_manual": (zh_cn and "手动举报") or "Manual Report",
    # Special
    "config_code": (zh_cn and "设置编号") or "Config",
    "config_description": ((zh_cn and "请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效")
                           or ("Please change settings here. If the it is completed, please click Submit. "
                               "This session will expire after 5 minutes")),
    "committed": (zh_cn and "已更新设置") or "Committed",
    "commit_change": (zh_cn and "提交设置") or "Commit Change",
    "expired": (zh_cn and "会话已失效") or "Session Expired",
    "invalid_key": (zh_cn and "已提交或失效") or "Committed or Invalid Session",
    "target": (zh_cn and "针对项目") or "Target Project"
}

# Init

all_commands: List[str] = ["version"]

locks: Dict[str, Lock] = {
    "receive": Lock()
}

sender: str = "CONFIG"

should_hide: bool = False

version: str = "0.2.7"

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)


# Init data variables

configs: Dict[str, Dict[str, Union[bool, int, dict, str]]] = {}
# configs = {
#     "random": {
#         "type": "warn",
#         "lock": False,
#         "commit": False,
#         "time": 1512345678,
#         "group_id": -10012345678,
#         "group_name": "Group Name",
#         "group_link": "link to group",
#         "user_id": 12345678,
#         "message_id": 123,
#         "config": {
#             "default": False,
#             "lock": 1512345678,
#             "delete": True,
#             "limit": 3,
#             "mention": True,
#             "report": {
#                 "auto": True,
#                 "manual": True
#             }
#         },
#         "default": {
#             "default": True,
#             "lock": 0,
#             "delete": True,
#             "limit": 3,
#             "mention": True,
#             "report": {
#                 "auto": False,
#                 "manual": True
#             }
#         }
#     }
# }

# Load data
file_list: List[str] = ["configs"]

for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", 'rb') as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", 'wb') as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"data/.{file}", 'rb') as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
