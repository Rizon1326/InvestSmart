-- PostgreSQL Database Schema for Business Analysis Platform
-- Run this script to create the database structure

-- Create database (run this manually as superuser)
-- CREATE DATABASE market_analysis;

-- Create user_inputs table
CREATE TABLE IF NOT EXISTS user_inputs (
    id BIGSERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    business_interest VARCHAR(100) NOT NULL,
    capital_min DECIMAL(15,2) NOT NULL CHECK (capital_min >= 0),
    capital_max DECIMAL(15,2) NOT NULL CHECK (capital_max >= capital_min),
    risk_profile VARCHAR(50) NOT NULL CHECK (risk_profile IN ('conservative', 'balanced', 'aggressive')),
    target_income DECIMAL(15,2) NOT NULL CHECK (target_income >= 0),
    income_period VARCHAR(20) NOT NULL CHECK (income_period IN ('monthly', 'yearly')),
    work_type VARCHAR(20) NOT NULL CHECK (work_type IN ('full-time', 'part-time')),
    selling_channel VARCHAR(20) NOT NULL CHECK (selling_channel IN ('online', 'offline', 'both')),
    seasonal_preference VARCHAR(200),
    delivery_capability VARCHAR(30) NOT NULL CHECK (delivery_capability IN ('own', 'third-party', 'both')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create analysis_results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id BIGSERIAL PRIMARY KEY,
    user_input_id BIGINT NOT NULL REFERENCES user_inputs(id) ON DELETE CASCADE,
    fit_score DECIMAL(4,2) CHECK (fit_score >= 0 AND fit_score <= 10),
    suggested_price DECIMAL(15,2) CHECK (suggested_price >= 0),
    expected_revenue DECIMAL(15,2) CHECK (expected_revenue >= 0),
    net_profit DECIMAL(15,2),
    roi_percentage DECIMAL(8,2),
    payback_period_months INTEGER CHECK (payback_period_months >= 0),
    demand_forecast TEXT, -- JSON string
    recommendations TEXT, -- JSON string
    ai_analysis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create market_data table for storing scraped data
CREATE TABLE IF NOT EXISTS market_data (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL, -- 'foodpanda', 'daraz', etc.
    location VARCHAR(100) NOT NULL,
    business_type VARCHAR(100) NOT NULL,
    product_name VARCHAR(200),
    price DECIMAL(15,2),
    demand_score DECIMAL(4,2),
    competition_level VARCHAR(20),
    seasonal_trend VARCHAR(20),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create forecast_data table for storing ML predictions
CREATE TABLE IF NOT EXISTS forecast_data (
    id BIGSERIAL PRIMARY KEY,
    analysis_result_id BIGINT NOT NULL REFERENCES analysis_results(id) ON DELETE CASCADE,
    model_type VARCHAR(50) NOT NULL, -- 'prophet', 'sarimax', 'xgboost', 'lightgbm'
    forecast_month INTEGER NOT NULL,
    predicted_demand DECIMAL(15,2),
    confidence_lower DECIMAL(15,2),
    confidence_upper DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create financial_scenarios table for storing Monte Carlo results
CREATE TABLE IF NOT EXISTS financial_scenarios (
    id BIGSERIAL PRIMARY KEY,
    analysis_result_id BIGINT NOT NULL REFERENCES analysis_results(id) ON DELETE CASCADE,
    scenario_type VARCHAR(20) NOT NULL, -- 'best', 'expected', 'worst', 'monte_carlo'
    monthly_revenue DECIMAL(15,2),
    monthly_profit DECIMAL(15,2),
    annual_profit DECIMAL(15,2),
    roi_percentage DECIMAL(8,2),
    payback_period_months INTEGER,
    probability DECIMAL(5,4), -- For Monte Carlo scenarios
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_inputs_location ON user_inputs(location);
CREATE INDEX IF NOT EXISTS idx_user_inputs_business ON user_inputs(business_interest);
CREATE INDEX IF NOT EXISTS idx_user_inputs_created ON user_inputs(created_at);

CREATE INDEX IF NOT EXISTS idx_analysis_results_user_input ON analysis_results(user_input_id);
CREATE INDEX IF NOT EXISTS idx_analysis_results_created ON analysis_results(created_at);

CREATE INDEX IF NOT EXISTS idx_market_data_location_business ON market_data(location, business_type);
CREATE INDEX IF NOT EXISTS idx_market_data_source ON market_data(source);
CREATE INDEX IF NOT EXISTS idx_market_data_scraped ON market_data(scraped_at);

CREATE INDEX IF NOT EXISTS idx_forecast_data_analysis ON forecast_data(analysis_result_id);
CREATE INDEX IF NOT EXISTS idx_forecast_data_model ON forecast_data(model_type);

CREATE INDEX IF NOT EXISTS idx_financial_scenarios_analysis ON financial_scenarios(analysis_result_id);
CREATE INDEX IF NOT EXISTS idx_financial_scenarios_type ON financial_scenarios(scenario_type);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to user_inputs table
CREATE TRIGGER update_user_inputs_updated_at 
    BEFORE UPDATE ON user_inputs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample districts for Bangladesh
CREATE TABLE IF NOT EXISTS bd_districts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    division VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO bd_districts (name, division) VALUES
('Dhaka', 'Dhaka'),
('Chittagong', 'Chittagong'),
('Sylhet', 'Sylhet'),
('Rajshahi', 'Rajshahi'),
('Khulna', 'Khulna'),
('Barishal', 'Barishal'),
('Rangpur', 'Rangpur'),
('Mymensingh', 'Mymensingh'),
('Comilla', 'Chittagong'),
('Gazipur', 'Dhaka'),
('Narayanganj', 'Dhaka'),
('Cox''s Bazar', 'Chittagong'),
('Jessore', 'Khulna'),
('Bogura', 'Rajshahi'),
('Dinajpur', 'Rangpur')
ON CONFLICT (name) DO NOTHING;

-- Insert sample business categories
CREATE TABLE IF NOT EXISTS business_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    avg_startup_cost_min DECIMAL(15,2),
    avg_startup_cost_max DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO business_categories (name, description, avg_startup_cost_min, avg_startup_cost_max) VALUES
('Food & Restaurant', 'Food service and restaurant businesses', 50000, 500000),
('Retail & Fashion', 'Clothing, accessories, and retail shops', 30000, 300000),
('Electronics', 'Electronics sales and repair services', 100000, 800000),
('Beauty & Personal Care', 'Beauty salons, cosmetics, personal care', 25000, 200000),
('Agriculture', 'Farming, livestock, agricultural products', 20000, 150000),
('E-commerce', 'Online business and digital services', 10000, 100000),
('Services', 'Professional and personal services', 15000, 150000),
('Healthcare', 'Medical services and health products', 100000, 1000000)
ON CONFLICT (name) DO NOTHING;

-- Create view for comprehensive analysis results
CREATE OR REPLACE VIEW analysis_summary AS
SELECT 
    ar.id,
    ar.user_input_id,
    ui.location,
    ui.business_interest,
    ui.capital_min,
    ui.capital_max,
    ui.risk_profile,
    ui.target_income,
    ar.fit_score,
    ar.suggested_price,
    ar.expected_revenue,
    ar.net_profit,
    ar.roi_percentage,
    ar.payback_period_months,
    ar.created_at
FROM analysis_results ar
JOIN user_inputs ui ON ar.user_input_id = ui.id;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO market_analysis_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO market_analysis_user;