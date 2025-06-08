import RPi.GPIO as GPIO
import sqlite3
import pygame
import subprocess
import threading
import time
from motor import forward, backward, turn_right, turn_left, rest
from light import LEFT_SENSOR_PIN, RIGHT_SENSOR_PIN
from ul import measure_distance

TRIGGER_PIN = 17
ECHO_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Function to clear all entries in vc_cam table (This will be called when main_final.py starts)
def clear_vc_cam_table():
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vc_cam")  # Delete all records in vc_cam
    conn.commit()
    conn.close()
    print("vc_cam table has been cleared.")

# Function to clear all entries in vc_sensor table (This will be called when main_final.py starts)
'''
def clear_vc_sensor_table():
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vc_sensor")  # Delete all records in vc_sensor
    conn.commit()
    conn.close()
    print("vc_sensor table has been cleared.")


# Function to check the latest value in the vc_distance table (for distance <= 50cm)
def check_distance_alert():
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    
    # Check the most recent entry in vc_sensor table for a value = 1 (distance <= 50cm)
    cursor.execute("SELECT ID, value FROM vc_sensor ORDER BY ID DESC LIMIT 1")
    distance_entry = cursor.fetchone()
    conn.close()
    
    # Return True if the latest entry is an alert (value=1)
    return distance_entry and distance_entry[1] == 1, distance_entry[0] if distance_entry else None

# Function to delete the processed distance entry by ID
def delete_distance_alert_entry(alert_id):
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vc_sensor WHERE ID = ?", (alert_id,))
    conn.commit()
    conn.close()
    print(f"Deleted distance alert entry with ID {alert_id}")
'''
# Function to check the database for the latest alert condition (for smoking detection)
def check_db_for_alert():
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    
    # Check the most recent entry in vc_cam table for a value = 1 (smoking detected)
    cursor.execute("SELECT ID, value FROM vc_cam ORDER BY ID DESC LIMIT 1")
    cam_entry = cursor.fetchone()
    conn.close()
    
    # Return True if the latest entry is an alert (value=1)
    return cam_entry and cam_entry[1] == 1, cam_entry[0] if cam_entry else None

# Function to delete the processed alert entry by ID (for smoking detection)
def delete_alert_entry(alert_id):
    conn = sqlite3.connect('VC.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vc_cam WHERE ID = ?", (alert_id,))
    conn.commit()
    conn.close()
    print(f"Deleted alert entry with ID {alert_id}")

# Function to play alert sound
def play_alert():
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    print("Playing alert sound.")
    while pygame.mixer.music.get_busy():
        pass  # Wait until sound finishes playing

# Function to run db_cam.py in the background
def run_db_cam():
    subprocess.Popen(["python3", "db_cam.py"])
'''
# Function to run db_distance.py in the background
def run_db_distance():
    subprocess.Popen(["python3", "db_distance.py"])
'''
# Start the db_cam.py and db_distance.py scripts in background using threads
def start_background_processes():
    threading.Thread(target=run_db_cam, daemon=True).start()
    #threading.Thread(target=run_db_distance, daemon=True).start()

# Main execution loop
try:
    # Clear the vc_cam, vc_sensor, and vc_distance tables when the script starts
    clear_vc_cam_table()  # This will clear the vc_cam table every time main_final.py runs
    #clear_vc_sensor_table()  # This will clear the vc_sensor table every time main_final.py runs

    start_background_processes()  # Start db_cam and db_distance in the background

    speed = 30  # Speed value for motor
    while True:
        # Check the database for smoking detection alert
        alert_detected, alert_id = check_db_for_alert()
        if alert_detected:
            print("Alert detected in the database (smoking detection). Stopping the robot and playing alert sound.")
            rest()  # Stop the robot
            play_alert()  # Play alert sound
            delete_alert_entry(alert_id)  # Delete the processed alert entry after playing sound
            continue  # Skip to next loop iteration
        '''
        # Check the database for distance alert (50cm or less)
        distance_alert_detected, distance_alert_id = check_distance_alert()
        if distance_alert_detected:
            print("Alert detected in the database (distance <= 50cm). Stopping the robot.")
            rest()  # Stop the robot
            #delete_distance_alert_entry(distance_alert_id)  # Delete the processed distance alert entry
            continue  # Skip to next loop iteration
        '''     
        # If no alert, proceed with line-following
        left = GPIO.input(LEFT_SENSOR_PIN)
        right = GPIO.input(RIGHT_SENSOR_PIN)
        
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        
        if distance > 50:
            if left == GPIO.LOW and right == GPIO.LOW:
                forward(speed)
                print("Neither sensor detects black, moving both motors forward")
            
            elif left != GPIO.LOW and right != GPIO.LOW:
                backward(speed)
                print("Both sensors detected not black, moving both motors backward")

            elif right == GPIO.LOW:
                turn_right(speed)
                print("Right sensor detected black, turning right (motor 2)")

            elif left == GPIO.LOW:
                turn_left(speed)
                print("Left sensor detected black, turning left (motor 1)")
            
        elif distance <= 50:
            rest()
            print("motor stop")

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    GPIO.cleanup()  # Clean up GPIO settings when the program finishes
