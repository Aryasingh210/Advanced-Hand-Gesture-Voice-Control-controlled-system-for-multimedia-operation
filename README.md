🎛️ Advanced Hand Gesture & Voice-Controlled System for Multimedia Operations

This project presents an AI-powered system interface that allows users to control multimedia operations such as volume adjustment, playback control, and system commands using a hybrid approach of hand gestures and voice commands. The solution is built using Python, integrating computer vision, speech recognition, and audio control libraries to deliver a hands-free and intuitive user experience.

🚀 Features
✋ Hand Gesture Recognition (via webcam using MediaPipe and OpenCV)

Control system volume with finger distance

Play/Pause media

Mute/Unmute

Custom gestures for custom actions

🎤 Voice Command Integration

Play/Pause music

Volume up/down

Stop/Next/Previous

Shutdown/Restart system (optional with safety prompt)

🧠 Machine Learning & AI Tools Used

Real-time hand tracking (MediaPipe)

Speech recognition (SpeechRecognition, PyAudio, Google API)

Audio control (pycaw, ctypes)

💻 User Interface (optional)

Tkinter-based GUI or PyQt5-based dashboard (for gesture feedback and voice logs)

🧰 Tech Stack
Component	Technology
Language	Python 3.x
Computer Vision	OpenCV, MediaPipe
Speech Processing	SpeechRecognition, PyAudio
System Audio Control	pycaw
GUI (optional)	Tkinter or PyQt5

📷 How It Works
Gesture Module

Captures hand via webcam.

Uses MediaPipe to detect hand landmarks.

Calculates distance between fingers to adjust volume.

Voice Module

Listens for voice commands through the microphone.

Uses Google Speech-to-Text API to transcribe.

Maps commands to specific actions.

System Integration

Controls volume through Pycaw.

Sends OS-level commands where applicable.

GUI optionally displays real-time feedback.

🛠️ Setup Instructions
bash
Copy
Edit
git clone https://github.com/your-username/gesture-voice-multimedia-control.git
cd gesture-voice-multimedia-control
pip install -r requirements.txt
python main.py
Make sure your system has:

A webcam

A working microphone

Python 3.7+

Access to the internet (for Google Speech API)

📁 Project Structure
bash
Copy
Edit
gesture-voice-multimedia-control/
│

├── main.py                  # Main runner
├── hand_gesture.py          # Handles hand tracking logic
├── voice_commands.py        # Handles speech input
├── volume_controller.py     # Controls system volume
├── gui.py                   # Optional Tkinter/PyQt GUI
├── utils.py                 # Helper functions
├── requirements.txt
└── README.md


📽️ Demo
(Include a short GIF/video link showing gesture + voice control in action)

📚 References
MediaPipe Hands

OpenCV Documentation

Pycaw Library

SpeechRecognition Python

📌 Future Improvements
Add more custom gesture mappings

Integrate multilingual voice support

Add calibration and setup wizard

Support for media players (Spotify, VLC, etc.)

🧑‍💻 Author
Arya Singh
📧 Email: singharya06164


