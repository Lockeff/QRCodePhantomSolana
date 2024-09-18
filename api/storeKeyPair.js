// api/storeKeyPair.js

let keyStore = {}; // Stockage en mémoire (à remplacer par une base de données pour la production)

export default function handler(req, res) {
  // CORS Headers (si nécessaire)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'POST') {
    const { sessionId, publicKey, secretKey } = req.body;
    if (!sessionId || !publicKey || !secretKey) {
      return res.status(400).json({ error: 'Paramètres manquants' });
    }
    keyStore[sessionId] = { publicKey, secretKey };
    return res.status(200).json({ message: 'Paire de clés stockée avec succès' });
  } else {
    return res.status(405).json({ error: 'Méthode non autorisée' });
  }
}
