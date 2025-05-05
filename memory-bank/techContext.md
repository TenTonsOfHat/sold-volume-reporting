# Technical Context

## Technologies Used
- Python 3.x
- SQL Server
- Required Python Packages:
  - typer (CLI interface)
  - pandas (data manipulation)
  - pyodbc (database connectivity)
  - sqlalchemy (database engine)
  - openpyxl (Excel file handling)
  - tabulate (markdown table formatting)

## Development Setup
- SQL Server connection via pyodbc
- JSON configuration for database connections
- SQL query files for data extraction
- Command-line interface with two main commands:
  1. `generate` - Full report generation
  2. `summary` - Quick prior month summary

## Technical Constraints
- Requires SQL Server access
- Database connections must be configured in JSON
- SQL queries must be compatible with SQL Server syntax
- Output directory must be writable

## Dependencies
- SQL Server ODBC driver
- Python packages listed in requirements.txt
- Access to configured databases 