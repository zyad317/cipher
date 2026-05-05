import string
import numpy as np


def InsertX(text):
    result = []
    texts = list(text.upper().strip())
    i = 1
    while i < len(texts):
        if (texts[i] == texts[i - 1]):
            texts.insert(i, "X")
        i += 2
    finaltext = "".join(texts)
    for i in range(0, len(finaltext), 2):
        if int(len(finaltext)) % 2 != 0:
            if int(len(finaltext[i:i+2])) == 1:
                result.append(finaltext[i:i+2] + "X")
            else:
                result.append(finaltext[i:i+2])
        else:
            result.append(finaltext[i:i+2])
    return result


def PlayFairEncode(text="", keyword="MONARCHY"):
    text = text.replace(" ", "").replace("J", "I").replace("j", "I")
    AfterEdit = InsertX(text)
    # playfair matrix
    remove_letter = "J"
    letters = []
    keyword = keyword.upper().strip()
    for c in keyword:
        if c != remove_letter and c in string.ascii_uppercase and c not in letters:
            letters.append(c)
    for c in string.ascii_uppercase:
        if c != remove_letter and c not in letters:
            letters.append(c)
    matrix = np.array(letters[:25]).reshape(5, 5)
    encryption_text = ""
    for word in AfterEdit:
        first_letter = word[0]
        second_letter = word[1]
        r1 = c1 = r2 = c2 = -1
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == first_letter:
                    r1, c1 = i, j
                elif matrix[i][j] == second_letter:
                    r2, c2 = i, j
        if r1 == r2:
            encryption = matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            encryption = matrix[((r1 + 1) % 5)][c1] + matrix[(r2 + 1) % 5][c2]
        else:
            encryption = matrix[r1][c2] + matrix[r2][c1]
        encryption_text += encryption
    return encryption_text


def PlayFairDecode(finaltext="", keyword="MONARCHY"):
    result = []
    finaltext = finaltext.replace(" ", "").replace("J", "I").replace("j", "I")
    # playfair matrix
    remove_letter = "J"
    letters = []
    keyword = keyword.upper().strip()
    for c in keyword:
        if c != remove_letter and c in string.ascii_uppercase and c not in letters:
            letters.append(c)
    for c in string.ascii_uppercase:
        if c != remove_letter and c not in letters:
            letters.append(c)
    matrix = np.array(letters[:25]).reshape(5, 5)
    for i in range(0, len(finaltext), 2):
        if int(len(finaltext)) % 2 != 0:
            if int(len(finaltext[i:i+2])) == 1:
                result.append(finaltext[i:i+2] + "X")
            else:
                result.append(finaltext[i:i+2])
        else:
            result.append(finaltext[i:i+2])
    decryption_text = ""
    for word in result:
        first_letter = word[0]
        second_letter = word[1]
        r1 = c1 = r2 = c2 = -1
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == first_letter:
                    r1, c1 = i, j
                elif matrix[i][j] == second_letter:
                    r2, c2 = i, j
        if r1 == r2:
            decryption = matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            decryption = matrix[((r1 - 1) % 5)][c1] + matrix[(r2 - 1) % 5][c2]
        else:
            decryption = matrix[r1][c2] + matrix[r2][c1]
        decryption_text += decryption
    if decryption_text.endswith("X"):
        decryption_text = decryption_text[:-1]
    for index in decryption_text:
        index = decryption_text.find("X")
        if index > 0 and index + 1 < len(decryption_text):
            if decryption_text[index - 1] == decryption_text[(index + 1)]:
                decryption_text = decryption_text[:index] + decryption_text[index + 1:]
    return decryption_text


def PlayFairCipher(mode="encode", text="", keyword="MONARCHY"):
    if mode == "encode":
        return PlayFairEncode(text, keyword)
    elif mode == "decode":
        return PlayFairDecode(text, keyword)
