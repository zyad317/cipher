# CipherLab — Flask Cryptography Suite

A Flask web application exposing 9 classical cryptography algorithms via a clean REST API and dark-themed UI.

## Algorithms Included
- Caesar Cipher
- Auto-Key Cipher
- Vigenère Cipher (Polyalphabetic)
- Playfair Cipher
- Hill Cipher
- Monoalphabetic Cipher
- Rail Fence Cipher
- Row Transposition Cipher
- DES Algorithm

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open http://localhost:5000 in your browser.

## API Usage

**POST** `/api/cipher`

```json
{
  "algorithm": "caesar",
  "mode": "encode",
  "text": "Hello World",
  "key": "",
  "extra": { "shift": 3 }
}
```

### Algorithm values
| algorithm        | key field         | extra fields       |
|-----------------|-------------------|--------------------|
| caesar          | —                 | shift (int)        |
| autokey         | keyword           | —                  |
| vigenere        | keyword           | —                  |
| playfair        | keyword           | —                  |
| hill            | key matrix text   | —                  |
| monoalphabetic  | —                 | —                  |
| railfence       | —                 | rails (int)        |
| rowtransposition| key (digits/word) | —                  |
| des             | 64-bit hex key    | —                  |

### Mode values
- `encode` — encrypt the text
- `decode` — decrypt the text (DES encode-only)

## Project Structure
```
cipher_app/
├── app.py                  # Flask routes & API
├── requirements.txt
├── templates/
│   └── index.html          # Frontend UI
└── algorithms/             # Original unmodified algorithm files
    ├── AutoKeyAlgorithm.py
    ├── CaesarAlgorithm.py
    ├── DESAlgorithm.py
    ├── HillCipherAlgorithm.py
    ├── MonoalphabeticAlgorithm.py
    ├── PlayFairAlgorithm.py
    ├── PolyAlphabeticVigenereAlgorithm.py
    ├── RailFenceAlgorithm.py
    └── RowTranspositionAlgorithm.py
```
