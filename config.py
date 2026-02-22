"""
Configuration file for Driver Drowsiness Detection System
Contains all adjustable parameters and thresholds
"""

# ============================================
# CAMERA SETTINGS
# ============================================
CAMERA_INDEX = 0  # Default webcam (0 = first camera, 1 = second, etc.)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# ============================================
# DROWSINESS DETECTION THRESHOLDS
# ============================================

# Eye Aspect Ratio (EAR) thresholds
# Lower values = more closed eyes
EAR_THRESHOLD = 0.25  # Below this = eye closed
EAR_CONSECUTIVE_FRAMES = 3  # Frames to wait before confirming eye closure

# Blink detection
BLINK_THRESHOLD = 0.25  # EAR below this = blink
BLINK_CONSECUTIVE_FRAMES = 2  # Minimum frames for a valid blink

# Drowsiness detection
DROWSY_BLINK_RATE = 0.2  # Blinks per second (too low = drowsy)
DROWSY_EAR_AVERAGE = 0.20  # Average EAR below this = drowsy
DROWSY_TIME_THRESHOLD = 2.0  # Seconds of drowsiness before alert

# ============================================
# HEAD POSE DETECTION
# ============================================
HEAD_TILT_THRESHOLD = 15  # Degrees - tilt beyond this = distracted
HEAD_POSE_CONSECUTIVE_FRAMES = 10  # Frames to confirm head tilt

# ============================================
# FATIGUE SCORING
# ============================================
FATIGUE_SCORE_MAX = 100  # Maximum fatigue score
FATIGUE_INCREASE_RATE = 0.5  # Score increase per second when drowsy
FATIGUE_DECREASE_RATE = 0.2  # Score decrease per second when alert

# ============================================
# ALERT SETTINGS
# ============================================
ALERT_SOUND_ENABLED = True
ALERT_SOUND_FILE = "alert.wav"  # Path to alert sound file
ALERT_COLOR = (0, 0, 255)  # BGR format (Red in this case)
ALERT_TEXT_COLOR = (255, 255, 255)  # White text

# ============================================
# DISPLAY SETTINGS
# ============================================
SHOW_FPS = True
SHOW_LANDMARKS = True  # Show face landmarks on video
SHOW_STATUS_PANEL = True
PANEL_WIDTH = 300
PANEL_HEIGHT = 200

# ============================================
# MEDIAPIPE SETTINGS
# ============================================
MEDIAPIPE_MODEL_COMPLEXITY = 1  # 0, 1, or 2 (higher = more accurate, slower)
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5

