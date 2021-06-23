
CREATE TABLE driver 
(
    first_name  VARCHAR(20),
    mid_name    VARCHAR(20),
    last_name   VARCHAR(20),
    user        VARCHAR(20),
    driver_id   INT,
    sponsor_id  INT,
    point       INT,
    address     VARCHAR(40),
    phone       INT,
    email       VARCHAR(20),
    pwd         VARCHAR(255),
    image       BLOB,
    date_join   DATE,
    date_leave  DATE
)