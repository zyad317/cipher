def CaesarCipher(mode="encode", UserText="", key=3):
    key = int(key)
    if mode == "encode":
        result = ""
        for char in UserText:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) + key - 65) % 26 + 65)
                else:
                    result += chr((ord(char) + key - 97) % 26 + 97)
            else:
                result += char
        return result
    elif mode == "decode":
        result = ""
        for char in UserText:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) - key - 65) % 26 + 65)
                else:
                    result += chr((ord(char) - key - 97) % 26 + 97)
            else:
                result += char
        return result
