from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from AutoKeyAlgorithm import AutoKey
from CaesarAlgorithm import CaesarCipher
from DESAlgorithm import CipherEncode ,CipherDecode
from HillCipherAlgorithm import HillCipher
from MonoalphabeticAlgorithm import MonoalphabeticCipher
from PlayFairAlgorithm import PlayFairCipher
from PolyAlphabeticVigenereAlgorithm import PolyAlphabeticVigenèreCipher
from RailFenceAlgorithm import RailFence
from RowTranspositionAlgorithm import RowTransposition

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cipher', methods=['POST'])
def cipher():
    data = request.get_json()
    algorithm = data.get('algorithm')
    mode = data.get('mode', 'encode')
    text = data.get('text', '')
    key = data.get('key', '')
    extra = data.get('extra', {})

    try:
        result = None

        if algorithm == 'autokey':
            result = AutoKey(mode=mode, PlainText=text, KeyText=key)

        elif algorithm == 'caesar':
            shift = int(extra.get('shift', 3))
            result = CaesarCipher(mode=mode, UserText=text, key=shift)
        elif algorithm == 'des':
            if mode == 'decode':
                result = CipherDecode(mode=mode, PlainText=text, KeyText=key or '133457799BBCDFF1')
            else:
                result = CipherEncode(mode=mode, PlainText=text, KeyText=key or '133457799BBCDFF1')
        
        
        
        elif algorithm == 'hill':
            result = HillCipher(mode=mode, text=text, key=key if key else "GYBNQKURP")

        elif algorithm == 'monoalphabetic':
            result = MonoalphabeticCipher(mode=mode, word=text)

        elif algorithm == 'playfair':
            result = PlayFairCipher(mode=mode, text=text, keyword=key if key else "MONARCHY")

        elif algorithm == 'vigenere':
            result = PolyAlphabeticVigenèreCipher(mode=mode, PlainText=text, KeyText=key)

        elif algorithm == 'railfence':
            rails = int(extra.get('rails', 3))
            result = RailFence(mode=mode, text=text, rails=rails)

        elif algorithm == 'rowtransposition':
            result = RowTransposition(mode=mode, text=text, keyS=key if key else "4312567")

        else:
            return jsonify({'error': 'Unknown algorithm'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
