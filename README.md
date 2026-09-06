# AI-Powered Fitness Trainer with Automatic Exercise Recognition and Repetition Counting

## Problem Statement

Engaging in regular physical exercise without certified professional supervision often leads to improper form, inaccurate tracking of workout metrics, and an increased likelihood of musculoskeletal injuries. Conventional fitness applications predominantly depend on manual user logging, a process that is both error-prone and disruptive during workout sessions. Consequently, there is a distinct need for an automated, accessible, and computer-vision-based fitness monitoring system capable of accurately analyzing human biomechanics in real time without necessitating wearable sensors or specialized hardware.

This project addresses these challenges by developing an AI-driven personal fitness evaluation system. Leveraging state-of-the-art computer vision and deep learning techniques, the application captures video from a standard webcam, extracts body landmarks, classifies exercise actions, and counts repetitions in real time.

---

## Objectives

1. **Automated Exercise Recognition**: Accurately classify physical exercises (including push-ups, squats, bicep curls, and shoulder presses) from temporal landmark sequences utilizing a Bidirectional Long Short-Term Memory (BiLSTM) network.
2. **Real-Time Repetition Counting**: Dynamically track repetitions through geometric joint-angle estimation derived from coordinate landmark positions, eliminating the need for manual logging.
3. **Low-Latency Feedback**: Process live video streams and display instantaneous visual feedback, metric updates, and posture status overlays on user interfaces.
4. **Offline Video Analysis**: Support recorded video uploads for retrospective performance assessment and repetition verification.
5. **Interactive Fitness Advisory**: Integrate a conversational assistant to answer exercise-related queries and provide contextual fitness guidance.

---

## Scope of Contribution and Planned Enhancements

While the baseline framework is grounded in research on real-time exercise classification (*arXiv:2411.11548*), this capstone initiative focuses on extending and standardizing the system through the following enhancements:

### 1. Workout Analytics and Session Tracking
- Implementation of session-level tracking and structured data logging for completed sets and repetitions.
- Visualization of historical performance metrics to monitor user progression over time.
- Automated generation of post-workout summary reports.

### 2. Extension of Exercise Repertoire
- Integration of kinematic analysis and angle-tracking logic for additional compound movements, beginning with lunges.
- Modularized pose-logic architecture to facilitate future expansion to complex calisthenics exercises.

### 3. Biomechanical Form Evaluation
- Development of threshold-based posture validation checks to detect form discrepancies (e.g., knee displacement during squats or incomplete extension during curls).
- Real-time visual warning indicators to guide corrective posture adjustments.

---

## Technical Stack

| Component | Framework / Library | Role |
|---|---|---|
| Pose Estimation | MediaPipe Pose | Real-time 33-point skeletal landmark extraction |
| Temporal Classification | TensorFlow / Keras | Bidirectional LSTM neural network architecture |
| Application Interface | Streamlit | Web interface for webcam feed and analytics |
| Computer Vision | OpenCV | Frame manipulation, drawing, and video streaming |
| Conversational Assistant | OpenAI API / LangChain | Fitness knowledge querying and user interaction |
| Core Language | Python 3.9+ | Backend pipeline and algorithmic execution |

---

## References

1. Riccio, R. (2024). *Real-Time Fitness Exercise Classification and Counting from Video Frames.* arXiv:2411.11548.
2. Lugaresi, C., et al. (2019). *MediaPipe: A Framework for Building Perception Pipelines.* arXiv:1906.08172.
3. Hochreiter, S., & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation, 9(8), 1735-1780.
4. Schuster, M., & Paliwal, K. K. (1997). *Bidirectional Recurrent Neural Networks.* IEEE Transactions on Signal Processing, 45(11), 2673-2681.
