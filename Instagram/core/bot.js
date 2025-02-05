const { IgApiClient } = require("instagram-private-api");
const ig = new IgApiClient();

async function login() {
    ig.state.generateDevice("your_username");
    await ig.account.login("your_username", "your_password");
    console.log("✅ Instagram Bot is Running...");
}

login();
