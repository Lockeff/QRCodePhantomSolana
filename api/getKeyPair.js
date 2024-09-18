// api/getKeyPair.js

let keyStore = {}; // Assurez-vous que ceci est partagé entre les fonctions ou utilisez une vraie base de données

export default function handler(req, res) {
    if (req.method === 'GET') {
        const { sessionId } = req.query;
        if (!sessionId) {
            return res.status(400).json({ error: 'Paramètre sessionId manquant' });
        }
        const keyPair = keyStore[sessionId];
        if (!keyPair) {
            return res.status(404).json({ error: 'Paire de clés non trouvée' });
        }
        return res.status(200).json({ publicKey: keyPair.publicKey, secretKey: keyPair.secretKey });
    } else {
        return res.status(405).json({ error: 'Méthode non autorisée' });
    }
}
