# SCP-079-CONFIG

This bot is used to manage settings for each bot.

## How to use

- Read [the document](https://scp-079.org/config/) to learn more
- [README](https://github.com/scp-079/scp-079-readme) of the SCP-079 Project
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- Python 3.6 or higher
- pip: `pip install -r requirements.txt` or `pip install -U APScheduler pyAesCrypt pyrogram[fast]`

## Files

- plugins
    - functions
        - `channel.py` : Functions about channel
        - `config.py` : Generate config session message
        - `etc.py` : Miscellaneous
        - `filters.py` : Some filters
        - `receive.py` : Receive data from exchange channel
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
