// src/App.tsx

import React, { useState, useEffect } from 'react';
import nacl from 'tweetnacl';
import bs58 from 'bs58';
import QRCode from 'qrcode';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

function App() {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [publicKey, setPublicKey] = useState<string>('');
  const [logs, setLogs] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Fonction pour ajouter un message aux logs
  const logMessage = (message: string) => {
    setLogs((prevLogs) => [...prevLogs, message]);
  };

  // Fonction pour dériver un seed à partir du sessionId
  const deriveSeed = async (sessionId: string): Promise<Uint8Array> => {
    const encoder = new TextEncoder();
    const data = encoder.encode(sessionId);
    const hashBuffer = await window.crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return new Uint8Array(hashArray.slice(0, 32));
  };

  // Générer la paire de clés déterministe
  const generateKeyPair = async (sessionId: string): Promise<nacl.BoxKeyPair> => {
    const seed = await deriveSeed(sessionId);
    return nacl.box.keyPair.fromSeed(seed);
  };

  // Générer le QR Code
  const generateQRCode = async () => {
    const sessionId = uuidv4();
    logMessage(`Session ID généré : ${sessionId}`);

    try {
      const keyPair = await generateKeyPair(sessionId);
      logMessage('Paire de clés générée de manière déterministe');

      const appUrl = window.location.origin;
      const redirectLink = `${appUrl}/?sessionId=${encodeURIComponent(sessionId)}`;

      const phantomDeepLink = `https://phantom.app/ul/v1/connect?app_url=${encodeURIComponent(
        appUrl
      )}&dapp_encryption_public_key=${encodeURIComponent(bs58.encode(keyPair.publicKey))}&redirect_link=${encodeURIComponent(
        redirectLink
      )}&cluster=mainnet-beta`;

      logMessage(`Lien Phantom Deep Link généré : ${phantomDeepLink}`);

      const qrCodeDataUrl = await QRCode.toDataURL(phantomDeepLink);
      setQrCodeUrl(qrCodeDataUrl);
      logMessage('QR Code généré');
    } catch (error: any) {
      console.error('Erreur lors de la génération du QR Code :', error);
      logMessage(`Erreur : ${error.message}`);
      setError(error.message);
    }
  };

  // Déchiffrer la payload
  const decryptPayload = (data: string, nonce: string, sharedSecret: Uint8Array) => {
    if (!sharedSecret) {
      throw new Error('Secret partagé manquant');
    }

    const decryptedData = nacl.box.open.after(bs58.decode(data), bs58.decode(nonce), sharedSecret);
    if (!decryptedData) {
      throw new Error('Échec du déchiffrement');
    }

    return JSON.parse(new TextDecoder().decode(decryptedData));
  };

  // Récupérer la clé publique depuis l'URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('sessionId');

    if (sessionId) {
      logMessage('Paramètres de redirection détectés');

      const fetchAndDecrypt = async () => {
        try {
          const keyPair = await generateKeyPair(sessionId);
          logMessage('Paire de clés dérivée à partir du sessionId');

          // Simuler la récupération de données chiffrées (à ajuster selon votre logique)
          // Ici, nous supposons que les paramètres 'data' et 'nonce' sont présents dans l'URL
          const data = urlParams.get('data');
          const nonce = urlParams.get('nonce');

          if (data && nonce) {
            const sharedSecret = nacl.box.before(bs58.decode(keyPair.publicKey), keyPair.secretKey);
            logMessage('Secret partagé calculé');

            const decryptedData = decryptPayload(data, nonce, sharedSecret);
            logMessage('Données déchiffrées');

            // Afficher la clé publique du wallet utilisateur
            setPublicKey(decryptedData.public_key);
            logMessage(`Clé publique du wallet utilisateur : ${decryptedData.public_key}`);

            // Nettoyer les paramètres de l'URL
            window.history.replaceState({}, document.title, '/');
          } else {
            logMessage('Paramètres "data" et "nonce" manquants dans l\'URL');
          }
        } catch (error: any) {
          console.error('Erreur lors de la récupération de la clé publique :', error);
          logMessage(`Erreur : ${error.message}`);
          setError(error.message);
        }
      };

      fetchAndDecrypt();
    } else {
      logMessage('Aucune donnée de redirection à traiter');
    }
  }, []);

  return (
    <div className="App">
      <h1>Connexion à Phantom Wallet via QR Code</h1>
      <button onClick={generateQRCode}>Générer le QR Code</button>
      {qrCodeUrl && (
        <div>
          <img src={qrCodeUrl} alt="QR Code" />
        </div>
      )}
      {publicKey && (
        <div>
          <h2>Votre clé publique Solana :</h2>
          <p>{publicKey}</p>
        </div>
      )}
      <h2>Logs :</h2>
      <div className="logs">
        {logs.map((log, index) => (
          <pre key={index}>{log}</pre>
        ))}
      </div>
      {error && (
        <div className="error">
          <h2>Erreur :</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default App;
