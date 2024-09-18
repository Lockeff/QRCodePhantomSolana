from flask import Flask, request, jsonify
from base58 import b58encode, b58decode
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import RawEncoder
import json

app = Flask(__name__)

# Stockage de la paire de clés en mémoire (pour simplifier)
keypair = None

@app.route('/generate-keypair', methods=['GET'])
def generate_keypair():
    global keypair
    keypair = PrivateKey.generate()
    public_key_base58 = b58encode(keypair.public_key.encode()).decode('utf-8')
    return jsonify({'publicKey': public_key_base58})

@app.route('/public-key', methods=['GET'])
def get_public_key():
    if keypair is None:
        return jsonify({'error': 'La paire de clés n\'a pas encore été générée'}), 400
    public_key_base58 = b58encode(keypair.public_key.encode()).decode('utf-8')
    return jsonify({'publicKey': public_key_base58})

@app.route('/decode-base58', methods=['POST'])
def decode_base58_route():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Aucune donnée fournie'}), 400
    try:
        decoded = b58decode(data)
        return jsonify({'decoded': list(decoded)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/encode-base58', methods=['POST'])
def encode_base58_route():
    data = request.json.get('data')
    if data is None:
        return jsonify({'error': 'Aucune donnée fournie'}), 400
    try:
        # Supposons que les données sont une liste d'entiers
        byte_data = bytes(data)
        encoded = b58encode(byte_data).decode('utf-8')
        return jsonify({'encoded': encoded})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/keypair', methods=['GET'])
def get_keypair():
    if keypair is None:
        return jsonify({'error': 'La paire de clés n\'a pas encore été générée'}), 400
    public_key_bytes = keypair.public_key.encode()
    secret_key_bytes = keypair.encode()
    return jsonify({
        'publicKey': list(public_key_bytes),
        'secretKey': list(secret_key_bytes)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
