# MySQL Installation and Validation

## Environment
- OS: Ubuntu 26.04.1 LTS
- Database: MySQL Server
- Database name: cybersecurity_db
- Table: security_events
- Database user: sqoop_user

## Database Structure
The security_events table stores:
- Event timestamp
- Source IP
- Destination IP
- Event type
- Severity
- Description
- Source system

## Validation
- MySQL service: active
- Database created: cybersecurity_db
- Table created: security_events
- Sample records inserted: 8
- Sqoop user authentication: tested
- SELECT permissions: tested

## Dataset Note
The initial records are synthetic demonstration data.
They are not records from CIC-IDS2017.
