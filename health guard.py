import serial
import time
import mysql.connector
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set the serial port and baud rate
ser = serial.Serial('COM3', 9600)  

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Muthuchitra@04',
    'database': 'health'
}

# Lists to store heart rate and temperature data for plotting
heart_rate_data = []
temperature_data = []

pulse_value = None
temperature_value = None

# Function to parse the serial data and insert into MySQL table
# Function to parse the serial data and insert into MySQL table
def parse_serial(data):
    global pulse_value, temperature_value
    try:
        data_str = data.decode('utf-8').strip()
        if data_str.startswith("Pulse Value:"):
            try:
                pulse_value = int(data_str.split(":")[1])
                # Append pulse value to the list
                heart_rate_data.append(pulse_value)
                if len(heart_rate_data) > 10:
                    heart_rate_data.pop(0)  # Keep only the last 10 values
            except ValueError:
                print("Invalid pulse value received:", data_str)
        elif data_str.startswith("Temperature:"):
            try:
                temperature_value = float(data_str.split(":")[1].split(" ")[1])
                # Append temperature value to the list
                temperature_data.append(temperature_value)
                if len(temperature_data) > 10:
                    temperature_data.pop(0)  # Keep only the last 10 values
            except (ValueError, IndexError):
                print("Invalid temperature value received:", data_str)
               
        # Check if both pulse_value and temperature_value are not None
        if pulse_value is not None and temperature_value is not None:
            # Insert both values into MySQL table
            insert_data_into_mysql(pulse_value, temperature_value)
            # Reset pulse_value and temperature_value to None for next data
            pulse_value = None
            temperature_value = None
               
    except UnicodeDecodeError:
        print("Error decoding data:", data)

# Function to insert data into MySQL table
def insert_data_into_mysql(pulse_value, temperature_value):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO health_data (heart_rate, temperature) VALUES (%s, %s)"
        cursor.execute(query, (pulse_value, temperature_value))
        connection.commit()
        print("Data inserted into MySQL table successfully.")
    except mysql.connector.Error as error:
        print("Error inserting data into MySQL:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle "Show report" button click event
def show_report():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT * FROM health_data ORDER BY id DESC LIMIT 10"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Create a new Tkinter window for displaying the report
        report_window = tk.Toplevel()
        report_window.title("Health Data Report")

        # Create a table to display the fetched data
        table = tk.Label(report_window, text="Health Data Report")
        table.grid(row=0, column=0, columnspan=2)

        # Add column headers
        tk.Label(report_window, text="ID").grid(row=1, column=0)
        tk.Label(report_window, text="Timestamp").grid(row=1, column=1)
        tk.Label(report_window, text="Heart Rate").grid(row=1, column=2)
        tk.Label(report_window, text="Temperature").grid(row=1, column=3)

        # Display fetched data in table format
        for i, row in enumerate(rows, start=2):
            for j, value in enumerate(row):
                tk.Label(report_window, text=value).grid(row=i, column=j)

    except mysql.connector.Error as error:
        print("Error fetching data from MySQL:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle "Dashboard" button click event
def show_dashboard():
    # Create a new Tkinter window for the dashboard
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Dashboard")

    # Create a figure and axis for the line chart
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Plot heart rate data
    ax.plot(range(1, len(heart_rate_data) + 1), heart_rate_data, label='Heart Rate')

    # Plot temperature data
    ax.plot(range(1, len(temperature_data) + 1), temperature_data, label='Temperature')

    # Set labels and legend
    ax.set_xlabel('Data Points')
    ax.set_ylabel('Values')
    ax.set_title('Health Data')
    ax.legend()

    # Create a canvas to display the line chart
    canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a Tkinter window
window = tk.Tk()
window.title("Health Monitor")

# Create buttons for "Show report" and "Dashboard"
report_button = tk.Button(window, text="Show report", command=show_report)
report_button.pack(pady=10)

dashboard_button = tk.Button(window, text="Dashboard", command=show_dashboard)
dashboard_button.pack(pady=10)

try:
    while True:
        # Read serial data
        if ser.in_waiting > 0:
            data = ser.readline()
            parse_serial(data)
            window.update_idletasks()  # Update Tkinter window to handle button clicks
            window.update()
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")

window.mainloop()  # Start the Tkinter event loop

