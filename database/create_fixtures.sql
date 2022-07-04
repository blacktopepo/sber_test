CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    external_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE notes
(
    id SERIAL PRIMARY KEY,
    region_id INTEGER,
    year INTEGER NOT NULL,
    value INTEGER NOT NULL
    FOREIGN KEY (region_id) REFERENCES regions (id)
);