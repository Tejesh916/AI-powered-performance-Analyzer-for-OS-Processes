# process_monitor.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import json
from datetime import datetime
import sys

def analyze_process_logs():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        print("Loading data...")
        
        data = pd.read_csv('process_logs.csv').fillna(0)
        
        with open('optimization_rules.json', encoding='utf-8') as f:
            optimizations = json.load(f)
        
        print("Analyzing bottlenecks...")
        X = data[['CPU', 'Memory']]
        y = data['Status'].map({'NORMAL': 0, 'WARNING': 1, 'CRITICAL': 2}).fillna(0)
        
        model = RandomForestClassifier()
        model.fit(X, y)
        data['Risk'] = model.predict(X)
        
        print("Generating reports...")
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
        
        fig = px.line(data, x='Timestamp', y='CPU', color='ProcessName', title='CPU Usage')
        fig.write_html('cpu_usage.html')
        
        print("Success! Reports generated.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    analyze_process_logs()

# PowerShell script for real-time process monitoring
powershell_script = '''
while($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $processes = Get-Process | Select-Object -First 10 | ForEach-Object {
        try {
            $cpu = [math]::Round($_.CPU, 1)
            $memory = [math]::Round($_.WorkingSet / 1MB, 2)
            $status = if ($cpu -gt 15 -or $memory -gt 500) { "CRITICAL" } 
                      elseif ($cpu -gt 5) { "WARNING" } 
                      else { "NORMAL" }
            
            [PSCustomObject]@{
                Timestamp = $timestamp
                ProcessName = $_.ProcessName
                PID = $_.Id
                CPU = $cpu
                Memory = $memory
                Status = $status
            }
        } catch { continue }
    }
    
    $processes | Format-Table -AutoSize
    if (!(Test-Path "process_logs.csv") -or (Get-Content "process_logs.csv" -Tail 1 | Select-String -NotMatch $timestamp)) {
    $processes | Export-Csv -Path "process_logs.csv" -Append -NoTypeInformation -Force
    }
    Start-Sleep -Seconds 3
}
'''

# Save the PowerShell script to a file
with open("monitor_processes.ps1", "w", encoding="utf-8") as f:
    f.write(powershell_script)

print("PowerShell script 'monitor_processes.ps1' created. Run it in PowerShell to start monitoring processes.")
