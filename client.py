import json
import os
import socket
import threading

from kit import Kit


def listen(s: socket.socket):
    """Слушает ответ от сервера и выводит ответ.
    :param s: Сокет
    """
    while True:
        try:
            msg = s.recv(1024)
            print('\r\r' + msg.decode() + '\n' + 'Передайте путь к файлу(JSON): ', end='')
        except ConnectionRefusedError as e:
            print('\nНевозможно соединится с сервером! Попробуйте позже!')
            continue


def connect(host: str = '127.0.0.1', port: int = 3000):
    """Устанавливает соединение с сервером. Просит от пользователя путь к файлу. Разбивает при необходимости на
    пакеты и отправляет на сервер
    :param host: хост
    :param port: порт
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect((host, port))

    threading.Thread(target=listen, args=(s,), daemon=True).start()

    while True:
        path_json = input('Передайте путь к файлу(JSON): ')

        try:
            with open(path_json, 'r') as file:
                json_data = json.load(file)
            kit = Kit(json_data, 61166)
            while kit.SERIAL_NUMBER_PARAMETRIC_STRING <= kit.total_parametric_strings:
                s.send(kit.pack())
        except FileNotFoundError:
            print('Файл не найден!')
            continue
        except json.decoder.JSONDecodeError:
            print('Вы передали файл с не данными формата JSON')
            continue


if __name__ == '__main__':
    os.system('clear')
    print('Добро пожаловать!')
    connect()
