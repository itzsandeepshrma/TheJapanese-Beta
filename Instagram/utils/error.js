const fs = require('fs');
const path = require('path');
const { INSTAGRAM_USERNAME } = require('../config');

const logFile = path.join(__dirname, `../logs/${INSTAGRAM_USERNAME}_errors.log`);

if (!fs.existsSync(path.dirname(logFile))) {
  fs.mkdirSync(path.dirname(logFile), { recursive: true });
}

function logError(error) {
  const timestamp = new Date().toISOString();
  const message = `[${timestamp}] Error: ${error}\n`;

  fs.appendFileSync(logFile, message, 'utf8');
}

module.exports = { logError };
