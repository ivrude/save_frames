import os
from time import sleep

import cv2
import datetime
import threading
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# Налаштування
RTSP_URL = "rtsp://admin:p@ssw0rd@192.168.0.22:554"  # Замініть на свою RTSP-URL
SAVE_DIR = "Leliv"
FRAMES_TO_CAPTURE = 5

# Створюємо основну папку, якщо її немає
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def capture_frames(folder_path):
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print("Не вдалося відкрити RTSP потік")
        return

    for i in range(FRAMES_TO_CAPTURE):
        ret, frame = cap.read()
        if not ret:
            print("Не вдалося отримати кадр")
            break

        filename = os.path.join(folder_path, f"frame_{i + 1}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Збережено: {filename}")

    cap.release()
    capture_grafana_screenshot(folder_path)


def capture_grafana_screenshot(folder):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--window-size=1280,800"])
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})  # Встановлюємо розмір вікна браузера

        page.goto("http://192.168.0.5:3000/d/ddlsl1eunjugwd1222/arm-2-leliv?orgId=1&refresh=5s")
        page.fill('input[name="user"]', "admin")
        page.fill('input[name="password"]', "p@ssw0rd")

        # Натискання кнопки входу
        page.click('button[type="submit"]')


        sleep(2.5)
        # Зняття скріншота
        page.screenshot(path=f"{folder}/grafana_screenshot.png")
        browser.close()


@app.route("/webhook", methods=["POST","GET"])
def webhook():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = os.path.join(SAVE_DIR, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    threading.Thread(target=capture_frames, args=(folder_path,)).start()

    return jsonify({"status": "ok", "folder": folder_path})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
