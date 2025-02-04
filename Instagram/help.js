const { startScheduler } = require('./utils/scheduler');
const { likeHashtag } = require('./commands/like');
const { followUser } = require('./commands/follow');
const { unfollowUser } = require('./commands/unfollow');
const { postPhoto } = require('./commands/post');
const { uploadStory } = require('./commands/story');
const { autoReply } = require('./commands/reply');
const { connectDB } = require('./utils/database');

async function startBot() {
  await connectDB();
  startScheduler();

  likeHashtag('nature', 10);
  followUser('target_user');
  unfollowUser('target_user');
  postPhoto('./images/photo.jpg', 'My new post!');
  uploadStory('./images/story.jpg');
  autoReply();
}

startBot();
