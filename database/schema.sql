CREATE TABLE IF NOT EXISTS `users` (
  `user_id` TEXT PRIMARY KEY,
  `language` TEXT DEFAULT 'ja-JP' NOT NULL,
  `voice` TEXT DEFAULT 'ja-JP-Standard-A' NOT NULL,
  `speakingrate` REAL DEFAULT '1.0' NOT NULL,
  `pitch` REAL DEFAULT '0.0' NOT NULL
);

CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` TEXT PRIMARY KEY,
  `target_channel_id` TEXT DEFAULT '0' NOT NULL
);
