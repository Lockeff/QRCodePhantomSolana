// api/decodeBase58.js

const bs58 = require('bs58');

module.exports = (req, res) => {
  if (req.method === 'POST') {
    const { data } = req.body;
    if (!data) {
      return res.status(400).json({ error: 'Data is required' });
    }
    try {
      const decoded = bs58.decode(data);
      res.status(200).json({ decoded: decoded.toString('hex') });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
};
