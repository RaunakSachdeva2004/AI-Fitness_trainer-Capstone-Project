# AI-Powered Fitness Trainer with Automatic Exercise Recognition and Rep Counting

## 📌 Problem Statement

In today's fast-paced world, a large portion of the population exercises without professional supervision, leading to poor form, inaccurate repetition tracking, and increased risk of injury. Traditional fitness apps rely on manual input from users to log workouts, which is both unreliable and inconvenient. There is a growing need for an intelligent, accessible, and automated fitness monitoring system that can analyze human body movements in real time — without the need for wearable sensors or specialized equipment.

This project addresses that gap by developing an **AI-powered personal fitness trainer** that uses computer vision and deep learning to automatically recognize exercises being performed and count repetitions accurately using only a standard webcam.

---

## 🎯 Objectives

1. **Exercise Recognition** — Automatically identify the type of exercise being performed (e.g., push-ups, squats, bicep curls, shoulder press) using a Bidirectional LSTM model trained on body pose landmarks extracted via MediaPipe.

2. **Repetition Counting** — Count exercise repetitions in real time using joint angle thresholds derived from pose estimation, without any manual input from the user.

3. **Real-Time Feedback** — Process live webcam feed and provide on-screen feedback about the current exercise and rep count with minimal latency.

4. **Video Analysis Mode** — Allow users to upload recorded workout videos for offline analysis and rep counting.

5. **Conversational Fitness Assistant** — Integrate an AI chatbot to answer fitness-related queries and provide basic guidance, making the system more interactive and user-friendly.

---

## 🚀 My Contribution (Planned Enhancements)

The base system from the research paper *"Real-Time Fitness Exercise Classification and Counting from Video Frames"* [(arXiv:2411.11548)](https://arxiv.org/abs/2411.11548) provides the core exercise classification pipeline. As part of this capstone project, the following enhancements are being developed:

### 1. 📊 Workout Analytics Dashboard
A session-level analytics module that tracks and visualizes:
- Total reps per exercise per session
- Rep count trends over time (session history)
- A simple performance summary displayed after each workout session

### 2. 🏋️ New Exercise Support — Lunges
Extending the model's capability by adding **lunge** detection and rep counting logic using MediaPipe knee and hip angle analysis, which was not part of the original implementation.

### 3. 📝 Form Feedback (Basic)
Adding a basic **form quality indicator** that warns the user if key joint angles go significantly out of the expected range during an exercise (e.g., knees going too far forward in a squat).

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Pose Estimation | MediaPipe Pose |
| Exercise Classification | Bidirectional LSTM (TensorFlow/Keras) |
| Web Interface | Streamlit |
| Video Processing | OpenCV |
| AI Chatbot | OpenAI GPT / LangChain |
| Language | Python 3.9+ |

---

## 📚 References

1. Riccio, R. (2024). *Real-Time Fitness Exercise Classification and Counting from Video Frames.* arXiv:2411.11548.
2. Lugaresi, C., et al. (2019). *MediaPipe: A Framework for Building Perception Pipelines.* arXiv:1906.08172.
3. Hochreiter, S., & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation, 9(8).
4. Schuster, M., & Paliwal, K. K. (1997). *Bidirectional Recurrent Neural Networks.* IEEE Transactions on Signal Processing.
