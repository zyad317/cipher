def AutoKeyEncode(PlainText="", KeyText=""):
    PlainText = PlainText.replace(" ", "").upper()
    KeyText = KeyText.replace(" ", "").upper()

    i = 0
    while len(KeyText) < len(PlainText):
        KeyText += PlainText[i % len(PlainText)]
        i += 1
    n = list(zip(PlainText, KeyText))
    result = ""
    for i in range(len(n)):
        a = chr(((ord(n[i][0]) - 65) + (ord(n[i][1]) - 65)) % 26 + 65)
        result += a
    return(result)


def AutoKeyDecode(PlainText="", KeyText=""):
    PlainText = PlainText.replace(" ", "").upper()
    KeyText = KeyText.replace(" ", "").upper()

    PlainTextSplit = [c for c in PlainText]
    KeyTextSplit = [c for c in KeyText]

    while len(KeyTextSplit) < len(PlainTextSplit):
        i = len(KeyTextSplit)
        a = chr(((ord(PlainTextSplit[i - len(KeyText)]) - 65) - (ord(KeyTextSplit[i - len(KeyText)]) - 65)) % 26 + 65)
        KeyTextSplit.append(a)

    UsedKeyText = "".join(KeyTextSplit)

    n = list(zip(PlainText, UsedKeyText))
    result = ""
    for i in range(len(n)):
        a = chr(((ord(n[i][0]) - 65) - (ord(n[i][1]) - 65)) % 26 + 65)
        result += a
    return result


def AutoKey(mode="decode", PlainText="", KeyText=""):
    if mode == "encode":
        return(AutoKeyEncode(PlainText, KeyText))
    elif mode == "decode":
        return(AutoKeyDecode(PlainText, KeyText))
