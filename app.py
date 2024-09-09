import qrcode
import os
from flask import Flask, jsonify, request, render_template, send_file

app = Flask(__name__)

# Variable pour stocker l'adresse publique du wallet une fois récupérée
public_key = None

# Fonction pour générer l'URL de connexion Phantom
def generate_phantom_connect_url(callback_url):
    """
    Génère une URL que le wallet Phantom utilisera pour demander la connexion.
    """
    return f"https://phantom.app/ul/v1/connect?app_url={callback_url}"

# Route pour l'index.html qui contient le bouton pour générer le QR code
@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)

# Route pour générer et renvoyer le QR code
@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    try:
        callback_url = request.host_url + 'phantom_callback'  # URL où Phantom renverra l'adresse publique
        connection_url = generate_phantom_connect_url(callback_url)

        # Génération du QR code
        qr = qrcode.make(connection_url)
        
        # Enregistrer le QR code dans un fichier
        qr_path = os.path.join('static', 'phantom_connect_qr.png')
        qr.save(qr_path)

        return jsonify({'message': 'QR code generated', 'url': connection_url})
    except Exception as e:
        print(f"Erreur lors de la génération du QR code: {e}")
        return jsonify({'error': 'An error occurred'}), 500

# Route pour récupérer l'adresse publique après la connexion
@app.route('/phantom_callback', methods=['GET'])
def phantom_callback():
    global public_key
    public_key = request.args.get('public_key')
    return render_template('index.html', public_key=public_key)

# Route pour afficher le QR code dans le HTML
@app.route('/get_qr_code', methods=['GET'])
def get_qr_code():
    qr_path = os.path.join('static', 'phantom_connect_qr.png')
    if os.path.exists(qr_path):
        return send_file(qr_path, mimetype='image/png')
    else:
        return jsonify({'error': 'QR code not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
