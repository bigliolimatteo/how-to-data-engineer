\connect postgres

DROP TABLE IF EXISTS raw_data;
CREATE TABLE raw_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    user_id VARCHAR NOT NULL,
    is_logged BOOLEAN NOT NULL,
    device_type VARCHAR NOT NULL,
    page_type VARCHAR NOT NULL
);
