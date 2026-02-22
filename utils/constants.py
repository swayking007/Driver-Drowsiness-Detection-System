"""
Constants used throughout the application
Mathematical and geometric constants for calculations
"""

# ============================================
# FACE LANDMARK INDICES (MediaPipe)
# ============================================
# MediaPipe Face Mesh has 468 landmarks
# These are the indices for key facial features

# Left eye landmarks (MediaPipe uses 6 points per eye)
LEFT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
# Right eye landmarks
RIGHT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

# Simplified eye points for EAR calculation (MediaPipe Face Mesh indices)
# Using 6 points for more accurate EAR: left, right, top-left, top-right, bottom-left, bottom-right
LEFT_EYE_SIMPLE = [33, 133, 160, 158, 153, 144]  # Left, right, top-left, top-right, bottom-left, bottom-right
RIGHT_EYE_SIMPLE = [362, 263, 387, 385, 373, 380]  # Left, right, top-left, top-right, bottom-left, bottom-right

# Alternative 4-point version (simpler but less accurate)
LEFT_EYE_4PT = [33, 133, 159, 145]  # Left, right, top, bottom
RIGHT_EYE_4PT = [362, 263, 386, 374]  # Left, right, top, bottom

# Nose tip (for head pose estimation)
NOSE_TIP = 4

# Face outline points (for bounding box)
FACE_OUTLINE = [10, 151, 9, 175, 18, 200, 199, 175]

# ============================================
# GEOMETRIC CONSTANTS
# ============================================
PI = 3.14159265359
DEGREES_TO_RADIANS = PI / 180.0
RADIANS_TO_DEGREES = 180.0 / PI

# ============================================
# COLOR CONSTANTS (BGR format for OpenCV)
# ============================================
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# ============================================
# STATUS CONSTANTS
# ============================================
STATUS_ALERT = "ALERT"
STATUS_DROWSY = "DROWSY"
STATUS_DISTRACTED = "DISTRACTED"
STATUS_NORMAL = "NORMAL"

