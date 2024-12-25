import socket

from threading import Thread
from datetime import datetime
from colorama import Fore, init

init()
name = input("Введите ваше имя: ")


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = "<SEP>"

s = socket.socket()
print(f"[*] Присоединяется {SERVER_HOST} : {SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] присоединился .")

def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()
            if message:
                print("\n"+message)
        except Exception as e:
            print(f"[!] Ошибка: {e}")
            break

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    if to_send.lower() == 'q':
        break

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"[{date_now}] {name} {separator_token} {to_send}{Fore.RESET}"
    try:
        s.send(to_send.encode())
    except Exception as e:
        print(f"[!] Ошибка: {e}")
        break

s.close()