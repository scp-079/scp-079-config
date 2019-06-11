# SCP-079-CONFIG

This bot is used to manage settings for each bot.

## How to use

See [this article](https://scp-079.org/config/).

## To Do List

- [x] Support SCP-079-WARN
- [x] Support SCP-079-NOPORN
- [x] Support SCP-079-CLEAN
- [x] Support SCP-079-LANG
- [x] Support SCP-079-NOFLOOD
- [x] Support SCP-079-CAPTCHA
- [x] Support SCP-079-NOSPAM
- [x] Support SCP-079-TIP
- [x] Support SCP-079-USER
- [x] Support SCP-079-LONG

## Requirements

- Python 3.6 or higher.
- `requirements.txt` ： APScheduler pyrogram[fast]

## Files

- plugins
    - functions
        - `channel.py` : Send messages to channel
        - `config.py` : Generate config session message
        - `etc.py` : Miscellaneous
        - `filters.py` : Some filters
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
    - handlers
        - `callback.py` : Handle callbacks
        - `command` : Handle commands
        - `message.py`: Handle messages
    - `glovar.py` : Global variables
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configuration
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribute

Welcome to make this project even better. You can submit merge requests, or report issues.

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
