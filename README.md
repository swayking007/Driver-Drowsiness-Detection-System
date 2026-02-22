# 🚗 Driver Drowsiness Detection System

A complete, real-time computer vision system that detects driver drowsiness and fatigue using facial landmarks and eye tracking. Built for hackathon demonstrations with beginner-friendly code and comprehensive documentation.

## 📋 Features

- ✅ **Real-time webcam feed processing** - Live video capture and analysis
- ✅ **Face detection** - Automatic face detection using MediaPipe
- ✅ **Facial landmark detection** - 468-point face mesh for precise tracking
- ✅ **Eye landmark extraction** - Accurate eye region detection
- ✅ **Eye Aspect Ratio (EAR) calculation** - Mathematical measure of eye openness
- ✅ **Blink detection** - Automatic blink counting and rate calculation
- ✅ **Drowsiness detection timer** - Tracks how long eyes remain closed
- ✅ **Alarm sound trigger** - Audio alert when drowsiness detected
- ✅ **Real-time overlay UI** - Visual feedback with status information
- ✅ **Status text display** - Alert/Drowsy/Normal status indicators
- ✅ **Fatigue score meter** - 0-100 fatigue level tracking
- ✅ **Clean modular code** - Well-organized, commented, maintainable code

## 🛠️ Tech Stack

- **Python 3.8+** - Programming language
- **OpenCV** - Image processing and video capture
- **MediaPipe** - Face and landmark detection (pre-trained models)
- **NumPy** - Numerical computations
- **Windows winsound** - Audio alerts (built-in, no extra install)

## 📁 Complete Project Structure

```
SaveLife/
├── requirements.txt              # Python dependencies
├── README.md                    # This file - project documentation
├── INSTALL.md                   # Detailed installation guide
├── config.py                    # Configuration settings (adjustable)
├── main.py                      # Main application entry point
├── .gitignore                   # Git ignore file
├── modules/
│   ├── __init__.py
│   ├── face_detector.py         # Face detection using MediaPipe
│   ├── eye_detector.py          # Eye detection and EAR calculation
│   ├── drowsiness_detector.py   # Main drowsiness detection logic
│   └── alert_system.py          # Alert and notification system
└── utils/
    ├── __init__.py
    ├── constants.py             # Constants and landmark indices
    └── helpers.py               # Utility functions (EAR, distance, etc.)
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `opencv-python>=4.8.0`
- `numpy>=1.24.0`
- `mediapipe>=0.10.0`

### Step 2: Run the Application

```bash
python main.py
```

### Step 3: Use the System

1. **Position yourself** in front of the webcam
2. **Keep your face visible** - system will detect your face automatically
3. **Test the alert** - Close your eyes for 2+ seconds to trigger drowsiness alert
4. **Monitor status** - Check the status panel for real-time information
5. **Press 'q'** to quit

## 📖 How It Works

### 1. Face Detection
- Uses MediaPipe Face Mesh to detect face in real-time
- Extracts 468 facial landmark points
- Works with single face (driver)

### 2. Eye Detection
- Extracts 6 key points for each eye from landmarks
- Calculates Eye Aspect Ratio (EAR) for both eyes
- EAR formula: `(vertical_dist_1 + vertical_dist_2) / (2 * horizontal_dist)`

### 3. Drowsiness Detection
- Monitors EAR values continuously
- Detects when EAR drops below threshold (eyes closing)
- Tracks consecutive frames with closed eyes
- Triggers alert if eyes closed for 2+ seconds

### 4. Alert System
- **Visual Alert**: Red overlay with warning text
- **Audio Alert**: Beep sound (Windows winsound)
- **Status Panel**: Real-time information display

## ⚙️ Configuration

Edit `config.py` to adjust settings:

```python
# Eye closure threshold (lower = more sensitive)
EAR_THRESHOLD = 0.25

# Drowsiness time threshold (seconds)
DROWSY_TIME_THRESHOLD = 2.0

