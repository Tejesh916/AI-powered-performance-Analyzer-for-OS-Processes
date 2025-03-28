import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import json
from datetime import datetime
import sys
import logging
import os  # To check file existence

# Configure logging
logging.basicConfig(filename='process_monitor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started successfully.")

def main():
    try:
        # Force UTF-8 encoding
        sys.stdout.reconfigure(encoding='utf-8')
        
        # Check if required files exist
        if not os.path.exists('process_logs.csv'):
            logging.error("Missing file: process_logs.csv")
            print("Error: process_logs.csv not found.")
            return

        if not os.path.exists('optimization_rules.json'):
            logging.error("Missing file: optimization_rules.json")
            print("Error: optimization_rules.json not found.")
            return

        logging.info("Loading data...")
        data = pd.read_csv('process_logs.csv').fillna(0)

        # Ensure required columns exist
        required_columns = {'ProcessName', 'CPU', 'Memory', 'Status', 'Timestamp'}
        if not required_columns.issubset(data.columns):
            logging.error("Missing required columns in process_logs.csv")
            print(f"Error: Required columns missing: {required_columns - set(data.columns)}")
            return

        # Ensure timestamp column is properly formatted
        try:
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        except Exception as e:
            logging.error(f"Invalid timestamp format: {str(e)}")
            print("Error: Invalid timestamp format in process_logs.csv")
            return

        # Load optimizations
        with open('optimization_rules.json', encoding='utf-8') as f:
            optimizations = json.load(f)

        logging.info("Analyzing bottlenecks...")
        X = data[['CPU', 'Memory']]
        y = data['Status'].map({'NORMAL': 0, 'WARNING': 1, 'CRITICAL': 2}).fillna(0)
        
        # Ensure that there are enough samples for training
        if len(y.unique()) < 2:
            logging.error("Not enough data variation for model training.")
            print("Error: Not enough data for model training.")
            return

        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X, y)
        data['Risk'] = model.predict(X)

        logging.info("Generating reports...")
        # Text report with explicit UTF-8 encoding
        with open('performance_report.txt', 'w', encoding='utf-8') as f:
            f.write("=== Performance Report ===\n")
            f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
            
            critical = data[data['Risk'] == 2]
            if not critical.empty:
                f.write("Critical Processes:\n")
                f.write(critical[['ProcessName', 'CPU', 'Memory']].to_string(index=False))
                
                f.write("\n\nRecommendations:\n")
                for proc in critical['ProcessName'].unique():
                    if proc in optimizations:
                        f.write(f"{proc}: {', '.join(optimizations[proc][:3])}\n")
            else:
                f.write("No critical processes found\n")

        # Visual report
        fig = px.line(data, x='Timestamp', y=['CPU', 'Memory'], 
                      color='ProcessName', title='CPU & Memory Usage')

        # Check if data has valid timestamps
        if data['Timestamp'].isnull().all():
            logging.error("All timestamps are null, skipping plot.")
            print("Error: No valid timestamps for plotting.")
            return

        fig.write_html('cpu_usage.html')

        logging.info("Success! Reports generated.")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
