			
CREATE TABLE IF NOT EXISTS performance
(
    "game_id" TEXT NOT NULL,
    "preview_link" TEXT DEFAULT NULL,
    "ER" FLOAT DEFAULT NULL,
    "CTR" FLOAT DEFAULT NULL,
    PRIMARY KEY ("game_id")
);
