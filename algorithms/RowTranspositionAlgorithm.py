import numpy as np
import wordninja
from math import ceil

def RowTransposition(mode="encode", text="", keyS="4312567"):
    if mode == "encode":
        if keyS.isalpha():
            letter = [c for c in keyS]
            number = [i for i in range(1, 1 + len(letter))]
            arr = dict(zip(sorted(letter), number))
            set_key = ""
            for j in letter:
                set_key += str(arr[j])
            key = set_key
        elif keyS.isdigit():
            key = int(keyS)

        letters = []
        p = text.replace(" ", "").upper()

        for c in p:
            letters.append(c)
        for i in range((ceil(len(p) / len(str(key))) * len(str(key))) - int(len(p))):
            letters.append("x")
        matrix = np.array(letters[:]).reshape(ceil(len(p) / len(str(key))), len(str(key)))

        order = sorted(range(len(str(key))), key=lambda i: str(key)[i])
        result = [[row[i] for i in order] for row in matrix]
        cipher = ""
        np_matrix = np.array(result)
        for i in range(len(str(key))):
            cipher += "".join(np_matrix[:, i])

        return(cipher)

    elif mode == "decode":
        if keyS.isalpha():
            letter = [c for c in keyS]
            number = [i for i in range(1, 1 + len(letter))]
            arr = dict(zip(sorted(letter), number))
            set_key = ""
            for j in letter:
                set_key += str(arr[j])
            key = set_key
        elif keyS.isdigit():
            key = int(keyS)

        text = text.replace(" ", "").upper()
        rows, cols = ceil(len(text) / len(str(key))), len(str(key))

        arr = np.array(list(text[:int(rows) * int(cols)])).reshape(int(rows), int(cols), order='F')

        order = sorted(range(len(str(key))), key=lambda i: str(key)[i])
        result = [[row[i] for i in order] for row in arr]
        np_matrix = np.array(result)

        order = [int(c) - 1 for c in str(key)]
        A_new = arr[:, order]

        plaintext = []
        for i in A_new:
            for j in i:
                plaintext.append("".join(j))

        final = "".join(plaintext)
        final1 = final.rstrip("X")
        return(" ".join(wordninja.split(final1)))
