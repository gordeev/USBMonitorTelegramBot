import wmi
import time
import telegram
import asyncio
import pythoncom
from threading import Thread
from win32com.client import GetObject
import cv2
import os
from telegram import InputFile

# Initialize Telegram Bot
bot = telegram.Bot(token='TELEGRAM_BOT_TOKEN')
chat_id = 'CHAT_ID'

async def send_message_to_telegram(bot, chat_id, message):
    # Capture photo from webcam
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture photo")
        return
    cam.release()

    # Save photo
    photo_path = "photo.jpg"
    cv2.imwrite(photo_path, frame)

    # Send photo with message
    with open(photo_path, 'rb') as photo_file:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file), caption=message)

    # Delete photo
    os.remove(photo_path)

def monitor_usb():
    pythoncom.CoInitialize()  # Initialize COM library for this thread
    c = wmi.WMI()
    last_count = len(c.Win32_USBControllerDevice())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        while True:
            c = wmi.WMI()
            count = len(c.Win32_USBControllerDevice())
            if count != last_count:
                if count > last_count:
                    loop.run_until_complete(send_message_to_telegram(bot, chat_id, 'A new USB device has been connected.'))
                else:
                    loop.run_until_complete(send_message_to_telegram(bot, chat_id, 'A USB device has been disconnected.'))
                last_count = count
            time.sleep(1)
    finally:
        loop.close()
    pythoncom.CoUninitialize()  # Clean up COM library for this thread

Thread(target=monitor_usb).start()


