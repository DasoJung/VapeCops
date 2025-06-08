import RPi.GPIO as GPIO
import time
import sqlite3
from datetime import datetime

class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin, db_path='VC.db'):
        self.TRIGGER = trigger_pin
        self.ECHO = echo_pin
        self.db_path = db_path

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, GPIO.LOW)

        start_time = time.time()
        while GPIO.input(self.ECHO) == 0:
            start_time = time.time()

        stop_time = time.time()
        while GPIO.input(self.ECHO) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
        return distance

    def log_detection_to_db(self, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vc_sensor (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER,
                time TEXT
            )
        ''')
        
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M')
        cursor.execute("INSERT INTO vc_sensor (value, time) VALUES (?, ?)", (value, current_time))
        conn.commit()
        conn.close()

    def run(self):
        try:
            while True:
                distance = self.measure_distance()
                print(f"Distance: {distance:.2f} cm")

                if distance <= 50:
                    print("Object detected within 50 cm. Logging to database.")
                    self.log_detection_to_db(value=1)

                time.sleep(1)
                
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    sensor = DistanceSensor(trigger_pin=17, echo_pin=27)
    sensor.run()
