import ctypes
import json
import struct


class Kit:
    """Создает объект набора пакетов, которые отправяться на сервер."""

    MAX_LENGTH_PACK = 1024
    MAX_SIZE_CYCLIC_NUMBER_MESSAGES = ctypes.c_uint32(-1).value
    MAX_SIZE_CYCLIC_ID_PARAMETRIC_STRING = ctypes.c_uint16(-1).value

    CYCLIC_NUMBER_MESSAGES = 1
    CYCLIC_ID_PARAMETRIC_STRING = 1

    SERIAL_NUMBER_PARAMETRIC_STRING = 1

    FORMAT_HEADER = '>HIH'

    def __init__(self, json_data: json, marker: int):
        self.json_data = json_data
        self.marker = marker
        self.parametric_strings = self._total_string()
        self.total_parametric_strings = len(self.parametric_strings)

    def _create_header(self, size_block_data: int) -> bytes:
        """Упаковывает данные заголовка
        :param size_block_data: размер блока данных
        """
        return struct.pack(self.FORMAT_HEADER, self.marker, self.CYCLIC_NUMBER_MESSAGES, size_block_data)

    def _create_body(self) -> bytes:
        """Упаковывает данные блока данных"""
        body = struct.pack(
            f'>HHHH{len(self.parametric_strings[self.SERIAL_NUMBER_PARAMETRIC_STRING - 1])}s',
            self.CYCLIC_ID_PARAMETRIC_STRING,
            self.total_parametric_strings,
            self.SERIAL_NUMBER_PARAMETRIC_STRING,
            len(self.parametric_strings[self.SERIAL_NUMBER_PARAMETRIC_STRING - 1]),
            self.parametric_strings[self.SERIAL_NUMBER_PARAMETRIC_STRING - 1],
        )
        return body

    def pack(self) -> bytes:
        """Создает заголовок и блок данных. Объединяет в пакет."""
        body = self._create_body()
        header = self._create_header(len(body))

        self.CYCLIC_NUMBER_MESSAGES = self.CYCLIC_NUMBER_MESSAGES + 1 if self.CYCLIC_NUMBER_MESSAGES < self.MAX_SIZE_CYCLIC_NUMBER_MESSAGES else 1
        self.CYCLIC_ID_PARAMETRIC_STRING = self.CYCLIC_ID_PARAMETRIC_STRING + 1 if self.CYCLIC_ID_PARAMETRIC_STRING < self.MAX_SIZE_CYCLIC_ID_PARAMETRIC_STRING else 1
        self.SERIAL_NUMBER_PARAMETRIC_STRING += 1

        return header + body

    def _total_string(self) -> list:
        """JSON объекта кодирует и делит на параметрическая строки"""
        json_str = json.dumps(self.json_data, ensure_ascii=False).encode()
        chunks = []
        index = 0
        max_size = 992
        while index < len(json_str):
            chunk = json_str[index:index + max_size]
            chunks.append(chunk)
            index += len(chunk)
        return chunks
