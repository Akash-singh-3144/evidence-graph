DROP TABLE IF EXISTS quarterly_revenue;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS customers;

CREATE TABLE quarterly_revenue (
    id SERIAL PRIMARY KEY,
    quarter VARCHAR(10),
    revenue_millions DECIMAL,
    notes TEXT
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount DECIMAL,
    date DATE,
    status VARCHAR(20)
);

INSERT INTO quarterly_revenue (quarter, revenue_millions, notes) VALUES
('2023-Q1', 450.5, 'Strong start to the year'),
('2023-Q2', 480.0, 'Continued growth'),
('2023-Q3', 495.2, 'Record breaking quarter'),
('2023-Q4', 510.0, 'Holiday surge'),
('2024-Q1', 460.0, 'Post-holiday stabilization'),
('2024-Q2', 368.0, 'Sudden drop in revenue due to supply chain shortages in SE Asia');

INSERT INTO customers (name, region) VALUES
('Acme Corp', 'North America'),
('Globex Inc', 'Europe'),
('Soylent LLC', 'Asia');

INSERT INTO sales (customer_id, amount, date, status) VALUES
(1, 15000, '2024-04-10', 'completed'),
(2, 22000, '2024-05-15', 'completed'),
(3, 5000, '2024-06-20', 'cancelled_supply_issue');
