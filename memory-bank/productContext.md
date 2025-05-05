# Product Context: Volume Reporting System

## Purpose
The system exists to automate and standardize the process of gathering volume data from multiple client databases. It solves the problem of manually querying each database and consolidating the results.

## User Experience
- Users can run a single command to generate reports for all clients
- Reports are consistently formatted and easy to read
- Excel output provides a familiar interface for data analysis
- Date-based file naming prevents confusion with multiple runs

## How It Works
1. Reads connection details from a JSON configuration file
2. Connects to each client's SQL Server database
3. Executes a standardized volume query
4. Generates individual CSV files for each client
5. Combines all data into a single Excel file with auto-sized columns
6. Uses date-based file naming (YYYYMMDD format)

## Key Features
- Automated multi-database querying
- Standardized report format
- Consolidated Excel output
- Error handling and logging
- Date-based file management

## User Workflows
- To be defined based on project needs

## Integration Points
- To be defined based on project needs 