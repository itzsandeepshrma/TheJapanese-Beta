const mongoose = require('mongoose');
const { DATABASE_URI } = require('../config');

async function connectDB() {
  try {
    await mongoose.connect(DATABASE_URI, { useNewUrlParser: true, useUnifiedTopology: true });
    console.log('Connected to database');
  } catch (error) {
    console.error('Error connecting to database', error);
    process.exit(1);
  }
}

module.exports = { connectDB };
