import csv
import threading
import time
from datetime import datetime

# Global variable
global_variable = 0

# Function to update the global variable every second
def update_global_variable():
    global global_variable
    while True:
        # Update global variable (replace this with your own logic)
        global_variable += 1
        time.sleep(1)

# Function to write the global variable value and current time to a CSV file
def write_to_csv(filename,global_variable,state):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Write global variable value and current time to CSV file
    with open(filename, 'ab') as csvfile:  # Use 'ab' for Python 2.7
        writer = csv.writer(csvfile)
        writer.writerow([current_time, global_variable,state])

# Main function to start threads
def main():
    # Start a thread to update the global variable
    update_thread = threading.Thread(target=update_global_variable)
    update_thread.daemon = True  # Set as daemon thread to terminate with main program
    update_thread.start()

    # Start a thread to write the global variable and current time to CSV file
    csv_thread = threading.Thread(target=write_to_csv, args=('log.csv',))
    csv_thread.daemon = True  # Set as daemon thread to terminate with main program
    csv_thread.start()

    # Keep main program running
    while True:
        pass

if __name__ == "__main__":
    main()

