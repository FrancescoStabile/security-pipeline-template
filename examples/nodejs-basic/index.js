const express = require('express');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());

// Basic middleware
app.use(express.json());

// Example route with potential security issue (for testing)
app.get('/user/:id', (req, res) => {
  const userId = req.params.id;
  
  // ⚠️ Potential SQL injection vulnerability (example for testing)
  // In real code, use parameterized queries
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  
  res.json({
    message: 'User data',
    userId: userId,
    query: query // Don't expose queries in real applications
  });
});

// Safe route example
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
