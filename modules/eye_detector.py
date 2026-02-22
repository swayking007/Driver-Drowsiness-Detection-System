"""
Eye Detection Module
Extracts eye landmarks and calculates Eye Aspect Ratio (EAR)
"""

import numpy as np
from typing import List, Tuple, Optional
from utils.constants import LEFT_EYE_SIMPLE, RIGHT_EYE_SIMPLE, LEFT_EYE_4PT, RIGHT_EYE_4PT
from utils.helpers import calculate_ear
import config


class EyeDetector:
    """
    Eye detector that extracts eye landmarks and calculates EAR
    """
    
    def __init__(self):
        """
        Initialize eye detector
        """
        # Eye landmark indices from MediaPipe (6-point version for accuracy)
        self.left_eye_indices = LEFT_EYE_SIMPLE
        self.right_eye_indices = RIGHT_EYE_SIMPLE
        
        # Store current EAR values
        self.left_ear = 0.0
        self.right_ear = 0.0
        self.avg_ear = 0.0
    
    def extract_eye_landmarks(self, face_landmarks: List[Tuple[int, int]]) -> Tuple[Optional[List], Optional[List]]:
        """
        Extract eye landmark points from face landmarks
        
        Args:
            face_landmarks: List of all face landmark coordinates
        
        Returns:
            Tuple of (left_eye_points, right_eye_points)
            Each is a list of (x, y) coordinates (6 points for better accuracy)
        """
        if face_landmarks is None or len(face_landmarks) < 468:
            return None, None
        
        # Extract left eye points (6 key points for accurate EAR)
        left_eye_points = []
        for idx in self.left_eye_indices:
            if idx < len(face_landmarks):
                left_eye_points.append(face_landmarks[idx])
        
        # Extract right eye points (6 key points for accurate EAR)
        right_eye_points = []
        for idx in self.right_eye_indices:
            if idx < len(face_landmarks):
                right_eye_points.append(face_landmarks[idx])
        
        return left_eye_points, right_eye_points
    
    def calculate_ear(self, face_landmarks: List[Tuple[int, int]]) -> Tuple[float, float, float]:
        """
        Calculate Eye Aspect Ratio for both eyes
        
        EAR Formula:
        EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        Where p1-p6 are eye landmark points
        
        Args:
            face_landmarks: List of all face landmark coordinates
        
        Returns:
            Tuple of (left_ear, right_ear, average_ear)
        """
        # Extract eye points
        left_eye_points, right_eye_points = self.extract_eye_landmarks(face_landmarks)
        
        # Calculate left eye EAR (works with 4 or 6 points)
        if left_eye_points and len(left_eye_points) >= 4:
            self.left_ear = calculate_ear(left_eye_points)
        else:
            self.left_ear = 0.0
        
        # Calculate right eye EAR (works with 4 or 6 points)
        if right_eye_points and len(right_eye_points) >= 4:
            self.right_ear = calculate_ear(right_eye_points)
        else:
            self.right_ear = 0.0
        
        # Calculate average EAR
        if self.left_ear > 0 and self.right_ear > 0:
            self.avg_ear = (self.left_ear + self.right_ear) / 2.0
        else:
            self.avg_ear = 0.0
        
        return self.left_ear, self.right_ear, self.avg_ear
    
    def is_eye_closed(self, ear: float = None) -> bool:
        """
        Check if eye is closed based on EAR threshold
        
        Args:
            ear: Eye Aspect Ratio (if None, uses average EAR)
        
        Returns:
            True if eye is closed, False otherwise
        """
        if ear is None:
            ear = self.avg_ear
        
        # Eye is closed if EAR is below threshold
        return ear < config.EAR_THRESHOLD
    
    def get_eye_status(self) -> dict:
        """
        Get current eye status information
        
        Returns:
            Dictionary with eye status data
        """
        return {
            'left_ear': self.left_ear,
            'right_ear': self.right_ear,
            'avg_ear': self.avg_ear,
            'left_closed': self.is_eye_closed(self.left_ear),
            'right_closed': self.is_eye_closed(self.right_ear),
            'both_closed': self.is_eye_closed()
        }

