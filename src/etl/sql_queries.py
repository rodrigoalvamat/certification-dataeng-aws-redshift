"""AWS Redshift SQL query definitions.

This module defines a constant for each AWS Redshift SQL statement.
Then, a list is created to group each SQL query category,
such as DROP, CREATE, COPY and INSERT.
"""
from config import Config

config = Config()

# DROP TABLES

DROP_TABLE_STAGING_EVENTS = 'DROP TABLE IF EXISTS staging_events;'
DROP_TABLE_STAGING_SONGS = 'DROP TABLE IF EXISTS staging_songs;'
DROP_TABLE_SONGPLAYS = 'DROP TABLE IF EXISTS songplays;'
DROP_TABLE_USERS = 'DROP TABLE IF EXISTS users;'
DROP_TABLE_SONGS = 'DROP TABLE IF EXISTS songs;'
DROP_TABLE_ARTISTS = 'DROP TABLE IF EXISTS artists;'
DROP_TABLE_TIME = 'DROP TABLE IF EXISTS time;'

# CREATE TABLES

CREATE_TABLE_STAGING_EVENTS = """
CREATE TABLE staging_events (
userId              TEXT,
firstName           TEXT,
lastName            TEXT,
gender              TEXT,
level               TEXT,
artist              TEXT,
song                TEXT,     
length              FLOAT,
sessionId           SMALLINT,
auth                TEXT,
itemInSession       SMALLINT, 
location            TEXT,
registration        DECIMAL(13,0),
ts                  BIGINT,
page                TEXT,
userAgent           TEXT,
status              SMALLINT,
method              TEXT
) diststyle auto;
"""

CREATE_TABLE_STAGING_SONGS = """
CREATE TABLE staging_songs (
song_id             TEXT,
title               TEXT,
duration            FLOAT,
year                INTEGER,
num_songs           INTEGER,
artist_id           TEXT,
artist_name         TEXT,
artist_location     TEXT,
artist_latitude     DOUBLE PRECISION,
artist_longitude    DOUBLE PRECISION
) diststyle auto;
"""

CREATE_TABLE_SONGPLAYS = """
CREATE TABLE songplays (
songplay_id         TEXT                NOT NULL,
level               TEXT                NOT NULL,
location            TEXT                NOT NULL,
user_agent          TEXT                NOT NULL,
session_id          SMALLINT            NOT NULL,
user_id             INTEGER             NOT NULL,
song_id             TEXT                        ,
artist_id           TEXT                        ,
start_time          TIMESTAMP           NOT NULL
);
"""

CREATE_TABLE_USERS = """
CREATE TABLE users (
user_id             INTEGER             NOT NULL,
first_name          TEXT                NOT NULL,
last_name           TEXT                NOT NULL,
gender              TEXT                NOT NULL,
level               TEXT                NOT NULL
);
"""

CREATE_TABLE_SONGS = """
CREATE TABLE songs (
song_id             TEXT                NOT NULL,
title               TEXT                NOT NULL,
year                INTEGER             NOT NULL,
duration            FLOAT               NOT NULL,
artist_id           TEXT                NOT NULL
);
"""

CREATE_TABLE_ARTISTS = """
CREATE TABLE artists (
artist_id           TEXT                NOT NULL,
name                TEXT                NOT NULL,
location            TEXT                NOT NULL,
latitude            DOUBLE PRECISION            ,
longitude           DOUBLE PRECISION
);
"""

CREATE_TABLE_TIME = """
CREATE TABLE time (
start_time          TIMESTAMP           NOT NULL,
hour                NUMERIC(2)          NOT NULL,
day                 NUMERIC(2)          NOT NULL,
week                NUMERIC(2)          NOT NULL,
month               NUMERIC(2)          NOT NULL,
year                INTEGER             NOT NULL,
weekday             TEXT                NOT NULL
);
"""

#
# STAGING TABLES

COPY_STAGING_EVENTS = f"""
COPY staging_events
FROM '{config.get('S3', 'LOG_DATA')}'
CREDENTIALS 'aws_iam_role={config.get('IAM', 'REDSHIFT_ROLE_ARN')}'
FORMAT AS JSON 'auto ignorecase'
TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
region '{config.get('AWS', 'REGION')}';
"""

