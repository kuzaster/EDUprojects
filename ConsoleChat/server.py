import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9090))
members = []    # Список участников в чате. Хранится IP и PORT пользователя

print('Start Server')

while True:
    data, addr = sock.recvfrom(1024)    # data - сообщение от пользователя. addr - адрес пользователя (IP и PORT)
    if addr not in members:     # Если пользователя нет в списке, то добавлет его
        members.append(addr)    # и выводит сообщение о подключении пользователя с его данными
        print(f'{addr[0]}, {addr[1]} connected')
    if len(members) < 2:    # Предупреждает, если в чате только один пользователь
        sock.sendto("Please, wait another user, you are the only at this chat".encode('utf-8'), addr)
    for member in members:
        if member == addr:      # Не отсылает сообщение самому автору
            continue
        sock.sendto(data, member)
