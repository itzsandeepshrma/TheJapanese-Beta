// config/config.js
require('dotenv').config();
const { exit } = require('process');

// Validation Function to Check Required Environment Variables
const validateEnvVars = () => {
    const requiredVars = [
        'INSTAGRAM_USERNAME',
        'INSTAGRAM_PASSWORD',
        'DB_URI',
        'DB_NAME',
        'PORT',
        'APP_MODE',
    ];

    requiredVars.forEach((varName) => {
        if (!process.env[varName]) {
            console.error(`ERROR: Missing required environment variable: ${varName}`);
            exit(1); // Exit if any required environment variable is missing
        }
    });

    // Additional validations for formats, e.g., valid phone numbers, API keys
    const phonePattern = /^[+]?[0-9]{10,15}$/; // Example: Validate phone numbers
    if (process.env.WHATSAPP_USER_PHONE && !phonePattern.test(process.env.WHATSAPP_USER_PHONE)) {
        console.error('ERROR: Invalid phone number format for WHATSAPP_USER_PHONE');
        exit(1);
    }
};

// Call the function to ensure environment variables are validated
validateEnvVars();

// Sanitization function (for example, stripping extra spaces in strings)
const sanitizeInput = (input) => {
    return input ? input.trim() : input;
};

module.exports = {
    whatsapp: {
        sessionName: sanitizeInput(process.env.WHATSAPP_SESSION_NAME) || 'whatsapp-session',
        apiKey: sanitizeInput(process.env.WHATSAPP_API_KEY) || '', // Secure API Key storage
        userPhone: process.env.WHATSAPP_USER_PHONE ? sanitizeInput(process.env.WHATSAPP_USER_PHONE) : '', // Ensure clean input
    },
    instagram: {
        username: sanitizeInput(process.env.INSTAGRAM_USERNAME),
        password: sanitizeInput(process.env.INSTAGRAM_PASSWORD),
        apiKey: sanitizeInput(process.env.INSTAGRAM_API_KEY) || '', // Ensure clean API key
    },
    common: {
        appMode: process.env.APP_MODE || 'production', // Default to 'production' if not specified
        logLevel: process.env.LOG_LEVEL || 'info', // Default log level is info
    },
    db: {
        uri: process.env.DB_URI || 'mongodb://localhost:27017/myapp', // Default to local MongoDB URI
        name: process.env.DB_NAME || 'mydb', // Default DB name
    },
    server: {
        port: process.env.PORT || 3000, // Default to port 3000
    }
};
