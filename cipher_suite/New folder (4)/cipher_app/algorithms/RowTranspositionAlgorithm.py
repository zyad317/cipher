import numpy as np
from math import ceil

def RowTransposition(mode="encode", text="", keyS="4312567"):
    if mode == "encode":
        if keyS.isalpha():
            letter = [c for c in keyS]
            number = [i for i in range(1, 1 + len(letter))]
            arr = dict(zip(sorted(letter), number))
            key = "".join(str(arr[j]) for j in letter)
        elif keyS.isdigit():
            key = keyS

        letters = list(text.replace(" ", "").upper())
        for i in range((ceil(len(letters) / len(str(key))) * len(str(key))) - len(letters)):
            letters.append("x")
        matrix = np.array(letters).reshape(ceil(len(text.replace(" ","")) / len(str(key))), len(str(key)))
        order = sorted(range(len(str(key))), key=lambda i: str(key)[i])
        result = [[row[i] for i in order] for row in matrix]
        np_matrix = np.array(result)
        cipher = ""
        for i in range(len(str(key))):
            cipher += "".join(np_matrix[:, i])
        return cipher

    elif mode == "decode":
        if keyS.isalpha():
            letter = [c for c in keyS]
            number = [i for i in range(1, 1 + len(letter))]
            arr = dict(zip(sorted(letter), number))
            key = "".join(str(arr[j]) for j in letter)
        elif keyS.isdigit():
            key = keyS

        text = text.replace(" ", "").upper()
        rows, cols = ceil(len(text) / len(str(key))), len(str(key))
        arr = np.array(list(text[:int(rows) * int(cols)])).reshape(int(rows), int(cols), order='F')
        order = [int(c) - 1 for c in str(key)]
        A_new = arr[:, order]
        plaintext = []
        for i in A_new:
            for j in i:
                plaintext.append("".join(j))
        return "".join(plaintext).rstrip("X").rstrip("x")
