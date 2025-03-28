import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import json
from datetime import datetime
import sys
import logging  # Add logging module

# Configure logging
logging.basicConfig(filename='process_monitor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started successfully.")

def main():
    try:
        # Force UTF-8 encoding
        sys.stdout.reconfigure(encoding='utf-8')
        
        logging.info("Loading data...")
        data = pd.read_csv('process_logs.csv').fillna(0)
        
        with open('optimization_rules.json', encoding='utf-8') as f:
            optimizations = json.load(f)

        logging.info("Analyzing bottlenecks...")
        X = data[['CPU', 'Memory']]
        y = data['Status'].map({'NORMAL': 0, 'WARNING': 1, 'CRITICAL': 2}).fillna(0)
        
        model = RandomForestClassifier()
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
        fig = px.line(data, x='Timestamp', y='CPU', 
                     color='ProcessName', title='CPU Usage')
        fig.write_html('cpu_usage.html')

        logging.info("Success! Reports generated.")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
