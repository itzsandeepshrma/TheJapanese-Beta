// config/config.js
require('dotenv').config();

module.exports = {
    whatsapp: {
        sessionName: process.env.WHATSAPP_SESSION_NAME || 'whatsapp-session',
    },
    instagram: {
        username: process.env.INSTAGRAM_USERNAME,
        password: process.env.INSTAGRAM_PASSWORD,
    }
};
