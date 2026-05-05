import string

def MonoalphabeticCipher(mode, word=""):
    letters = list(string.ascii_lowercase)
    shuffleletter = ['o', 'z', 'm', 'p', 'y', 'a', 'b', 't', 'w', 'v', 'c', 'u', 'k',
                     'e', 'x', 'j', 'l', 'q', 'h', 's', 'r', 'n', 'i', 'd', 'f', 'g']
    cipher = dict(zip(letters, shuffleletter))
    if mode == "encode":
        result = ""
        for char in word:
            if char in cipher:
                result += cipher[char]
        return(result)
    elif mode == "decode":
        result = ""
        for char in word:
            for key, val in cipher.items():
                if val == char:
                    result += key
        return(result)
