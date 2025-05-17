import cv2
import numpy as np
import mediapipe as mp
import screen_brightness_control as sbc
import pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import speech_recognition as sr
import pyttsx3
from comtypes import CLSCTX_ALL
import threading
import sys

# Initialize Pycaw for Volume Control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Initialize Pyttsx3 for Voice Feedback
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech

# Initialize MediaPipe for Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# OpenCV Webcam Setup
cap = cv2.VideoCapture(0)

# Function to Change System Volume Safely
def change_volume(increase=True):
    current_volume = volume.GetMasterVolumeLevelScalar()  # Get current volume (0.0 - 1.0)
    new_volume = min(current_volume + 0.1, 1.0) if increase else max(current_volume - 0.1, 0.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)  # Set new volume level
    return int(new_volume * 100)  # Return volume percentage

# Function to Change Brightness Safely
def change_brightness(increase=True):
    """Safely increase or decrease screen brightness."""
    current_brightness = sbc.get_brightness()
    
    if isinstance(current_brightness, list):  
        current_brightness = current_brightness[0]  # Extract first display brightness
    
    new_brightness = min(current_brightness + 10, 100) if increase else max(current_brightness - 10, 10)
    sbc.set_brightness(new_brightness)

# Function to Capture Screenshot
def take_screenshot():
    pyautogui.screenshot("screenshot.png")
    print("Screenshot taken.")

# Function to Process Voice Commands
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening for command...")
            try:
                audio = recognizer.listen(source, timeout=5)  # You can remove timeout for continuous listening
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")

                if "increase volume" in command:
                    change_volume(increase=True)
                    engine.say("Increasing volume")
                elif "decrease volume" in command:
                    change_volume(increase=False)
                    engine.say("Decreasing volume")
                elif "brightness up" in command:
                    change_brightness(increase=True)
                    engine.say("Increasing brightness")
                elif "brightness down" in command:
                    change_brightness(increase=False)
                    engine.say("Decreasing brightness")
                elif "screenshot" in command:
                    take_screenshot()
                    engine.say("Screenshot taken")
                elif "pause music" in command:
                    pyautogui.press("playpause")
                    engine.say("Music paused")
                elif "next song" in command:
                    pyautogui.press("nexttrack")
                    engine.say("Skipping to next song")
                elif "previous song" in command:
                    pyautogui.press("prevtrack")
                    engine.say("Playing previous song")
                
                engine.runAndWait()

            except sr.UnknownValueError:
                print("Could not understand the command.")
            except sr.RequestError:
                print("Speech recognition service unavailable.")
            except sr.WaitTimeoutError:
                print("No voice detected, continuing...")
                continue  # Keeps listening without crashing


# Start Voice Recognition in a Separate Thread
voice_thread = threading.Thread(target=recognize_voice, daemon=True)
voice_thread.start()

# Main Gesture Detection Function
def detect_gestures():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror the image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get finger tip positions
                landmarks = hand_landmarks.landmark
                index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]

                # Convert to pixel positions
                h, w, _ = frame.shape
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

                # Distance between thumb and index finger
                distance = np.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)

                if distance > 70:  # Open fingers apart → Increase Volume
                    vol = change_volume(increase=True)
                    cv2.putText(frame, f"Increasing Volume: {vol}%", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                elif distance < 30:  # Fingers close together → Decrease Volume
                    vol = change_volume(increase=False)
                    cv2.putText(frame, f"Decreasing Volume: {vol}%", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Volume Indicator Bar
                vol_level = int(volume.GetMasterVolumeLevelScalar() * 100)
                cv2.rectangle(frame, (50, 150), (80, 400), (255, 255, 255), 3)
                cv2.rectangle(frame, (50, int(400 - (vol_level * 2.5))), (80, 400), (0, 255, 0), -1)
                cv2.putText(frame, f"Vol: {vol_level}%", (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the Gesture Detection
detect_gestures()
