CREATE TABLE IF NOT EXISTS face_emotions
(
    "game_id" TEXT NOT NULL,
    "emotion_x" TEXT DEFAULT NULL,
    "gender_x" TEXT DEFAULT NULL,
    "race_x" TEXT DEFAULT NULL,
    "emotion_y" TEXT DEFAULT NULL,
    "race_y" TEXT DEFAULT NULL,
    "gender_y" TEXT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);
