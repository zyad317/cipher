def CaesarCipher(mode="encode", UserText="", key=3):
    key = int(key)
    # encode
    if mode == "encode":
        result = ""
        for char in UserText:
            if char.isalpha():
                if char.isupper():
                    Encode = (ord(char) + key - 65) % 26 + 65
                    TextEncode = chr(Encode)
                    result += TextEncode
                else:
                    Encode = (ord(char) + key - 97) % 26 + 97
                    TextEncode = chr(Encode)
                    result += TextEncode
            else:
                result += char
        return result
    # decode
    elif mode == "decode":
        result = ""
        for char in UserText:
            if char.isalpha():
                if char.isupper():
                    Encode = (ord(char) - key - 65) % 26 + 65
                    TextEncode = chr(Encode)
                    result += TextEncode
                else:
                    Encode = (ord(char) - key - 97) % 26 + 97
                    TextEncode = chr(Encode)
                    result += TextEncode
            else:
                result += char
        return result
