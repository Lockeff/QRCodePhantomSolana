const bs58 = require('bs58');

module.exports = (req, res) => {
  const { data } = req.body;
  try {
    const decoded = bs58.decode(data);
    res.status(200).json({ decoded: Array.from(decoded) });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};
