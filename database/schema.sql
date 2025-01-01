CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INTEGER PRIMARY KEY,
  `voice_languagecode` TEXT DEFAULT 'ja-JP' NOT NULL,
  `voice_name` TEXT DEFAULT 'ja-JP-Wavenet-C' NOT NULL,
  `audioconfig_speakingrate` REAL DEFAULT '1.0' NOT NULL,
  `audioconfig_pitch` REAL DEFAULT '0.0' NOT NULL
);

CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` INTEGER PRIMARY KEY,
  `target_channel_id` INTEGER DEFAULT '0' NOT NULL
);
