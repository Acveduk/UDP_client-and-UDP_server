import json
import socket
import struct

UDP_MAX_SIZE = 1024


def listen(host: str = '127.0.0.1', port: int = 3000):
    """Создает сокет и слушает сообщения. Полученные пакеты обрабатывает. Складывает данные пакетов одного маркера
    вместе.
    :param host: Хост
    :param port: Порт
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Слушаем {host}:{port}')

    data = {}

    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)
        header, body, json_data = (struct.unpack('>HIH', msg[:struct.calcsize('>HIH')]),
                                   struct.unpack('>HHHH', msg[struct.calcsize('>HIH'):struct.calcsize('>HIHHHHH')]),
                                   msg[16:])

        if data.get(header[0]):
            data[header[0]]['json_data'] += json_data
            data[header[0]]['count_pack'] += 1
        else:
            data[header[0]] = dict(
                json_data=json_data,
                count_pack=1
            )

        if data[header[0]]['count_pack'] == body[1]:
            json_client = json.loads(data[header[0]]['json_data'].decode())
            print('JSON от клиента дошел полностью:\n', json_client)
            data.pop(header[0])
            s.sendto('Данные успешно пришли!'.encode(), addr)


if __name__ == '__main__':
    listen()
