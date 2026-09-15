-- Logical schema for the analysis-ready SQLite model.

CREATE TABLE transactions (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    invoice_date TIMESTAMP NOT NULL,
    unit_price REAL NOT NULL CHECK (unit_price > 0),
    customer_id TEXT NOT NULL,
    country TEXT NOT NULL,
    revenue REAL NOT NULL,
    invoice_date_only DATE NOT NULL,
    invoice_month TEXT NOT NULL,
    invoice_month_start DATE NOT NULL
);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    first_purchase TIMESTAMP NOT NULL,
    last_purchase TIMESTAMP NOT NULL,
    total_orders INTEGER NOT NULL,
    total_items INTEGER NOT NULL,
    total_revenue REAL NOT NULL,
    country TEXT,
    average_order_value REAL NOT NULL,
    days_since_last_purchase INTEGER NOT NULL,
    customer_tenure_days INTEGER NOT NULL,
    is_repeat_customer INTEGER NOT NULL
);

CREATE TABLE rfm_segments (
    customer_id TEXT PRIMARY KEY,
    recency INTEGER NOT NULL,
    frequency INTEGER NOT NULL,
    monetary REAL NOT NULL,
    r_score INTEGER NOT NULL,
    f_score INTEGER NOT NULL,
    m_score INTEGER NOT NULL,
    rfm_score TEXT NOT NULL,
    segment TEXT NOT NULL
);

CREATE TABLE cohort_retention (
    cohort_month TEXT NOT NULL,
    cohort_index INTEGER NOT NULL,
    active_customers INTEGER NOT NULL,
    cohort_size INTEGER NOT NULL,
    retention_rate REAL NOT NULL,
    PRIMARY KEY (cohort_month, cohort_index)
);