# Camera settings
CAMERA_INDEX = 0  # 0 = first camera, 1 = second, etc.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
```

## 📊 Expected Output

When running, you should see:

1. **Video Window**: Live webcam feed with overlays
2. **Status Panel** (top-right):
   - Status: NORMAL/DROWSY/ALERT
   - EAR: Current Eye Aspect Ratio
   - Blinks: Total blink count
   - Fatigue: Fatigue score (0-100)
3. **On-Screen Text**:
   - EAR values (left and right)
   - FPS counter
   - Instructions

### Normal Operation:
- Green status indicators
- EAR values around 0.25-0.35 (eyes open)
- Blink count increases with natural blinking

### Drowsiness Detected:
- Red overlay appears
- Beep sound plays
- Status changes to "DROWSY"
- Warning text displayed

## 🧪 Testing Checklist

- [ ] Camera opens and displays video feed
- [ ] Face is detected when positioned in front of camera
- [ ] EAR values display correctly (0.2-0.4 range when eyes open)
- [ ] Blink detection works (blink count increases)
- [ ] Drowsiness alert triggers after 2 seconds of closed eyes
- [ ] Audio beep plays when alert triggers
- [ ] Status panel updates in real-time
- [ ] FPS counter shows reasonable frame rate (20+ FPS)
- [ ] System quits cleanly when pressing 'q'

## 🐛 Common Issues & Fixes

### Issue: "No module named 'cv2'"
**Fix:** Install OpenCV: `pip install opencv-python`

### Issue: "Could not open camera"
**Fix:** 
- Check if camera is connected
- Close other applications using camera
- Try changing `CAMERA_INDEX` in `config.py` (0, 1, 2)

### Issue: "MediaPipe installation fails"
**Fix:**
- Use Python 3.8-3.11 (MediaPipe doesn't support 3.12+)
- Try: `pip install mediapipe --no-cache-dir`

### Issue: "Face not detected"
**Fix:**
- Ensure good lighting
- Position face directly in front of camera
- Remove glasses if causing issues
- Check camera focus

### Issue: "False alarms (too sensitive)"
**Fix:**
- Increase `EAR_THRESHOLD` in `config.py` (try 0.20)
- Increase `DROWSY_TIME_THRESHOLD` (try 3.0 seconds)

### Issue: "Not detecting drowsiness"
**Fix:**
- Decrease `EAR_THRESHOLD` in `config.py` (try 0.30)
- Decrease `DROWSY_TIME_THRESHOLD` (try 1.5 seconds)

## 🎯 Hackathon Demo Explanation

### What to Show:

1. **Live Demo:**
   - Run the application
   - Show face detection working
   - Demonstrate blink detection
   - Trigger drowsiness alert by closing eyes

2. **Key Points to Explain:**
   - **Real-time processing**: 20-30 FPS on standard laptop
   - **No training required**: Uses pre-trained MediaPipe models
   - **Mathematical approach**: EAR calculation for accurate detection
   - **Modular design**: Easy to extend and modify
   - **Practical application**: Can save lives on the road

3. **Technical Highlights:**
   - Computer vision techniques
   - Facial landmark detection
   - Eye tracking algorithms
   - Real-time video processing

### Demo Script:

```
"Today I'm demonstrating a Driver Drowsiness Detection System built with 
Python and OpenCV. The system uses MediaPipe to detect facial landmarks 
and calculates the Eye Aspect Ratio to determine if a driver's eyes are 
closed. When drowsiness is detected for more than 2 seconds, it triggers 
both visual and audio alerts. This technology could be integrated into 
vehicles to prevent accidents caused by driver fatigue."
```

## 🔧 Possible Improvements

1. **Head Pose Detection**: Detect when driver looks away
2. **Yawn Detection**: Detect yawning as additional fatigue indicator
3. **Machine Learning**: Train custom model for better accuracy
4. **Mobile App**: Port to Android/iOS for mobile use
5. **Cloud Integration**: Send alerts to monitoring center
6. **Data Logging**: Record drowsiness events for analysis
7. **Multi-face Support**: Detect multiple drivers
8. **Night Vision**: Improve detection in low light
9. **Dashboard Integration**: Connect to car's infotainment system
10. **Machine Learning Fatigue Prediction**: Predict drowsiness before it happens

## 📝 Code Explanation

### Main Components:

1. **FaceDetector** (`modules/face_detector.py`):
   - Initializes MediaPipe Face Mesh
   - Detects face and extracts landmarks
   - Converts normalized coordinates to pixel coordinates

2. **EyeDetector** (`modules/eye_detector.py`):
   - Extracts eye landmarks from face landmarks
   - Calculates EAR for both eyes
   - Determines if eyes are closed

3. **DrowsinessDetector** (`modules/drowsiness_detector.py`):
   - Tracks eye closure duration
   - Counts blinks and calculates blink rate
   - Manages fatigue score
   - Determines drowsiness status

4. **AlertSystem** (`modules/alert_system.py`):
   - Triggers visual and audio alerts
   - Draws status panel
   - Manages alert timing

5. **Main Application** (`main.py`):
   - Coordinates all modules
   - Handles video capture
   - Manages main loop
   - Handles user input

## 📄 License

This project is built for educational and hackathon purposes.

## 👨‍💻 Author

Built for hackathon demonstration - Complete working system ready for demo!

---

## 🎓 Learning Resources

- **OpenCV Documentation**: https://docs.opencv.org/
- **MediaPipe Face Mesh**: https://google.github.io/mediapipe/solutions/face_mesh.html
- **Eye Aspect Ratio Paper**: Research on EAR-based blink detection

---

**Ready to run! Just install dependencies and execute `python main.py`**
