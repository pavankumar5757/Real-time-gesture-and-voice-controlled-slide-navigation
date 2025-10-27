🎯 Gesture Control: Real-Time Gesture & Voice-Controlled Presentation System

B.Tech Final Year Project  
By: A. Pavan Kumar, T. Dileep, K. Karthik, D. Prakash  
Institution: Sanketika Vidya Parishad Engineering College  
Department: Computer Science and Engineering

🧠 Overview

Gesture Control is a real-time, computer vision-based system written in Python, enabling users to control presentation slides using hand gestures and voice commands—no keyboard or mouse required.  
Powered by OpenCV, cvzone, and SpeechRecognition libraries, it provides a hands-free, interactive experience for smart classrooms, conferences, or remote teaching.

🚀 Features

- Hand Gesture Navigation: Navigate slides (next/previous) with intuitive hand gestures.
- Voice Commands: Control navigation by speaking commands (e.g., “Next Slide”, “Jump to Slide 2”).
- Annotation & Drawing: Draw or erase directly on the slides using gestures.
- Pointer Control: Use your hand as a virtual pointer.
- Accurate & Fast: ~88.5% gesture recognition accuracy, less than 120ms per frame.
- Cross-Platform: Runs on Windows, macOS, or Linux with any standard webcam and microphone.

🗂️ Project Structure

Gesture control/
├── code/
│   └── Gesture_master_code.py
├── documentation/
│   ├── Gesture-Master abstract.docx
│   ├── Gesture-Master-Documentation_1.pdf
│   ├── IJIRT174316_PAPER-Gesture_master.pdf
│   └── Gesture-Master_ppt-3.pptx
├── screenshots/
│   └── [project screenshots/images]
└── README.md

⚙️ Getting Started

Requirements

- Python: 3.8 or above
- Hardware: Webcam and Microphone

Dependencies

Install the required libraries:

```bash
pip install opencv-python cvzone numpy SpeechRecognition pyautogui pyaudio
```

If you have trouble installing pyaudio:

```bash
pip install pipwin
pipwin install pyaudio
```

Running the Project

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/gesture-control.git
   cd gesture-control
   ```

2. Navigate to the code directory:

   ```bash
   cd code
   ```

3. Run the main file:

   ```bash
   python Gesture_master_code.py
   ```

4. Start presenting!  
   Ensure your webcam and microphone are enabled.

🎮 Usage Instructions

Hand Gestures

| Gesture            | Action           |
|--------------------|------------------|
| 👍 Thumb Up        | Previous Slide   |
| 🤙 Pinky Up        | Next Slide       |
| 👆 Index + Thumb   | Draw on Slide    |
| ✊ Closed Fist     | Erase Annotation |
| ✌️ Two Fingers     | Zoom/Select      |
| ✋ Full Palm       | Virtual Pointer  |

Voice Commands

| Command              | Action                       |
|----------------------|-----------------------------|
| Next Slide           | Moves forward one slide      |
| Previous Slide       | Moves back one slide         |
| Jump to slide n      | Goes directly to slide n     |


📸 Screenshots

See the `screenshots/` folder for example results, gesture detection, and UI snapshots.

📚 Documentation

Supporting documents (abstract, report, research paper, and presentation slides) are available in the `documentation/` folder.

👨‍🏫 Credits

Project Guide:  
G. Vijaya Lakshmi, Assistant Professor, Department of CSE, SVPEC

Developed by:  
A. Pavan Kuma, Student, Department of CSE,SVPEC  
T. Dileep  
K. Karthik  
D. Prakash

🪪 License

Created for educational and research demonstration purposes.  
All rights reserved © 2025 – Sanketika Vidya Parishad Engineering College.

⭐ Acknowledgments

Special thanks to the Department of Computer Science and Engineering, SVPEC, for their continuous guidance and support.
