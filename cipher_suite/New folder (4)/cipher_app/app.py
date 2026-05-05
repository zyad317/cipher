from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from CaesarAlgorithm import CaesarCipher
from AutoKeyAlgorithm import AutoKey
from PolyAlphabeticVigenereAlgorithm import PolyAlphabeticVigenereCipher
from RailFenceAlgorithm import RailFence
from MonoalphabeticAlgorithm import MonoalphabeticCipher
from PlayFairAlgorithm import PlayFairCipher
from HillCipherAlgorithm import HillCipher
from RowTranspositionAlgorithm import RowTransposition

app = Flask(__name__)

CIPHER_INFO = {
    "caesar": {
        "name": "Caesar Cipher",
        "description": "A substitution cipher that shifts each letter by a fixed number of positions.",
        "type": "Substitution",
        "era": "Ancient Rome",
        "icon": "⚔️",
        "fields": [{"name": "key", "label": "Shift Key", "type": "number", "default": "3", "placeholder": "e.g. 3"}]
    },
    "autokey": {
        "name": "AutoKey Cipher",
        "description": "A polyalphabetic cipher using the plaintext itself to extend the key.",
        "type": "Polyalphabetic",
        "era": "16th Century",
        "icon": "🗝️",
        "fields": [{"name": "KeyText", "label": "Key", "type": "text", "default": "KEY", "placeholder": "e.g. KEY"}]
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "description": "A method of encrypting text using a series of different Caesar ciphers based on a keyword.",
        "type": "Polyalphabetic",
        "era": "16th Century",
        "icon": "📜",
        "fields": [{"name": "KeyText", "label": "Keyword", "type": "text", "default": "KEY", "placeholder": "e.g. SECRET"}]
    },
    "railfence": {
        "name": "Rail Fence Cipher",
        "description": "A transposition cipher that writes text in a zigzag pattern across multiple 'rails'.",
        "type": "Transposition",
        "era": "Ancient",
        "icon": "🚂",
        "fields": [{"name": "rails", "label": "Number of Rails", "type": "number", "default": "3", "placeholder": "e.g. 3"}]
    },
    "monoalphabetic": {
        "name": "Monoalphabetic Cipher",
        "description": "A substitution cipher where each letter maps to a unique fixed substitute.",
        "type": "Substitution",
        "era": "Classical",
        "icon": "🔡",
        "fields": []
    },
    "playfair": {
        "name": "Playfair Cipher",
        "description": "A digraph substitution cipher that encrypts pairs of letters using a 5×5 key matrix.",
        "type": "Digraph Substitution",
        "era": "19th Century",
        "icon": "♟️",
        "fields": [{"name": "keyword", "label": "Keyword", "type": "text", "default": "MONARCHY", "placeholder": "e.g. MONARCHY"}]
    },
    "hill": {
        "name": "Hill Cipher",
        "description": "A polygraphic cipher based on linear algebra, encrypting blocks of letters using matrix multiplication.",
        "type": "Polygraphic",
        "era": "1929",
        "icon": "📐",
        "fields": [{"name": "key", "label": "Key Matrix (letters)", "type": "text", "default": "GYBNQKURP", "placeholder": "e.g. GYBNQKURP"}]
    },
    "rowtransposition": {
        "name": "Row Transposition",
        "description": "A transposition cipher that rearranges plaintext columns according to a numeric or alphabetic key.",
        "type": "Transposition",
        "era": "Classical",
        "icon": "📊",
        "fields": [{"name": "keyS", "label": "Key", "type": "text", "default": "4312567", "placeholder": "e.g. 4312567 or KEYWORD"}]
    },
}

@app.route('/')
def index():
    return render_template('index.html', ciphers=CIPHER_INFO)

@app.route('/cipher/<cipher_name>')
def cipher_page(cipher_name):
    if cipher_name not in CIPHER_INFO:
        return "Cipher not found", 404
    return render_template('cipher.html', cipher=CIPHER_INFO[cipher_name], cipher_name=cipher_name, ciphers=CIPHER_INFO)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    cipher = data.get('cipher')
    mode = data.get('mode', 'encode')
    text = data.get('text', '')

    try:
        if cipher == 'caesar':
            key = int(data.get('key', 3))
            result = CaesarCipher(mode=mode, UserText=text, key=key)
        elif cipher == 'autokey':
            key_text = data.get('KeyText', 'KEY')
            result = AutoKey(mode=mode, PlainText=text, KeyText=key_text)
        elif cipher == 'vigenere':
            key_text = data.get('KeyText', 'KEY')
            result = PolyAlphabeticVigenereCipher(mode=mode, PlainText=text, KeyText=key_text)
        elif cipher == 'railfence':
            rails = int(data.get('rails', 3))
            result = RailFence(mode=mode, text=text, rails=rails)
        elif cipher == 'monoalphabetic':
            result = MonoalphabeticCipher(mode=mode, word=text)
        elif cipher == 'playfair':
            keyword = data.get('keyword', 'MONARCHY')
            result = PlayFairCipher(mode=mode, text=text, keyword=keyword)
        elif cipher == 'hill':
            key = data.get('key', 'GYBNQKURP')
            result = HillCipher(mode=mode, text=text, key=key)
        elif cipher == 'rowtransposition':
            key_s = data.get('keyS', '4312567')
            result = RowTransposition(mode=mode, text=text, keyS=key_s)
        else:
            return jsonify({'error': 'Unknown cipher'}), 400

        return jsonify({'result': result, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
