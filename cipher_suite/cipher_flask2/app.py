from flask import Flask, render_template, request, jsonify
import sys, os, traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "algorithms"))

import CaesarAlgorithm
import MonoalphabeticAlgorithm
import PlayFairAlgorithm
import PolyAlphabeticVigenereAlgorithm
import AutoKeyAlgorithm
import RailFenceAlgorithm
import RowTranspositionAlgorithm
import HillCipherAlgorithm
import DESAlgorithm
app = Flask(__name__)

ALGO_META = {
    "caesar": {
        "name": "Caesar Cipher",
        "description": "Shifts each letter by a fixed number of positions in the alphabet.",
        "params": [{"id": "shift", "label": "Shift", "default": "3", "type": "number"}],
    },
    "monoalphabetic": {
        "name": "Monoalphabetic Cipher",
        "description": "Substitutes each letter with a fixed shuffled alphabet.",
        "params": [],
    },
    "playfair": {
        "name": "Playfair Cipher",
        "description": "Encrypts digraphs using a 5×5 matrix built from a keyword.",
        "params": [{"id": "key", "label": "Keyword", "default": "MONARCHY", "type": "text"}],
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "description": "Repeating keyword shifts — each letter is keyed independently.",
        "params": [{"id": "key", "label": "Keyword", "default": "KEY", "type": "text"}],
    },
    "autokey": {
        "name": "Autokey Cipher",
        "description": "Seed key extends with the plaintext itself — breaks repeating key patterns.",
        "params": [{"id": "key", "label": "Initial Key", "default": "SECRET", "type": "text"}],
    },
    "railfence": {
        "name": "Rail Fence Cipher",
        "description": "Writes text in a zigzag pattern across N rails, then reads row by row.",
        "params": [{"id": "rails", "label": "Number of Rails", "default": "3", "type": "number"}],
    },
    "rowtransposition": {
        "name": "Row Transposition",
        "description": "Rearranges columns based on the alphabetical order of the key.",
        "params": [{"id": "key", "label": "Column Key", "default": "4312567", "type": "text"}],
    },
    "hillcipher": {
        "name": "Hill Cipher",
        "description": "Matrix multiplication mod 26. Key must form an invertible square matrix.",
        "params": [{"id": "key", "label": "Key (letters)", "default": "GYBNQKURP", "type": "text"}],
    },
    "des": {
    "name": "Data Encryption Standard (DES)",
    "description": "Symmetric block cipher operating on 64-bit blocks with a 56-bit key (8 bytes including parity). Uses 16-round Feistel structure.",
    "params": [{"id": "key","label": "Key (8 characters / 64-bit)","default": "password","type": "text"}],
},
    
}


@app.route("/")
def index():
    return render_template("index.html", algorithms=ALGO_META)


@app.route("/cipher", methods=["POST"])
def cipher():
    data   = request.get_json(force=True)
    algo   = data.get("algorithm", "")
    mode   = data.get("mode", "encode")
    text   = data.get("text", "")
    params = data.get("params", {})

    if not text.strip():
        return jsonify({"error": "Input text is empty."}), 400

    try:
        if algo == "caesar":
            result = CaesarAlgorithm.CaesarCipher(mode, text, params.get("shift", 3))

        elif algo == "monoalphabetic":
            result = MonoalphabeticAlgorithm.MonoalphabeticCipher(mode, text.lower())

        elif algo == "playfair":
            result = PlayFairAlgorithm.PlayFairCipher(mode, text, params.get("key", "MONARCHY"))

        elif algo == "vigenere":
            result = PolyAlphabeticVigenereAlgorithm.PolyAlphabeticVigenèreCipher(
                mode, text, params.get("key", "KEY"))

        elif algo == "autokey":
            result = AutoKeyAlgorithm.AutoKey(mode, text, params.get("key", "SECRET"))

        elif algo == "railfence":
            result = RailFenceAlgorithm.RailFence(mode, text, int(params.get("rails", 3)))

        elif algo == "rowtransposition":
            result = RowTranspositionAlgorithm.RowTransposition(
                mode, text, params.get("key", "4312567"))

        elif algo == "hillcipher":
            result = HillCipherAlgorithm.HillCipher(mode, text, params.get("key", "GYBNQKURP"))
        
        elif algo == "des":
            result = DESAlgorithm.CipherEncode(mode, text, params.get("key", "GYBNQKURP"))
        
        
        else:
            return jsonify({"error": f"Unknown algorithm: {algo}"}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    app.run(debug=True)
