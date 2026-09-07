# --- fitness_demo_idle.py ---
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import threading
import time

# --- Configuration ---
EXERCISES = {
    "bicep_curl": {
        "name": "Bicep Curl",
        "landmarks": [11, 13, 15],
        "angle_threshold_down": 160,
        "angle_threshold_up": 30,
    },
    "squat": {
        "name": "Squat",
        "landmarks": [23, 25, 27],
        "angle_threshold_down": 90,
        "angle_threshold_up": 160,
    }
}

# --- Helper Functions ---
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# --- Main Application Class ---
class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ Personal AI Trainer Demo")
        self.root.geometry("900x750")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.is_running = False
        self.cap = None
        self.counter = 0
        self.stage = None
        self.exercise_type = "bicep_curl"
        
        # Create UI
        self.setup_ui()
        
        # MediaPipe setup
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🏋️ Personal AI Trainer Demo", 
                               font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.root, text="Real-time Exercise Recognition & Counting", 
                                  font=('Arial', 14), bg='#2c3e50', fg='#ecf0f1')
        subtitle_label.pack(pady=5)
        
        # Main frame for video
        self.video_frame = tk.Frame(self.root, bg='#34495e', width=640, height=480)
        self.video_frame.pack(pady=10)
        self.video_frame.pack_propagate(False)
        
        # Video label
        self.video_label = tk.Label(self.video_frame, bg='#34495e')
        self.video_label.pack(expand=True, fill='both')
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#2c3e50')
        status_frame.pack(pady=10)
        
        # Status labels
        self.status_label = tk.Label(status_frame, text="Status: Waiting to start...", 
                                     font=('Arial', 12), bg='#2c3e50', fg='#ecf0f1')
        self.status_label.grid(row=0, column=0, padx=10)
        
        self.rep_label = tk.Label(status_frame, text="Repetitions: 0", 
                                  font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#2ecc71')
        self.rep_label.grid(row=0, column=1, padx=10)
        
        self.angle_label = tk.Label(status_frame, text="Angle: --", 
                                    font=('Arial', 12), bg='#2c3e50', fg='#f1c40f')
        self.angle_label.grid(row=0, column=2, padx=10)
        
        # Control frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        # Exercise selection
        exercise_label = tk.Label(control_frame, text="Select Exercise:", 
                                  font=('Arial', 11), bg='#2c3e50', fg='white')
        exercise_label.grid(row=0, column=0, padx=5)
        
        self.exercise_var = tk.StringVar(value="bicep_curl")
        exercise_dropdown = ttk.Combobox(control_frame, textvariable=self.exercise_var, 
                                         values=list(EXERCISES.keys()), 
                                         state="readonly", width=15)
        exercise_dropdown.grid(row=0, column=1, padx=5)
        exercise_dropdown.bind('<<ComboboxSelected>>', self.on_exercise_change)
        
        # Start/Stop buttons
        self.start_button = tk.Button(control_frame, text="▶ Start Webcam", 
                                      command=self.start_webcam, 
                                      bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                                      padx=20, pady=8)
        self.start_button.grid(row=0, column=2, padx=10)
        
        self.stop_button = tk.Button(control_frame, text="⏹ Stop", 
                                     command=self.stop_webcam,
                                     bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                     padx=20, pady=8, state='disabled')
        self.stop_button.grid(row=0, column=3, padx=10)
        
        # Reset button
        self.reset_button = tk.Button(control_frame, text="🔄 Reset Count", 
                                      command=self.reset_counter,
                                      bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                                      padx=20, pady=8)
        self.reset_button.grid(row=0, column=4, padx=10)
        
        # Info text
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=10)
        info_label = tk.Label(info_frame, 
                              text="💡 Stand in front of camera and perform the selected exercise",
                              font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        info_label.pack()
        
        # Placeholder message
        self.placeholder_text = tk.Label(self.video_frame, text="Click 'Start Webcam' to begin",
                                         font=('Arial', 18), bg='#34495e', fg='#7f8c8d')
        self.placeholder_text.place(relx=0.5, rely=0.5, anchor='center')
        
    def on_exercise_change(self, event):
        self.exercise_type = self.exercise_var.get()
        self.reset_counter()
        if self.is_running:
            self.status_label.config(text=f"Status: Switched to {EXERCISES[self.exercise_type]['name']}")
    
    def reset_counter(self):
        self.counter = 0
        self.stage = None
        self.rep_label.config(text="Repetitions: 0")
        
    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.config(text="❌ Could not open webcam. Check permissions!")
            return
            
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.placeholder_text.destroy()
        self.status_label.config(text="Status: Running...")
        self.update_frame()
        
    def stop_webcam(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Status: Stopped")
        
    def update_frame(self):
        if not self.is_running or self.cap is None:
            return
            
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="❌ Failed to capture frame")
            self.stop_webcam()
            return
            
        # Process frame
        processed_frame, new_reps, angle, current_stage = self.process_frame(frame)
        
        # Update counter
        if new_reps == 1 and current_stage != self.stage:
            self.counter += 1
            self.stage = current_stage
            self.rep_label.config(text=f"Repetitions: {self.counter}")
        elif new_reps == 0:
            self.stage = current_stage
            
        # Update angle display
        if angle is not None:
            self.angle_label.config(text=f"Angle: {int(angle)}°")
        else:
            self.angle_label.config(text="Angle: --")
            
        # Convert for display
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(processed_frame_rgb)
        img_tk = ImageTk.PhotoImage(img)
        
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk
        
        # Schedule next update
        self.root.after(30, self.update_frame)
        
    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        results = None
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        rep_count = 0
        current_stage = None
        angle = None
        exercise_type = self.exercise_type
        landmarks_to_track = EXERCISES[exercise_type]["landmarks"]
        
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
            
            landmarks = results.pose_landmarks.landmark
            h, w, _ = image.shape
            
            try:
                points = []
                for idx in landmarks_to_track:
                    points.append([landmarks[idx].x * w, landmarks[idx].y * h])
                
                angle = calculate_angle(points[0], points[1], points[2])
                
                if exercise_type == "bicep_curl":
                    if angle > EXERCISES[exercise_type]["angle_threshold_down"]:
                        current_stage = "down"
                    elif angle < EXERCISES[exercise_type]["angle_threshold_up"] and self.stage == "down":
                        current_stage = "up"
                        rep_count = 1
                        
                elif exercise_type == "squat":
                    if angle > EXERCISES[exercise_type]["angle_threshold_up"]:
                        current_stage = "up"
                    elif angle < EXERCISES[exercise_type]["angle_threshold_down"] and self.stage == "up":
                        current_stage = "down"
                        rep_count = 1
                        
            except:
                pass
        
        # Display info on frame
        cv2.putText(image, f"Exercise: {EXERCISES[exercise_type]['name']}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f"Reps: {self.counter}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if angle is not None:
            cv2.putText(image, f"Angle: {int(angle)}", (10, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return image, rep_count, angle, current_stage
        
    def on_closing(self):
        self.stop_webcam()
        self.root.destroy()

# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
