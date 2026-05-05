# -*- coding: utf-8 -*-

def VigenèreCipherEncode(PlainText="", KeyText=""):
    PlainText = PlainText.replace(" ", "").upper()
    KeyText = KeyText.replace(" ", "").upper()

    i = 0
    while len(KeyText) < len(PlainText):
        KeyText += KeyText[i % len(KeyText)]
        i += 1

    s = list(zip(PlainText, KeyText))
    result = ""
    for i in range(len(s)):
        a = chr(((ord(s[i][0]) - 65) + (ord(s[i][1]) - 65)) % 26 + 65)
        result += a
    return(result)


def VigenèreCipherDecode(PlainText="", KeyText=""):
    PlainText = PlainText.replace(" ", "").upper()
    KeyText = KeyText.replace(" ", "").upper()

    i = 0
    while len(KeyText) < len(PlainText):
        KeyText += KeyText[i % len(KeyText)]
        i += 1

    s = list(zip(PlainText, KeyText))
    result = ""
    for i in range(len(s)):
        a = chr(((ord(s[i][0]) - 65) - (ord(s[i][1]) - 65)) % 26 + 65)
        result += a
    return result


def PolyAlphabeticVigenèreCipher(mode="decode", PlainText="", KeyText=""):
    if mode == "encode":
        return VigenèreCipherEncode(PlainText, KeyText)
    elif mode == "decode":
        return VigenèreCipherDecode(PlainText, KeyText)
