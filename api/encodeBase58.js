// api/encodeBase58.js

const bs58 = require('bs58');

module.exports = (req, res) => {
  if (req.method === 'POST') {
    const { data } = req.body;
    if (!data) {
      return res.status(400).json({ error: 'Data is required' });
    }
    try {
      const buffer = Buffer.from(data, 'hex'); // Expecting data in hex format
      const encoded = bs58.encode(buffer);
      res.status(200).json({ encoded });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
};
