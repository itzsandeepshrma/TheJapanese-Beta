const cron = require('node-cron');
const { likeHashtag, followUser } = require('../commands/like');
const { autoReply } = require('../commands/reply');
const { logError } = require('./error');
const { MAX_RETRIES, CRON_SCHEDULE, ACTION_DELAY } = require('../config');

function randomDelay() {
  const min = ACTION_DELAY[0];
  const max = ACTION_DELAY[1];
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function executeWithRetry(action, retries = 0) {
  return new Promise(async (resolve, reject) => {
    try {
      await action();
      resolve();
    } catch (error) {
      if (retries < MAX_RETRIES) {
        console.log(`Retrying due to error: ${error.message}`);
        setTimeout(() => resolve(executeWithRetry(action, retries + 1)), randomDelay());
      } else {
        logError(error.message);
        reject(error);
      }
    }
  });
}

function startScheduler() {
  cron.schedule(CRON_SCHEDULE, () => {
    console.log('Starting scheduled tasks...');
    executeWithRetry(() => likeHashtag('nature', 10));
    executeWithRetry(() => followUser('target_user'));
    executeWithRetry(() => autoReply());
  });
}

module.exports = { startScheduler };
