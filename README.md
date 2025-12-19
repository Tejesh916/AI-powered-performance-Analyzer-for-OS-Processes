# **Process Monitor & Performance Analyzer**  
This project provides **real-time process monitoring, risk assessment, and performance optimization** using machine learning techniques. It logs system resource usage, detects potential bottlenecks, and generates interactive reports to help analyze CPU and memory consumption trends.  

---

## **📌 Features**  
✅ **Real-time process monitoring**: Tracks active processes and logs CPU & memory usage every few seconds.  
✅ **Machine learning-based risk analysis**: Uses a RandomForest model to classify process status as `NORMAL`, `WARNING`, or `CRITICAL`.  
✅ **Automated reports**: Generates text-based and graphical performance reports for easy analysis.  
✅ **Interactive CPU & Memory usage charts**: View real-time trends through a web-based visualization.  
✅ **Optimization recommendations**: Suggests possible performance optimizations based on critical processes.  

---

## **🚀 Setup & Installation**  

### **1️⃣ Install Dependencies**  
Before running the scripts, ensure you have Python installed. Then, install the required libraries:  

```sh
pip install pandas scikit-learn plotly
```

### **2️⃣ Running the Monitoring Script**
Execute the real-time process monitoring script:
```sh
python monitor.py
```

### **3️⃣ View Reports & Analysis**
Performance Summary: Open performance_report.txt to review identified bottlenecks.

Interactive Chart: Open cpu_usage.html in a web browser to analyze CPU & memory trends visually.

Raw Logs: View process_logs.csv for detailed process usage data.

---

## **📊 How It Works**
Process Monitoring (PowerShell Script)
Collects process details (Process Name, CPU Usage, Memory Usage).
Logs data in process_logs.csv every few seconds.
Classifies processes as NORMAL, WARNING, or CRITICAL.
Data Analysis (Python Script)
Reads process_logs.csv and processes the data.
Trains a RandomForestClassifier to predict process risk levels.
Generates performance reports (performance_report.txt and cpu_usage.html).
Provides optimization recommendations for critical processes.

---

## **📂 File Structure**
```sh
📁 Process-Monitor-Analyzer/
│── monitor.py                  # Python script for analysis & visualization  
│── monitor_processes.ps1       # PowerShell script for real-time process monitoring  
│── process_logs.csv            # Log file storing CPU & Memory usage (auto-generated)  
│── performance_report.txt      # Text-based performance analysis report (auto-generated)  
│── cpu_usage.html              # Interactive CPU & Memory graph (auto-generated)  
│── optimization_rules.json     # JSON file storing optimization recommendations  
│── README.md                   # Project documentation
```

---

## **📌 Example Output**
```sh
Performance Report (performance_report.txt)
=== Performance Report ===
Generated: 2025-03-28 14:30:15

Critical Processes:
ProcessName    CPU   Memory
chrome.exe     32.5   750.2
python.exe     45.3   620.1

Recommendations:
chrome.exe: Reduce tab usage, Enable hardware acceleration, Disable unnecessary extensions
python.exe: Optimize script logic, Reduce memory-intensive operations, Use multiprocessing
```

---

### **Graphical Report (`cpu_usage.html`)**  

✅ **Real-time visualization** of CPU & Memory usage trends over time.  
✅ **Interactive filters** allow focusing on specific processes for detailed analysis.  
✅ **Helps identify and diagnose** potential performance bottlenecks efficiently.  

---

## **📢 Contributing**
Feel free to contribute by improving the scripts, adding new monitoring metrics, or refining the ML model. Fork the repo, make changes, and submit a pull request!

---

## **📧 Contact**
For any questions or suggestions, reach out at [tejeshmaddala916@gmail.com].
