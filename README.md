# Digital Twin Platform Explanation
This project is creating a Digital Twin system - a virtual representation of industrial machines. Let me break it down:

What is it?
A system that monitors industrial machines in real-time
Collects data like temperature, pressure, vibration, and power usage
Predicts when machines might need maintenance
Project Components
1. Data Structure (ProcessState)
2. Digital Twin Core (DigitalTwin)
Stores historical data for each machine
Uses machine learning (IsolationForest) to detect abnormal behavior
Predicts when maintenance might be needed
3. API Endpoints
/update_state: Send new machine readings
/maintenance/{machine_id}: Check if machine needs maintenance
/machine/{machine_id}/history: View machine's historical data
