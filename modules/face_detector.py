"""
Face Detection Module using MediaPipe
Detects faces and extracts facial landmarks in real-time
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
import config


class FaceDetector:
    """
    Face detector using MediaPipe Face Mesh
    Detects face and extracts 468 facial landmarks
    """
    
    def __init__(self):
        """
        Initialize MediaPipe Face Mesh detector
        """
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,  # Process video frames
            max_num_faces=1,  # Only detect one face (driver)
            refine_landmarks=True,  # Get more detailed landmarks
            min_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
        )
        
        # Drawing utilities for landmarks
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Store face detection results
        self.face_detected = False
        self.landmarks = None
    
    def detect_face(self, frame: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Detect face and extract landmarks from frame
        
        Args:
            frame: Input video frame (BGR format)
        
        Returns:
            Tuple of (face_detected: bool, landmarks: List or None)
            landmarks is a list of (x, y) coordinates normalized to [0, 1]
        """
        # Convert BGR to RGB (MediaPipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.face_mesh.process(rgb_frame)
        
        # Check if face is detected
        if results.multi_face_landmarks:
            # Get the first face (we only track one face)
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract landmark coordinates
            h, w = frame.shape[:2]  # Frame height and width
            
            landmarks = []
            for landmark in face_landmarks.landmark:
                # Convert normalized coordinates to pixel coordinates
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                landmarks.append((x, y))
            
            self.face_detected = True
            self.landmarks = landmarks
            return True, landmarks
        else:
            self.face_detected = False
            self.landmarks = None
            return False, None
    
    def draw_landmarks(self, frame: np.ndarray, landmarks: Optional[List] = None) -> np.ndarray:
        """
        Draw facial landmarks on frame (optional visualization)
        
        Args:
            frame: Input frame to draw on
            landmarks: Landmarks to draw (if None, uses stored landmarks)
        
        Returns:
            Frame with landmarks drawn
        """
        if not config.SHOW_LANDMARKS:
            return frame
        
        # Convert frame to RGB for MediaPipe drawing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process to get MediaPipe format landmarks
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # Draw landmarks using MediaPipe's drawing utilities
            for face_landmarks in results.multi_face_landmarks:
                # Draw face mesh
                self.mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    self.mp_face_mesh.FACEMESH_CONTOURS,
                    None,  # Don't draw connections
                    self.mp_drawing_styles.get_default_face_mesh_contours_style()
                )
        
        return frame
    
    def get_face_bbox(self, landmarks: Optional[List] = None) -> Optional[Tuple[int, int, int, int]]:
        """
        Get bounding box around face
        
        Args:
            landmarks: Face landmarks (if None, uses stored landmarks)
        
        Returns:
            Tuple of (x, y, width, height) or None if no face
        """
        if landmarks is None:
            landmarks = self.landmarks
        
        if landmarks is None or len(landmarks) == 0:
            return None
        
        # Get min/max coordinates
        xs = [point[0] for point in landmarks]
        ys = [point[1] for point in landmarks]
        
        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)
        
        return (x_min, y_min, x_max - x_min, y_max - y_min)
    
    def release(self):
        """
        Release resources
        """
        if self.face_mesh:
            self.face_mesh.close()

