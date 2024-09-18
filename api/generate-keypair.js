const nacl = require('tweetnacl');
const bs58 = require('bs58');

let keyPair = null;

module.exports = (req, res) => {
  if (!keyPair) {
    keyPair = nacl.box.keyPair();
  }
  const publicKeyBase58 = bs58.encode(keyPair.publicKey);
  res.status(200).json({ publicKey: publicKeyBase58 });
};
