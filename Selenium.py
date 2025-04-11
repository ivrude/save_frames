from time import sleep
from playwright.sync_api import sync_playwright

def capture_grafana_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--window-size=1920,1080"])
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})  # Встановлюємо розмір вікна браузера

        page.goto("http://192.168.0.5:3000/d/ddlsl1eunjugwd1/arm-3-ditjatki?orgId=1&refresh=5s")
        page.fill('input[name="user"]', "admin")
        page.fill('input[name="password"]', "p@ssw0rd")

        # Натискання кнопки входу
        page.click('button[type="submit"]')
        sleep(3)

        # Зміна масштабу сторінки до 70%
        page.evaluate("document.body.style.zoom='100%'")
        sleep(2)

        # Зняття скріншота
        page.screenshot(path="grafana_screenshot.png")
        browser.close()

capture_grafana_screenshot()
