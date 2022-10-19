import base64
import random
import re
from functools import reduce
import numpy as np


def str2binary(text: str) -> list[str]:
    # Every character in the text body is converted into its binary form;
    # If its binary form's length is less than 8, zero(s) are complemented at the front;
    res = ''
    res = res.join(str('0' * (8 - len(bin(ord(char))[2:]))) + bin(ord(char))[2:] for char in text)
    # Then, those binary chars are concatenated into a whole string.
    # The length of the whole string should be able to be divided with 64, otherwise it is complemented with following
    # zero(s).
    # Split the big string into an array for later operations
    if len(res) % 64 != 0:
        res += '0' * (64 - len(res) % 64)
    return list(res)


# convert text from binary array to string
def binary2str(str_bin: list[str]) -> str:
    str_bin = "".join(str_bin)
    res = ""
    # Every eight digits represent a character
    tmp = re.findall(r'.{8}', str_bin)
    for i in tmp:
        res += chr(int(i, 2))
    return res


# convert from binary list to integer:
def binary2int(bin_list: list[int]) -> int:
    return reduce(lambda a, b: a * 2 + b, bin_list)


# input an integer number, output its binary form with an array.
# n illustrates the length of the array.
def int2binary(num, length):
    res = np.zeros(length, dtype=int)
    for x in range(length):
        res[length - x - 1] = num % 2
        num = num // 2
    return res.tolist()


# When the encoded binary sequence is entered for decryption, this function works to ensure the size of sequence
# is proportional to 64.
def complement_bin(bin_list: list[str]) -> list[str]:
    if len(bin_list) % 64 != 0:
        for i in range(64 - len(bin_list) % 64):
            bin_list.append('0')
    return bin_list
