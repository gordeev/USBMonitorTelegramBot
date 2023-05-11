#WINDOWS EDITION (!!!)

<h1 align="center">USB Device Guard with Telegram Notifications</h1>

<p align="center">
This is a Python script that monitors USB devices on your computer. It sends notifications to a specified Telegram chat when a USB device is connected or disconnected. The notification includes a photo captured from the system's webcam.
</p>

## Prerequisites

This script requires Python 3.7 or later. The following Python packages are also required:

- `wmi`
- `pywinusb`
- `python-telegram-bot`
- `opencv-python`

These can be installed via pip:

```sh
pip install wmi pywinusb python-telegram-bot opencv-python
```

## How to Use

1. Create a Telegram bot and obtain the bot token. See <a href="https://core.telegram.org/bots#creating-a-new-bot">Creating a new bot</a> for instructions.
2. Get your Telegram chat ID. You can do this by messaging your bot, then visiting https://api.telegram.org/bot<_YourBOTToken_>/getUpdates in a web browser. Replace <YourBOTToken> with your bot token.
3. In the Python script, replace YOUR_BOT_TOKEN and YOUR_CHAT_ID with your bot token and chat ID, respectively.
4. Run the script. You will receive a message with a photo in your Telegram chat whenever a USB device is connected or disconnected.
