const chalk = require('chalk');
const { WAConnection, MessageType, Mimetype } = require('@adiwajshing/baileys');
const fs = require('fs');
const crypto = require('crypto');
require('dotenv').config();

// Load environment variables
const SESSION_KEY = process.env.SESSION_KEY || 'yourSecretKey'; // Use a strong secret key

// Generate or retrieve the WhatsApp session string
async function generateSession() {
    const conn = new WAConnection();
    conn.version = [3, 3234, 9]; // WhatsApp Web version
    conn.logger.level = 'warn'; // Log warnings only

    // Event handler for connecting
    conn.on('connecting', () => {
        console.log(`${chalk.green.bold('Team')} ${chalk.blue.bold('JapaneseBot')}
${chalk.white.italic('Connecting to WhatsApp... Please Wait.')}`);
    });

    // Event handler for successful connection
    conn.on('open', async () => {
        console.log(`${chalk.green.bold('Connected!')} ${chalk.blue.bold('WhatsApp session established.')}`);

        // Generate the session string
        const sessionString = conn.base64EncodedAuthInfo();
        const encryptedSession = encryptSession(sessionString); // Encrypt the session

        // Save the encrypted session string to a config file
        saveSession(encryptedSession);

        // Display the session string to the user with a warning to keep it private
        console.log(`${chalk.green.bold('Session Generated:')} ${chalk.yellow.bold(sessionString)}`);
        console.log(`${chalk.red.bold('Do not share this session with anyone!')}`);
        process.exit(0);
    });

    // Connect to WhatsApp Web
    await conn.connect();
}

// Encrypt the session string using AES encryption
function encryptSession(sessionString) {
    const cipher = crypto.createCipher('aes-256-cbc', SESSION_KEY);
    let encrypted = cipher.update(sessionString, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
}

// Save the encrypted session to a config file
function saveSession(encryptedSession) {
    const configFilePath = 'config.env';

    // Check if the config file exists, if not create it
    if (!fs.existsSync(configFilePath)) {
        fs.writeFileSync(configFilePath, `SESSION="${encryptedSession}"`);
        console.log(chalk.green.bold(`Session saved in ${configFilePath}`));
    } else {
        console.log(chalk.red.bold('Config file already exists. Please delete it if you want to overwrite.'));
    }
}

// Start the bot process
generateSession().catch((err) => {
    console.error(chalk.red.bold('Error:'), err);
});
