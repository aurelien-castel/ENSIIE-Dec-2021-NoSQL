SELECT 'CREATE DATABASE cookiepost'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cookiepost')\gexec
\c cookiepost;

CREATE TABLE IF NOT EXISTS cookiepost (
  id BIGSERIAL PRIMARY KEY,
  text text,
  date timestamp
);