COPY_STAGING_SONGS = f"""
COPY staging_songs
FROM '{config.get('S3', 'SONG_DATA')}'
CREDENTIALS 'aws_iam_role={config.get('IAM', 'REDSHIFT_ROLE_ARN')}'
FORMAT AS JSON 'auto ignorecase'
region '{config.get('AWS', 'REGION')}';
"""

# FINAL TABLES

INSERT_TABLE_SONGPLAYS = """
INSERT INTO songplays
(
SELECT
CONCAT(CAST (e.userid AS VARCHAR), CONCAT(CAST (e.sessionid AS VARCHAR), CAST (e.iteminsession AS VARCHAR))) as songplay_id,
e.level AS level,
e.location AS location,
e.useragent AS user_agent,
e.sessionid AS session_id,
CAST (e.userid AS INTEGER) AS user_id,
s.song_id AS song_id,
s.artist_id AS artist_id,
TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second' AS start_time
FROM staging_events AS e
JOIN staging_songs  AS s
ON e.song = s.title AND e.artist = s.artist_name
WHERE e.page = 'NextSong'
ORDER BY e.ts
);
"""

INSERT_TABLE_USERS = """
INSERT INTO users
(
SELECT
DISTINCT CAST (userid AS INTEGER) AS user_id,
firstname AS first_name,
lastname AS last_name,
TRIM (BOTH FROM gender) AS gender,
TRIM (BOTH FROM level) AS level
FROM staging_events
WHERE page = 'NextSong'
ORDER BY userId
);
"""

INSERT_TABLE_SONGS = """
INSERT INTO songs
(
SELECT
DISTINCT s.song_id AS song_id,
s.title AS title,
s.year AS year,
s.duration AS duration,
s.artist_id AS artist_id
FROM staging_events AS e
JOIN staging_songs  AS s
ON e.song = s.title AND e.artist = s.artist_name
WHERE e.page = 'NextSong'
ORDER BY s.song_id
);
"""

INSERT_TABLE_ARTISTS = """
INSERT INTO artists
(
SELECT
DISTINCT s.artist_id AS artist_id,
s.artist_name AS name,
s.artist_location AS location,
s.artist_latitude AS latitude,
s.artist_longitude AS longitude
FROM staging_events AS e
JOIN staging_songs AS s
ON e.song = s.title AND e.artist = s.artist_name
WHERE e.page = 'NextSong'
ORDER BY s.artist_id
);
"""

INSERT_TABLE_TIME = """
INSERT INTO time
(
SELECT
DISTINCT TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second' AS start_time,
DATE_PART(hour, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS hour,
DATE_PART(day, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS day,
DATE_PART(week, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS week,
DATE_PART(month, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS month,
DATE_PART(year, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS year,
DATE_PART(dayofweek, TIMESTAMP 'epoch' + e.ts::float / 1000 * INTERVAL '1 second') AS weekday
FROM staging_events AS e
JOIN staging_songs  AS s
ON e.song = s.title AND e.artist = s.artist_name
WHERE e.page = 'NextSong'
ORDER BY e.ts
);
"""

# QUERY LISTS

CREATE_TABLE_QUERIES = [CREATE_TABLE_STAGING_EVENTS, CREATE_TABLE_STAGING_SONGS,
                        CREATE_TABLE_SONGPLAYS, CREATE_TABLE_USERS,
                        CREATE_TABLE_SONGS, CREATE_TABLE_ARTISTS,
                        CREATE_TABLE_TIME]

DROP_TABLE_QUERIES = [DROP_TABLE_STAGING_EVENTS, DROP_TABLE_STAGING_SONGS,
                      DROP_TABLE_SONGPLAYS, DROP_TABLE_USERS, DROP_TABLE_SONGS,
                      DROP_TABLE_ARTISTS, DROP_TABLE_TIME]

COPY_TABLE_QUERIES = [COPY_STAGING_EVENTS, COPY_STAGING_SONGS]

INSERT_TABLE_QUERIES = [INSERT_TABLE_SONGPLAYS, INSERT_TABLE_USERS,
                        INSERT_TABLE_SONGS, INSERT_TABLE_ARTISTS,
                        INSERT_TABLE_TIME]
