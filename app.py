import qrcode
import os
import shutil
from flask import Flask, jsonify, request, render_template, send_file
from nacl.public import PrivateKey

app = Flask(__name__)

# Variable pour stocker l'adresse publique du wallet une fois récupérée
public_key = None

# Générer une clé privée et publique pour la connexion sécurisée
private_key = PrivateKey.generate()
dapp_public_key = private_key.public_key.encode().hex()

# Fonction pour générer l'URL de connexion Phantom
def generate_phantom_connect_url(callback_url):
    """
    Génère une URL que le wallet Phantom utilisera pour demander la connexion.
    """
    base_url = "https://phantom.app/ul/v1/connect"
    params = {
        "dapp_encryption_public_key": dapp_public_key,  # Clé publique générée
        "cluster": "devnet",  # Utilise 'devnet' pour le test, ou 'mainnet-beta' pour le réseau principal
        "app_url": callback_url,  # URL de l'application
        "redirect_link": callback_url  # URL de redirection après connexion
    }

    # Construction de l'URL avec les paramètres
    connection_url = base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return connection_url

# Fonction pour vider le répertoire temporaire avant de générer un nouveau QR code
def clear_tmp_directory():
    tmp_dir = '/tmp'
    try:
        for filename in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print("Répertoire temporaire vidé.")
    except Exception as e:
        print(f"Erreur lors du nettoyage du répertoire temporaire: {e}")

# Route pour l'index.html qui contient le bouton pour générer le QR code
@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)

# Route pour générer et renvoyer le QR code
@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    try:
        # Vider le répertoire temporaire avant de générer un nouveau QR code
        clear_tmp_directory()

        callback_url = request.host_url + 'phantom_callback'  # URL où Phantom renverra l'adresse publique
        print(f"Callback URL: {callback_url}")  # Debugging log

        # Génération de l'URL de connexion Phantom
        connection_url = generate_phantom_connect_url(callback_url)
        print(f"Connection URL: {connection_url}")  # Debugging log

        # Génération du QR code
        qr = qrcode.make(connection_url)
        
        # Enregistrer le QR code dans le dossier temporaire (/tmp sur Vercel)
        qr_path = os.path.join('/tmp', 'phantom_connect_qr.png')
        print(f"Saving QR code to {qr_path}")  # Debugging log
        qr.save(qr_path)

        return jsonify({'message': 'QR code generated', 'url': connection_url})
    except Exception as e:
        print(f"Erreur lors de la génération du QR code: {e}")  # Imprimer l'erreur dans la console
        return jsonify({'error': 'An error occurred while generating the QR code'}), 500

# Route pour récupérer l'adresse publique après la connexion
@app.route('/phantom_callback', methods=['GET'])
def phantom_callback():
    global public_key
    public_key = request.args.get('public_key')
    return render_template('index.html', public_key=public_key)

# Route pour afficher le QR code dans le HTML
@app.route('/get_qr_code', methods=['GET'])
def get_qr_code():
    qr_path = os.path.join('/tmp', 'phantom_connect_qr.png')
    if os.path.exists(qr_path):
        return send_file(qr_path, mimetype='image/png')
    else:
        return jsonify({'error': 'QR code not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
