import time
import cv2
import telebot
import threading
import sys

# Введите свой токен телеграм-бота и ID чата
TOKEN = ""
CHAT_ID = ""

bot = telebot.TeleBot(TOKEN)
motion_detection_active = False
recording_video = False

# Функция для получения фотографии с веб-камеры
def take_photo():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if not ret:
        print("Не удалось сделать снимок")
        return None
    cv2.imwrite("snapshot.jpg", frame)
    camera.release()
    return "snapshot.jpg"

# Функция для записи видео
def record_video(filename='motion_detected.avi', duration=15):
    global recording_video
    recording_video = True

    camera = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            break

    camera.release()
    out.release()
    recording_video = False

# Функция для обнаружения движения
def detect_motion():
    global motion_detection_active, recording_video
    camera = cv2.VideoCapture(0)
    first_frame = None

    while motion_detection_active:
        ret, frame = camera.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            break

        if motion_detected and not recording_video:
            print("Motion detected!")
            bot.send_message(CHAT_ID, "Motion detected! Recording video...")
            record_video()
            bot.send_video(CHAT_ID, open('motion_detected.avi', 'rb'))

            if motion_detection_active:
                continue

        time.sleep(0.5)

    camera.release()

@bot.message_handler(commands=['photo'])
def send_photo(message):
    photo = take_photo()
    if photo is not None:
        bot.send_photo(message.chat.id, open(photo, 'rb'))
    else:
        bot.send_message(message.chat.id, "Не удалось сделать снимок")

@bot.message_handler(commands=['movedetect'])
def start_motion_detection(message):
    global motion_detection_active
    if not motion_detection_active:
        motion_detection_active = True
        bot.send_message(message.chat.id, "Motion detection activated.")
        motion_detection_thread = threading.Thread(target=detect_motion)
        motion_detection_thread.daemon = True
        motion_detection_thread.start()
    else:
        bot.send_message(message.chat.id, "Motion detection is already active.")

@bot.message_handler(commands=['movedetectoff'])
def stop_motion_detection(message):
    global motion_detection_active
    if motion_detection_active:
        motion_detection_active = False
        bot.send_message(message.chat.id, "Motion detection deactivated.")
    else:
        bot.send_message(message.chat.id, "Motion detection is not active.")

@bot.message_handler(commands=['video'])
def send_video(message):
    bot.send_message(message.chat.id, "Recording 15-second video...")
    record_video()
    bot.send_video(message.chat.id, open('motion_detected.avi', 'rb'))

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Available commands:\n"
        "/photo - Take a photo and send it\n"
        "/movedetect - Activate motion detection\n"
        "/movedetectoff - Deactivate motion detection\n"
        "/video - Record a 15-second video and send it\n"
        "/stop - Stop the bot\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    bot.send_message(message.chat.id, "Stopping bot...")
    sys.exit()

bot.send_message(CHAT_ID, "Bot started")

bot.polling()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
