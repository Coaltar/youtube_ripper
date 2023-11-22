CREATE DATABASE youtube_test;
USE youtube_test;

CREATE TABLE video_profile_overview (
    id VARCHAR(40) PRIMARY KEY,
    title VARCHAR(255),
    url VARCHAR(255),
    -- thumbnail_id UUID,
    views VARCHAR(255),
    age VARCHAR(255),
    length VARCHAR(255)
);

-- CREATE TABLE img_thumbnails (
--     id INT PRIMARY KEY,
--     video_id int,
--     img BLOB
-- )