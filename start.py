import threading
import subprocess

# Список портів для запуску трьох серверів
aps = ["/home/server/Save/save_dut.py", "/home/server/Save/save_lil.py", "/home/server/Save/save_par.py"]

# Функція для запуску Flask-додатка на конкретному порту
def run_app(app):
    subprocess.run(["python3", app])

# Запускаємо три програми у потоках
threads = []
for app in aps:
    thread = threading.Thread(target=run_app, args=(app,))
    thread.start()
    threads.append(thread)

# Чекаємо завершення всіх потоків (не обов'язково)
for thread in threads:
    thread.join()
