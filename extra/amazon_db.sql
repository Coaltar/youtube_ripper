CREATE DATABASE amazon_test;
USE amazon_test;

CREATE TABLE loft_beds (
    asin VARCHAR(10) PRIMARY KEY,
    dim_length float,
    dim_width float,
    dim_height float,
    price float,
    weight float
);

-- CREATE TABLE img_thumbnails (
--     id INT PRIMARY KEY,
--     video_id int,
--     img BLOB
-- )


CREATE USER amazon_worker@localhost IDENTIFIED BY 'cheap';
GRANT ALL privileges ON amazon_test.* TO amazon_worker@localhost;