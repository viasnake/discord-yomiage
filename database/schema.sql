CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INTEGER PRIMARY KEY,
  `voice_languagecode` TEXT DEFAULT 'ja-JP',
  `voice_name` TEXT DEFAULT 'ja-JP-Wavenet-C',
  `audioconfig_speakingrate` REAL DEFAULT '1.0',
  `audioconfig_pitch` REAL DEFAULT '0.0'
);

CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` INTEGER PRIMARY KEY,
  `channel_id` INTEGER DEFAULT NULL
);
