# Live Project demo
http://127.0.0.1:8050

# install on terminal
pip install dash plotly pandas numpy
# Run
python student_dashboard_app.py

# Student_Dashboard
Project Description — Real-Time Interactive Student Performance Dashboard

This project is a real-time data-driven dashboard built using Python, Dash, Pandas, and Plotly Express to visualize and monitor student performance stored in a CSV file. The application reads student records dynamically and updates charts and tables every few seconds, allowing live performance tracking without restarting the app.

The dashboard provides interactive controls that enable users to filter results, change visualization styles, and customize the appearance of the interface. It supports multiple data-visualization formats to help users analyze student scores from different perspectives.

Key Features
✔ Real-Time CSV Data Loading

Student records are loaded from
student_scores.csv

The app refreshes automatically every 3 seconds

Missing timestamps are auto-generated

✔ Interactive Filters & Controls

Users can:

Select a subject

Filter students based on minimum score

Choose from multiple chart types

Customize heading font style and size

✔ Multiple Visualization Modes

The dashboard supports:

Bar Chart

Line Chart

Stacked Bar Chart

Pie Chart

Heat-Map

3D Visualization

Time-Series Trend Plot

Each visualization provides a different analytical perspective on student performance.

✔ Dynamic Data Table

Displays filtered student records

Auto-updates with every refresh

Shows clean, tabular student data

✔ Customizable UI

Includes:

Modern gradient theme

Card-based layout

Adjustable heading typography

Technical Workflow

Data is read from the CSV file using Pandas

Data is filtered based on:

Selected subject

Minimum score threshold

The selected chart type is generated using Plotly Express

A data table is created using Dash HTML components

A dcc.Interval component refreshes:

Graph

Table

Data state

# Screen Shots
<img width="1167" height="450" alt="newplot (1)" src="https://github.com/user-attachments/assets/ff21c2b6-0599-4256-9c19-3720bae3b729" />

<img width="1167" height="450" alt="newplot (7)" src="https://github.com/user-attachments/assets/4d240c2c-accf-4fc8-99ff-703acead856e" />

<img width="1167" height="450" alt="newplot (2)" src="https://github.com/user-attachments/assets/d31017d4-b409-4417-a32f-3de6c5840a2e" />

<img width="1167" height="450" alt="newplot (8)" src="https://github.com/user-attachments/assets/16753f62-6650-4d68-bec0-337ee7b7b3d6" />
<img width="1167" height="450" alt="newplot" src="https://github.com/user-attachments/assets/abd5af7e-53dd-44b5-88c5-7acd259aeb34" />

<img width="1167" height="450" alt="newplot (9)" src="https://github.com/user-attachments/assets/536c629e-da99-4808-8827-82d438d2401f" />




