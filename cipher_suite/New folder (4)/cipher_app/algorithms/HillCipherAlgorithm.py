import numpy as np
from math import sqrt, ceil
from sympy import Matrix

def HillCipher(mode="encode", text="", key="GYBNQKURP"):
    if mode == "encode":
        key = key.upper().replace(" ", "")
        n = ceil(sqrt(len(key)))
        if len(key) < n * n:
            key = key + ("X" * abs(int(len(key)) - n * n))
        Mletter = [ord(i) - 65 for i in key]
        KeyMatrix = np.array(Mletter).reshape(n, n)
        plaintext = text.replace(" ", "").upper()
        if len(plaintext) % n != 0:
            plaintext = plaintext + "X" * ((n * ceil(len(plaintext) / n)) - len(plaintext))
        convertText = [ord(k) - 65 for k in plaintext]
        Vector = []
        j = 0
        while len(Vector) != len(plaintext) / n:
            Vector.append(convertText[j:j + n])
            j += n
        Multiplication = [np.dot(KeyMatrix, v) for v in Vector]
        cipher = ""
        for i in Multiplication:
            for j in i:
                cipher += chr((int(j) % 26) + 65)
        return cipher
    elif mode == "decode":
        key = key.upper().replace(" ", "")
        matrix = [ord(i) - 65 for i in key]
        n = ceil(sqrt(len(key)))
        KeyMatrix = np.array(matrix).reshape(n, n)
        DetKey = 0
        for e in range(26):
            if ((np.linalg.det(KeyMatrix) % 26) * e) % 26 == 1:
                DetKey = e
        A = Matrix(KeyMatrix.T)
        C = A.cofactor_matrix()
        C = (DetKey * C) % 26
        text = text.replace(" ", "").upper()
        textmatrix = [ord(i) - 65 for i in text]
        textmatrix1 = np.array(textmatrix)
        Vector1 = []
        j = 0
        while len(Vector1) != len(text) / n:
            Vector1.append(textmatrix1[j:j + n])
            j += n
        Multiplication1 = [np.dot(C, v) for v in Vector1]
        cipher1 = ""
        for i in Multiplication1:
            for j in i:
                cipher1 += chr((int(j) % 26) + 65)
        return cipher1.rstrip("X")
