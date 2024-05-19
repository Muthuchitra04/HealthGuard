HealthGuard: A Next-Gen Solution for Remote Patient Monitoring and Emergency Alerting

Abstract:
HealthGuard addresses challenges in remote healthcare by integrating sensor technology, NodeMCU microcontroller, Python analytics, and Power BI visualization to monitor crucial patient parameters—pulse rate and body temperature. The system provides real-time data processing, dynamic reporting, and automated alerting for timely intervention, enhancing patient safety and well-being.

Key Features:
Real-Time Monitoring: Continuous surveillance of pulse rate and body temperature.
Dynamic Reporting: Real-time data processing and visualization using Python and Power BI.
Automated Alerting: Trigger phone calls and SMS notifications to healthcare providers in case of abnormal readings.


Technologies Used:
NodeMCU Microcontroller
Sensors: Pulse rate and body temperature sensors
Python: Data processing and analytics
Power BI: Data visualization and dashboard creation


Prerequisites:
NodeMCU: Set up the microcontroller and sensors.
Python: Install necessary libraries (pandas, matplotlib, etc.).
Power BI Desktop:


Steps:
Clone the repository

Set up the NodeMCU:
Connect the sensors to the NodeMCU.
Upload the provided firmware to the NodeMCU.

1.Run the Python script:
2.Install required Python libraries:
3.pip install -r requirements.txt
4.Execute the data processing script:
5.python data_processing.py

Power BI:
Open the Power BI file (HealthGuard_Dashboard.pbix).
Ensure the data source is correctly linked.

Usage
Monitoring: View real-time patient data on the Power BI dashboard.
Alerts: Automated alerts are triggered for abnormal parameter values.

Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
