const express = require('express');
const path = require('path');
const app = express();
const port = 80;

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/search', (req, res) => {
  res.sendFile(path.join(__dirname, 'search.html'));
});

// Your new "encrypted API" endpoint
app.get('/s3nd4p1hUggingf4ce', (req, res) => {
  // You can log the query or do whatever encryption/processing you want here
  console.log('Encryption API called with query:', req.query.q);

  // Simulate delay or processing (optional)
  setTimeout(() => {
    res.json({ status: 'success', message: 'Query logged and encrypted' });
  }, 500); // 0.5s delay for demo
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
