
CREATE TABLE sponsor 
(
    title       VARCHAR(20),
    USER        VARCHAR(20),
    sponsor_id  INT,
    address     VARCHAR(40),
    phone       INT,
    email       VARCHAR(20),
    pwd_hash    VARCHAR(255),
    image       BLOB,
    date_join   DATE,
    date_leave  DATE
)