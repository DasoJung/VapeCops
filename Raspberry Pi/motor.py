import RPi.GPIO as GPIO
from time import sleep

IN1 = 13
IN2 = 19
IN3 = 18
IN4 = 12

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setwarnings(False)  # Disable warnings

# Set motor control pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Set up PWM for motor speed control (1kHz frequency)
motor1_pwm = GPIO.PWM(IN1, 1000)
motor2_pwm = GPIO.PWM(IN3, 1000)

motor1_pwm.start(0)  # Start with motor 1 at 0% speed (stopped)
motor2_pwm.start(0)  # Start with motor 2 at 0% speed (stopped)

# Function to set the speed of both motors
def set_speed(speed):
    motor1_pwm.ChangeDutyCycle(speed)  # Set speed for motor 1
    motor2_pwm.ChangeDutyCycle(speed)  # Set speed for motor 2

# Function to move both motors forward
def forward(speed):
    set_speed(speed) 
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

# Function to move both motors backward
def backward(speed):
    set_speed(speed) 
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

# Function to turn left (Motor 1 forward, Motor 2 backward)
def turn_left(speed):
    set_speed(speed) 
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

# Function to turn right (Motor 1 backward, Motor 2 forward)
def turn_right(speed):
    set_speed(speed) 
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

# Function to stop both motors
def rest():
    set_speed(0)  # Stop the motors by setting the speed to 0
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Cleanup GPIO settings after test is complete
