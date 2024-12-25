import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

client_sockets = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] подключаемся к серверу {SERVER_HOST}:{SERVER_PORT}")

def log_message(message):
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if not msg:
                break
            print(f"Получено сообщение от {cs.getpeername()}: {msg}")
            log_message(msg)
            for client_socket in client_sockets:
                if client_socket != cs:
                    client_socket.send(msg.encode())
        except Exception as e:
            print(f"[!] Ошибка: {e}")
            client_sockets.remove(cs)
            cs.close()
            break

while True:
    client_socket, client_address = s.accept()
    print(f"[+] Подключился {client_address}.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
