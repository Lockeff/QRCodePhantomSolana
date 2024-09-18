from flask import Flask, request, jsonify
from flask_cors import CORS
import base58
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

app = Flask(__name__)
CORS(app)

# Stockage en mémoire pour le keyPair (pour simplifier)
key_pair = None

# Endpoint pour générer et stocker le keyPair
@app.route('/generate-keypair', methods=['GET'])
def generate_keypair():
    global key_pair
    key_pair = PrivateKey.generate()
    public_key_base58 = base58.b58encode(key_pair.public_key.encode()).decode('utf-8')
    return jsonify({'publicKey': public_key_base58})

# Endpoint pour récupérer la clé publique
@app.route('/public-key', methods=['GET'])
def get_public_key():
    if not key_pair:
        return jsonify({'error': 'Key pair not generated yet'}), 400
    public_key_base58 = base58.b58encode(key_pair.public_key.encode()).decode('utf-8')
    return jsonify({'publicKey': public_key_base58})

# Endpoint pour décoder Base58
@app.route('/decode-base58', methods=['POST'])
def decode_base58():
    data = request.json.get('data')
    try:
        decoded = base58.b58decode(data)
        return jsonify({'decoded': list(decoded)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint pour encoder en Base58
@app.route('/encode-base58', methods=['POST'])
def encode_base58():
    data = request.json.get('data')
    try:
        data_bytes = bytes(data)
        encoded = base58.b58encode(data_bytes).decode('utf-8')
        return jsonify({'encoded': encoded})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint pour obtenir le keyPair (pour le déchiffrement)
@app.route('/keypair', methods=['GET'])
def get_keypair():
    if not key_pair:
        return jsonify({'error': 'Key pair not generated yet'}), 400
    return jsonify({
        'publicKey': list(key_pair.public_key.encode()),
        'secretKey': list(key_pair.encode())
    })

# Endpoint pour déchiffrer la payload
@app.route('/decrypt', methods=['POST'])
def decrypt():
    global key_pair
    if not key_pair:
        return jsonify({'error': 'Key pair not generated yet'}), 400

    data = request.json.get('data')
    nonce = request.json.get('nonce')
    phantom_encryption_public_key = request.json.get('phantom_encryption_public_key')

    try:
        decoded_data = base58.b58decode(data)
        decoded_nonce = base58.b58decode(nonce)
        decoded_phantom_public_key = base58.b58decode(phantom_encryption_public_key)

        # Clés
        phantom_public_key = PublicKey(decoded_phantom_public_key)
        box = Box(key_pair, phantom_public_key)

        # Déchiffrement
        decrypted = box.decrypt(decoded_data, decoded_nonce)

        # Conversion en JSON
        decrypted_json = decrypted.decode('utf-8')
        decrypted_data = json.loads(decrypted_json)

        return jsonify({'decryptedData': decrypted_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
