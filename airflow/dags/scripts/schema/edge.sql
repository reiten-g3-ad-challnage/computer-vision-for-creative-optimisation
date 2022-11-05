CREATE TABLE IF NOT EXISTS edges
(
    "game_id" TEXT NOT NULL,
    "edges_pixel_count"  INT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);