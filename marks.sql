PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS "config";
CREATE TABLE "config" (
        `name`  TEXT,
        `value`  TEXT
);
INSERT INTO config VALUES('version', '1');

DROP TABLE IF EXISTS "subject";
CREATE TABLE IF NOT EXISTS "subject" (
        `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `name`  TEXT
);

DROP TABLE IF EXISTS "mark";
CREATE TABLE IF NOT EXISTS "mark" (
        `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `subject_id`    INTEGER,
        `date`  INTEGER,
        `mark`  TEXT,
        FOREIGN KEY(`subject_id`) REFERENCES subject(id)
);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('subject',1);
INSERT INTO sqlite_sequence VALUES('mark','1');
COMMIT;
