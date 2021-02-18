import socket
import threading


def read_sock():    # Функция для считывания сообщений с сервера
    while True:
        data = sock.recv(1024).decode('utf-8')
        print(f'\n{data}')


server = 'localhost', 9090
nickname = input('Enter your name: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))
sock.sendto(f'{nickname} connected to chat'.encode('utf-8'), server)

thread = threading.Thread(target=read_sock)     # Создает поток и запускает в нем функцию read_sock, чтобы прием
thread.start()                                  # сообщений производился по мере их отправки (в постоянном потоке)

while True:
    message = input('Enter your message:\n')
    sock.sendto(f'[{nickname}] {message}'.encode('utf-8'), server)
