# Active Context

## Current Focus
- Volume reporting system with two main functionalities:
  1. Detailed monthly reports (generate command)
  2. Quick prior month summary (summary command)

## Recent Changes
1. Added new `summary` command
   - Shows prior month's volume data
   - Displays in markdown format
   - Includes client and database information in titles
   - Uses dedicated SQL query for prior month data

2. Enhanced output formatting
   - Added database server/name to summary titles
   - Improved markdown table presentation
   - Better error handling and empty data detection

## Next Steps
- Consider adding more summary views (e.g., current month, YTD)
- Explore adding more data points to summary view
- Consider adding export options for summary data
- Evaluate performance optimizations for large datasets

## Active Decisions
- Using markdown format for console output
- Separating detailed and summary queries
- Including database connection details in output
- Maintaining backward compatibility with existing reports 