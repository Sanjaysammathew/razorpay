-- Run with: psql -U postgres -f sql/setup.sql
CREATE DATABASE payment_db;
\connect payment_db

-- Equivalent to the tables created automatically by app/main.py.
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    razorpay_order_id VARCHAR(100) NOT NULL UNIQUE,
    amount INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'INR',
    status VARCHAR(30) NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO products (name, description, price)
VALUES
    ('Coffee Mug', 'Ceramic mug for payment flow practice', 249.00),
    ('Notebook', 'A5 ruled notebook', 149.50),
    ('Desk Lamp', 'LED desk lamp', 1299.00);
