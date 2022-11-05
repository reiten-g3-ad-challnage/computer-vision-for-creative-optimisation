			
CREATE TABLE IF NOT EXISTS colors
(
    "game_id" TEXT NOT NULL,
    "dom_color_1" TEXT DEFAULT NULL,
    "dom_color_2" TEXT DEFAULT NULL,
    "dom_prct_1" FLOAT DEFAULT NULL,
    "dom_prct_2" FLOAT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);
