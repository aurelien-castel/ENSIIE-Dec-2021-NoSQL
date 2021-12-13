CREATE DATABASE cookiepost;
\c cookiepost;

CREATE TABLE IF NOT EXISTS cookiepost (
  id BIGSERIAL PRIMARY KEY,
  text text,
  date timestamp
);
