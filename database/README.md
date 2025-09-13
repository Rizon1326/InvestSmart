# Database Setup Instructions

This directory contains the database schema and setup files for the Business Analysis Platform.

## Prerequisites

1. PostgreSQL 12+ installed
2. Database administration privileges

## Setup Steps

### 1. Create Database and User

```sql
-- Connect as postgres superuser
sudo -u postgres psql

-- Create database
CREATE DATABASE market_analysis;

-- Create user (optional, for security)
CREATE USER market_analysis_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE market_analysis TO market_analysis_user;
```

### 2. Run Schema Setup

```bash
# Run the schema creation script
psql -U postgres -d market_analysis -f schema.sql

# Or if using custom user:
psql -U market_analysis_user -d market_analysis -f schema.sql
```

### 3. Update Application Configuration

Update the `application.properties` file in the backend:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/market_analysis
spring.datasource.username=market_analysis_user
spring.datasource.password=your_secure_password
```

## Database Structure

### Core Tables

- **user_inputs**: Stores user form submissions
- **analysis_results**: Stores analysis outcomes
- **market_data**: Scraped market data
- **forecast_data**: ML prediction results
- **financial_scenarios**: Financial projections

### Reference Tables

- **bd_districts**: Bangladesh districts list
- **business_categories**: Business category definitions

### Views

- **analysis_summary**: Comprehensive analysis overview

## Sample Data

The schema includes sample data for:
- Bangladesh districts (64 districts)
- Business categories with cost ranges
- Basic lookup data

## Maintenance

### Backup Database

```bash
pg_dump -U postgres market_analysis > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
psql -U postgres market_analysis < backup_file.sql
```

### Performance Monitoring

Monitor these indexes for query performance:
- Location-based queries
- Date range queries
- Analysis result lookups

## Security Considerations

1. Use strong passwords
2. Limit network access to database
3. Regular backups
4. Monitor query performance
5. Update PostgreSQL regularly