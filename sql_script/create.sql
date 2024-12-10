-- Create COMPANY_INFO table
CREATE TABLE COMPANY_INFO (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    company_market_id CHAR(50) NOT NULL
);

-- Create COMPANY_FUNDAMENTAL_ANALYSIS table
CREATE TABLE COMPANY_FUNDAMENTAL_ANALYSIS (
    company_fa_id SERIAL PRIMARY KEY,
    stock_period CHAR(50) NOT NULL,
    stock_profit BIGINT,
    stock_loss BIGINT,
    stock_cashin BIGINT,
    stock_cashout BIGINT,
    stock_debt BIGINT,
    stock_expenditure BIGINT,
    company_id INT NOT NULL,
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES COMPANY_INFO(company_id)
);

-- Create STOCK_DATA table
CREATE TABLE STOCK_DATA (
    stock_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    stock_date DATE NOT NULL,
    open_price BIGINT,
    close_price BIGINT,
    high BIGINT,
    low BIGINT,
    adj_close BIGINT,
    volume BIGINT,
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES COMPANY_INFO(company_id)
);
