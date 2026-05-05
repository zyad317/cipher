# -*- coding: utf-8 -*-
def VigenereCipherEncode(PlainText="", KeyText=""):
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
    return result

def VigenereCipherDecode(PlainText="", KeyText=""):
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

def PolyAlphabeticVigenereCipher(mode="decode", PlainText="", KeyText=""):
    if mode == "encode":
        return VigenereCipherEncode(PlainText, KeyText)
    elif mode == "decode":
        return VigenereCipherDecode(PlainText, KeyText)
