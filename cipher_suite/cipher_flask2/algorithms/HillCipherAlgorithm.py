import numpy as np
from math import sqrt, ceil
from sympy import Matrix
import wordninja

def HillCipher(mode="encode", text="", key="GYBNQKURP"):
    if mode == "encode":
        key = key.upper().replace(" ", "")
        n = ceil(sqrt(len(key)))
        if len(key) < n * n:
            key = key + ("X" * abs(int(len(key)) - n * n))
        Mletter = []
        for i in key:
            Mletter.append(ord(i) - 65)
        KeyMatrix = np.array(Mletter[:]).reshape(n, n)
        plaintext = text.replace(" ", "").upper()
        convertText = []
        Vector = []
        if len(plaintext) % n != 0:
            plaintext = plaintext + "X" * ((n * ceil(len(plaintext) / n)) - (len(plaintext)))

        for k in plaintext:
            convertText.append(ord(k) - 65)
        j = 0
        while len(Vector) != len(plaintext) / n:
            Vector.append(convertText[j:j + n])
            j += n

        Multiplication = []
        for l in range(len(Vector)):
            Multiplication.append(np.dot(KeyMatrix, Vector[l]))
        cipher = ""
        for i in Multiplication:
            for j in i:
                cipher += chr((int(j) % 26) + 65)
        return(cipher)

    elif mode == "decode":
        key = key.upper().replace(" ", "")
        matrix = []
        for i in key:
            matrix.append(ord(i) - 65)
        n = ceil(sqrt(len(key)))
        KeyMatrix = np.array(matrix[:]).reshape(n, n)

        DetKey = 0
        for e in range(26):
            if ((np.linalg.det(KeyMatrix) % 26) * e) % 26 == 1:
                DetKey = e

        A = Matrix(KeyMatrix.T)
        C = A.cofactor_matrix()
        C = (DetKey * C) % 26
        text = text.replace(" ", "").upper()
        textmatrix = []
        for i in text:
            textmatrix.append(ord(i) - 65)
        textmatrix1 = np.array(textmatrix[:])
        Vector1 = []
        j = 0
        while len(Vector1) != len(text) / n:
            Vector1.append(textmatrix1[j:j + n])
            j += n
        Multiplication1 = []
        for l in range(len(Vector1)):
            Multiplication1.append(np.dot(C, Vector1[l]))
        cipher1 = ""
        for i in Multiplication1:
            for j in i:
                cipher1 += chr((int(j) % 26) + 65)

        final = "".join(cipher1)
        final1 = final.rstrip("X")
        return(" ".join(wordninja.split(final1)))
