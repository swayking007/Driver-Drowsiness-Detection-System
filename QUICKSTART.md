# Quick Start Guide - 5 Minutes to Running

## 🚀 Fastest Way to Get Started

### Step 1: Install (2 minutes)

Open PowerShell or Command Prompt in the project folder and run:

```bash
pip install opencv-python numpy mediapipe
```

**That's it!** Only 3 packages needed.

### Step 2: Run (10 seconds)

```bash
python main.py
```

### Step 3: Test (30 seconds)

1. Position yourself in front of webcam
2. Wait for face detection (you'll see landmarks)
3. Close your eyes for 2+ seconds
4. **Alert should trigger!** (Red overlay + beep sound)

## ✅ Success Indicators

You'll know it's working when you see:

- ✅ Camera window opens
- ✅ Your face is detected (landmarks visible if enabled)
- ✅ EAR values displayed (around 0.25-0.35 when eyes open)
- ✅ Status panel in top-right corner
- ✅ FPS counter in bottom-left

## 🐛 Quick Troubleshooting

**Camera not opening?**
- Try: Change `CAMERA_INDEX = 1` in `config.py`
- Check: Is camera being used by another app?

**Face not detected?**
- Ensure good lighting
- Position face directly in front of camera
- Remove glasses temporarily to test

**No sound?**
- Check Windows volume
- Sound is Windows beep (winsound module)

## 📝 What Each File Does

- `main.py` - **Run this file!** Main application
- `config.py` - Adjust settings (thresholds, camera, etc.)
- `modules/face_detector.py` - Detects your face
- `modules/eye_detector.py` - Tracks your eyes
- `modules/drowsiness_detector.py` - Detects drowsiness
- `modules/alert_system.py` - Shows alerts

## 🎯 Next Steps

1. **Customize**: Edit `config.py` to adjust sensitivity
2. **Experiment**: Try different EAR thresholds
3. **Extend**: Add your own features!

## 💡 Pro Tips

- **Lower EAR_THRESHOLD** = More sensitive (detects drowsiness easier)
- **Higher DROWSY_TIME_THRESHOLD** = Longer wait before alert
- **Press 'q'** to quit anytime
- **Check FPS** - Should be 20+ for smooth operation

---

**Ready? Run `python main.py` now!**

