const dotenv = require('dotenv');
const fs = require('fs');
const path = require('path');

dotenv.config();

const REQUIRED_ENV_VARS = ['INSTAGRAM_USERNAME', 'INSTAGRAM_PASSWORD', 'PROXY_URL', 'SECRET_KEY'];

REQUIRED_ENV_VARS.forEach((varName) => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});

const isDevMode = process.env.NODE_ENV !== 'production';

const LOG_DIR = path.join(__dirname, 'logs');
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

module.exports = {
  INSTAGRAM_USERNAME: process.env.INSTAGRAM_USERNAME,
  INSTAGRAM_PASSWORD: process.env.INSTAGRAM_PASSWORD,
  PROXY_URL: process.env.PROXY_URL,
  SECRET_KEY: process.env.SECRET_KEY,
  MAX_RETRIES: process.env.MAX_RETRIES || 3,
  ACTION_DELAY: [
    parseInt(process.env.ACTION_DELAY_MIN, 10) || 3000,
    parseInt(process.env.ACTION_DELAY_MAX, 10) || 6000,
  ],
  CRON_SCHEDULE: process.env.CRON_SCHEDULE || '*/30 * * * *',
  IS_DEV_MODE: isDevMode,
  LOG_DIR: LOG_DIR,
  LOG_LEVEL: isDevMode ? 'debug' : 'info',
  DATABASE_URI: process.env.DATABASE_URI,
  ENABLE_SECURE_AUTH: process.env.ENABLE_SECURE_AUTH === 'true',
  ENCRYPTION_KEY: process.env.ENCRYPTION_KEY,
  PASSWORD_SALT_ROUNDS: 12,
  RATE_LIMIT: parseInt(process.env.RATE_LIMIT, 10) || 5,
  USER_AGENT: process.env.USER_AGENT || 'InstagramUserBot/1.0',
};
