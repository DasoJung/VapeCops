import RPi.GPIO as GPIO
from time import sleep

# Set the GPIO pin numbering mode to BCM
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering (GPIO pin numbers)

# Example with two IR sensors
LEFT_SENSOR_PIN = 10  # GPIO pin for the left sensor
RIGHT_SENSOR_PIN = 23  # GPIO pin for the right sensor

# Set the IR sensor pins as input
GPIO.setup(LEFT_SENSOR_PIN, GPIO.IN)
GPIO.setup(RIGHT_SENSOR_PIN, GPIO.IN)

# Function to check both sensors and determine line status
def check_line():
    left = GPIO.input(LEFT_SENSOR_PIN)  # Read the left sensor
    right = GPIO.input(RIGHT_SENSOR_PIN)  # Read the right sensor
    return left, right  # Correct indentation here
