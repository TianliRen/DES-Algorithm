from utils import *
from tables import *
import numpy as np


# According to input key, we generate sixteen sub-keys and each of them is a 48 digit number. 
# Args:
#   key: a binary list representing the key itself
# Returns:
#   a list carrying sixteen sub-keys 
def generate_sub_key(key: list[str]) -> list[list[str]]:
    sub_keys = []
    left, right = pc_1(key=key)
    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    for i in range(16):  # according to the shift number, splits and concatenates the key
        left = left[shifts[i]:] + left[:shifts[i]]
        right = right[shifts[i]:] + right[:shifts[i]]
        sub_keys.append(pc_2(left + right))
    return sub_keys


# Iterating operation for left-key and right-key
def iterate_lr(left, right, sub_key):
    return right, exclusive_or(left, feistel(right, sub_key))


# Calculate exclusive-OR for elements in two lists.
# Args:
#   lst1, lst2: two lists carrying integers in the string form
# Returns:
#   a list carrying the exclusive-OR calculating result
def exclusive_or(lst1: list, lst2: list) -> list[int]:
    return [int(x) ^ int(y) for x, y in zip(lst1, lst2)]


# Function f,namely feistel, comprises three steps: exclusive_or, S_box, and permutation.
def feistel(x, sub_key):
    x = exclusive_or(expand(x), sub_key)
    x = do_s(x)
    x = permute(x)
    return x


# Execute operations related to the S-box, which comprises eight sub-boxes.
def do_s(x):
    s_box = [s1, s2, s3, s4, s5, s6, s7, s8]  # s_box is a two-dimensional list

    x = np.array(x, dtype=int).reshape(8, 6)  # reshaping the x to match s_box more easily

    res = []
    for i in range(8):
        p = x[i]
        r = s_box[i][binary2int([p[0], p[5], p[1], p[2], p[3], p[4]])]  # find the relative value in the s-box
        res.append(int2binary(r, 4))

    res = np.array(res).flatten().tolist()  # flatten the data structure into an one-dimensional list
    return res


# The main logic of encryption/decryption with DES Algorithm.
# Args:
#   text: the original text
#   key: the original key
#   method: whether choose encrypt/decrypt
# Returns:
#   the obtained result after DES operation
def execute_des(text: str, key: str, method: str, is_file=False) -> str:
    sub_keys = generate_sub_key(str2binary(key))

    # the inputs for decryption and encryption require different strategies
    if method == 'de':
        sub_keys = sub_keys[::-1]
        encoded_lst = complement_bin(list(text))
        print(f"The coded list has length of {len(encoded_lst)}")
    else:
        encoded_lst = str2binary(text)

    piece_num = int(len(encoded_lst) / 64)  # the text list is divided into pieces. Each piece is in 64 bits.
    result = []
    for i in range(piece_num):
        text = initial_permute(encoded_lst[i * 64: (i + 1) * 64])

        left, right = np.array(text, dtype=int).reshape(2, -1).tolist()

        for p in range(16):
            left, right = iterate_lr(left, right, sub_keys[p])

        result += [str(x) for x in final_permute(right + left)]

    if method == 'de':
        return binary2str(result)
    return ''.join(result)
