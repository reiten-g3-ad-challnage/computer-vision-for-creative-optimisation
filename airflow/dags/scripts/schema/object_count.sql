CREATE TABLE IF NOT EXISTS objects
(
    "game_id" TEXT NOT NULL,
    "object_count"  INT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);