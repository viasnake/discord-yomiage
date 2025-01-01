CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INTEGER PRIMARY KEY,
  `voice_languagecode` TEXT DEFAULT 'ja-JP',
  `voice_name` TEXT DEFAULT 'ja-JP-Wavenet-C',
  `audioconfig_speakingrate` TEXT DEFAULT '1.0'
);
