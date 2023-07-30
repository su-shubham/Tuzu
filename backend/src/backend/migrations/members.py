CREATE TABLE members(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    email TEXT NOT NULL,
    email_verified TIMESTAMP,
    password_hash TEXT NOT NULL
)

CREATE UNIQUE INDEX members_unique_email_idx on members(LOWER(email));

CERATE TABLE todos(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    complete BOOLEAN NOT NULL DEFAULT FALSE,
    due TIMESTAMPZ,
    member_id INT NOT NULL REFRENCES members(id),
    task TEXT NOT NULL  
)