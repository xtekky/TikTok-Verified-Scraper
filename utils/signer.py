import json
import time
import string
import hashlib
import itertools

class XGorgon:
    def __init__(self, params: str, data: str = None, cookies: str = None) -> None:

        self.params = params
        self.data = data
        self.cookies = cookies

    def __hash(self, data: str) -> str:
        _hash = str(
            hashlib.md5(
                data.encode()
            ).hexdigest()
        )

        return _hash

    def __base_string(self) -> str:
        base_str = self.__hash(self.params)
        base_str = (
            base_str + self.__hash(self.data) 
            if self.data
            else base_str + str("0" * 32)
        )
        base_str = (
            base_str + self.__hash(self.cookies)
            if self.cookies
            else base_str + str("0" * 32)
        )

        return base_str

    def get_value(self) -> json:
        base_str = self.__base_string()

        return self.__encrypt(base_str)

    def __encrypt(self, data: str) -> json:
        unix = int(time.time())
        len = 0x14
        key = [
            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]

        param_list = []

        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0x0, 0x6, 0xB, 0x1C])

        H = int(hex(unix), 16)

        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)

        eor_result_list = []

        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(len):

            C = self.__reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D

            F = self.__rbit_algorithm(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H

        result = ""
        for param in eor_result_list:
            result += self.__hex_str(param)

        return {
            "X-Gorgon": (
                "0404b0d30000" + result
            ), 
            "X-Khronos": str(unix)
        }

    def __rbit_algorithm(self, num):
        result = ""
        tmp_string = bin(num)[2:]

        while len(tmp_string) < 8:
            tmp_string = "0" + tmp_string

        for i in range(0, 8):
            result = result + tmp_string[7 - i]

        return int(result, 2)

    def __hex_str(self, num):
        tmp_string = hex(num)[2:]

        if len(tmp_string) < 2:
            tmp_string = "0" + tmp_string

        return tmp_string

    def __reverse(self, num):
        tmp_string = self.__hex_str(num)

        return int(tmp_string[1:] + tmp_string[:1], 16)
    
def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(string.ascii_lowercase, repeat=size):
            yield "".join(s)
 
def get_keywords(count: int):
    letter_list = []
    for s in iter_all_strings():
        # print(s)
        letter_list.append(s)
        if s == 'z'*count:
            break
    return letter_list