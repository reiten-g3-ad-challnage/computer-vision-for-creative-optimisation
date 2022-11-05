CREATE TABLE IF NOT EXISTS logos
(
    "game_id" TEXT NOT NULL,
    "startX"  INT DEFAULT NULL,
    "startY" INT DEFAULT NULL,
    "height" INT DEFAULT NULL,
    "width" INT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);