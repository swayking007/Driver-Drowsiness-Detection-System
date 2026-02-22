# Installation Instructions

## Step-by-Step Setup Guide

### Prerequisites

1. **Python 3.8 or higher**
   - Check your Python version: `python --version`
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check "Add Python to PATH"

2. **Webcam**
   - Built-in or external USB webcam
   - Make sure it's working (test in other applications)

### Installation Steps

#### Step 1: Navigate to Project Directory

Open Command Prompt or PowerShell and navigate to the project folder:

```bash
cd C:\Users\User\Desktop\SaveLife
```

#### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate virtual environment:

**Windows Command Prompt:**
```bash
venv\Scripts\activate
```

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting opencv-python>=4.8.0
Collecting numpy>=1.24.0
Collecting mediapipe>=0.10.0
...
Successfully installed opencv-python-4.8.x numpy-1.24.x mediapipe-0.10.x
```

#### Step 4: Verify Installation

Test if all packages are installed correctly:

```bash
python -c "import cv2; import numpy; import mediapipe; print('All packages installed successfully!')"
```

### Common Installation Issues

#### Issue 1: "pip is not recognized"

**Solution:**
- Make sure Python is added to PATH
- Use `python -m pip` instead of `pip`
- Reinstall Python with "Add to PATH" checked

#### Issue 2: "Microsoft Visual C++ 14.0 is required" (for some packages)

**Solution:**
- Install Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use pre-built wheels: `pip install --only-binary :all: package_name`

#### Issue 3: MediaPipe installation fails

**Solution:**
- Make sure you have Python 3.8-3.11 (MediaPipe doesn't support Python 3.12+ yet)
- Try: `pip install mediapipe --no-cache-dir`
- Alternative: Use conda: `conda install -c conda-forge mediapipe`

#### Issue 4: Camera not detected

**Solution:**
- Check if camera works in other apps (Camera app, Zoom, etc.)
- Try changing `CAMERA_INDEX` in `config.py` (try 0, 1, 2)
- Check Windows camera permissions

### Quick Test

After installation, test the system:

```bash
python main.py
```

You should see:
- Camera window opens
- Your face is detected
- EAR values displayed
- Status panel shows information

### Troubleshooting

If you encounter any issues:

1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be 3.8, 3.9, 3.10, or 3.11

2. **Check installed packages:**
   ```bash
   pip list
   ```
   Should show: opencv-python, numpy, mediapipe

3. **Test camera access:**
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   print(cap.isOpened())  # Should print True
   cap.release()
   ```

4. **Check for error messages:**
   - Read the full error message
   - Search for the error online
   - Check if all dependencies are installed

### Next Steps

Once installation is complete, proceed to run the application:

```bash
python main.py
```

See `README.md` for usage instructions.

