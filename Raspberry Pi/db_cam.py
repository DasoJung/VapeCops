import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import sqlite3
from datetime import datetime
import time

class SmokingDetection:
    def __init__(self, model_path="model"):
        # Load the pre-trained model
        self.model = tf.saved_model.load(model_path)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera.")

    def capture_and_predict(self):
        start_time = time.time()  # Start time for FPS calculation

        # Capture image from the camera
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture image.")
            return None, None
        
        # Preprocess the image
        img = cv2.resize(frame, (124, 124))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        # Predict using the model
        prediction = self.model(img_array, training=False)
        predicted_class = np.argmax(prediction, axis=1)[0]
        
        # Calculate FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        
        # Determine label based on prediction
        label = "Smoking" if predicted_class == 1 else "Non-smoking"
        
        return predicted_class, label, fps, frame

    def log_detection_to_db(self, value):
        # Log detection result to the database
        conn = sqlite3.connect('VC.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vc_cam (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER,
                time TEXT
            )
        ''')
        
        # Insert the detected value with timestamp
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M')
        cursor.execute("INSERT INTO vc_cam (value, time) VALUES (?, ?)", (value, current_time))
        conn.commit()
        conn.close()

    def run(self):
        smoking_start_time = None
        smoking_duration_count = 0

        try:
            while True:
                result, label, fps, frame = self.capture_and_predict()
                
                if result == 1:
                    if smoking_start_time is None:
                        smoking_start_time = time.time()
                    elif time.time() - smoking_start_time >= 2:
                        smoking_duration_count += 1
                        smoking_start_time = None
                        print(f"2-second smoking detection count: {smoking_duration_count}")

                        if smoking_duration_count >= 2:
                            print("Smoking detected for 2 seconds, twice. Logging to database.")
                            self.log_detection_to_db(value=1)
                            smoking_duration_count = 0
                else:
                    smoking_start_time = None
                    smoking_duration_count = 0
                    print("Non-smoking detected.")
                
                # Display the captured frame with label and FPS
                cv2.putText(frame, f"Class: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Camera Feed", frame)
                
                # Exit condition
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = SmokingDetection(model_path="model")
    detector.run()
