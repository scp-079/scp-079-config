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
import pickle
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from typing import Dict, List, Union

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
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
project_link: str = ""
project_name: str = ""
reset_day: str = ""

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
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    reset_day = config["custom"].get("reset_day", reset_day)
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
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or reset_day in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Init

all_commands: List[str] = ["version"]

sender: str = "CONFIG"

should_hide: bool = False

version: str = "0.1.7"

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
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
