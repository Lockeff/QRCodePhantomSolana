from nacl.public import PrivateKey

# Générer une nouvelle clé privée
private_key = PrivateKey.generate()

# Obtenir la clé publique
public_key = private_key.public_key

# Afficher la clé privée et la clé publique
print("Private Key:", private_key.encode().hex())
print("Public Key:", public_key.encode().hex())