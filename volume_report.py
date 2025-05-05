import json
import os
from pathlib import Path
from typing import List, Dict
import pyodbc
import pandas as pd
import typer
from datetime import datetime
from openpyxl.utils import get_column_letter
from sqlalchemy import create_engine, URL

app = typer.Typer()

volume_app = typer.Typer()
app.add_typer(volume_app, name="volume", help="Volume reporting commands")

def load_database_connections(connections_file: str) -> tuple[str, List[Dict]]:
    """Load database connection details from JSON file."""
    with open(connections_file, 'r') as f:
        data = json.load(f)
    return data['sql_driver'], data['definitions']

def execute_query(connection_details: Dict, query_file: str, sql_driver: str) -> pd.DataFrame:
    """Execute SQL query against a database and return results as DataFrame."""
    # Read the SQL query
    with open(query_file, 'r') as f:
        query = f.read()
    
    # Create SQLAlchemy connection URL
    connection_url = URL.create(
        "mssql+pyodbc",
        username=connection_details['uid'],
        password=connection_details['pwd'],
        host=connection_details['server'],
        database=connection_details['database'],
        query={"driver": sql_driver}
    )
    
    # Create engine and execute query
    engine = create_engine(connection_url)
    return pd.read_sql(query, engine)

def write_to_csv(df: pd.DataFrame, client_name: str, output_dir: str) -> str:
    """Write DataFrame to CSV file with client name in filename."""
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{client_name}_volume_report_{date_str}.csv"
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    return output_path

def auto_size_columns(worksheet):
    """Auto-size columns in the Excel worksheet."""
    for column in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        
        # Find the maximum length of content in the column
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        
        # Add some padding to the max length
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column_letter].width = adjusted_width

def combine_csvs_to_excel(csv_files: List[str], output_dir: str) -> str:
    """Combine multiple CSV files into a single Excel file with multiple sheets."""
    date_str = datetime.now().strftime("%Y%m%d")
    excel_path = os.path.join(output_dir, f"combined_volume_reports_{date_str}.xlsx")
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for csv_file in csv_files:
            # Get the client name from the filename
            client_name = os.path.basename(csv_file).split('_')[0]
            # Read the CSV file
            df = pd.read_csv(csv_file)
            # Write to Excel sheet
            df.to_excel(writer, sheet_name=client_name, index=False)
            
            # Get the worksheet and auto-size columns
            worksheet = writer.sheets[client_name]
            auto_size_columns(worksheet)
    
    return excel_path

@app.command(name="generate")
def generate_reports(
    connections_file: str = typer.Option(
        "database_connections.json",
        help="Path to database connections JSON file"
    ),
    query_file: str = typer.Option(
        "query_volume_totals_by_month.sql",
        help="Path to SQL query file"
    ),
    output_dir: str = typer.Option(
        "reports",
        help="Directory to save CSV reports"
    )
):
    """Generate volume reports for all databases defined in connections file."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load database connections and SQL driver
    sql_driver, connections = load_database_connections(connections_file)
    
    # List to store paths of generated CSV files
    csv_files = []
    
    # Process each database
    for conn in connections:
        try:
            typer.echo(f"Processing {conn['client']} database...")
            df = execute_query(conn, query_file, sql_driver)
            output_path = write_to_csv(df, conn['client'], output_dir)
            csv_files.append(output_path)
            typer.echo(f"Report generated: {output_path}")
        except Exception as e:
            typer.echo(f"Error processing {conn['client']}: {str(e)}", err=True)
    
    # Combine all CSV files into a single Excel file
    if csv_files:
        try:
            excel_path = combine_csvs_to_excel(csv_files, output_dir)
            typer.echo(f"\nCombined all reports into Excel file: {excel_path}")
        except Exception as e:
            typer.echo(f"Error combining reports into Excel: {str(e)}", err=True)

if __name__ == "__main__":
    app() 