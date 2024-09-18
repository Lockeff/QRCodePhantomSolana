const nacl = require('tweetnacl');
const bs58 = require('bs58');

let keyPair = null;

module.exports = (req, res) => {
  if (keyPair) {
    res.status(200).json({
      publicKey: Array.from(keyPair.publicKey),
      secretKey: Array.from(keyPair.secretKey),
    });
  } else {
    res.status(404).json({ error: 'Paire de clés non trouvée' });
  }
};
