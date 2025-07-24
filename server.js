// Load environment variables from .env file
require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { Client } = require('pg');
const bcrypt = require('bcrypt');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Database connection
const connectionString = process.env.SUPABASE_DB_URL;
let client;

if (connectionString) {
  client = new Client({
    connectionString,
  });

  client.connect()
    .then(() => {
      console.log('Connected to PostgreSQL database!');
    })
    .catch((err) => {
      console.error('Connection error:', err.message);
    });
}

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'API is running' });
});

// Admin routes
app.get('/admin', (req, res) => {
  const { ADMIN_EMAIL, ADMIN_PASSWORD } = process.env;
  res.json({ 
    message: 'Admin configuration loaded', 
    adminConfigured: !!(ADMIN_EMAIL && ADMIN_PASSWORD) 
  });
});

// Admin login route
app.post('/admin/login', async (req, res) => {
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminPassword = process.env.ADMIN_PASSWORD;
  
  if (!adminEmail || !adminPassword) {
    return res.status(500).json({ error: 'Admin credentials not configured on server' });
  }
  
  try {
    // Check if email matches
    if (req.body.email !== adminEmail) {
      return res.status(401).json({ 
        success: false, 
        message: 'Invalid admin credentials' 
      });
    }
    
    // Compare password using bcrypt
    const match = await bcrypt.compare(req.body.password, adminPassword);
    
    if (match) {
      return res.json({ 
        success: true, 
        message: 'Admin login successful',
        admin: { email: adminEmail }
      });
    } else {
      return res.status(401).json({ 
        success: false, 
        message: 'Invalid admin credentials' 
      });
    }
  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({ 
      success: false, 
      message: 'Server error during authentication' 
    });
  }
});

// Utility endpoint to generate hashed password (for development only)
app.get('/generate-hash/:password', async (req, res) => {
  try {
    const password = req.params.password;
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    res.json({ hashedPassword });
  } catch (error) {
    console.error('Hash generation error:', error);
    res.status(500).json({ error: 'Failed to generate hash' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Admin email: ${process.env.ADMIN_EMAIL}`);
  console.log('To generate a hashed password, visit: /generate-hash/yourpassword');
});