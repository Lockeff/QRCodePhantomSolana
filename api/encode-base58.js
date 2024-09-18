const bs58 = require('bs58');

module.exports = (req, res) => {
  const { data } = req.body;
  try {
    const buffer = Buffer.from(data);
    const encoded = bs58.encode(buffer);
    res.status(200).json({ encoded });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};
