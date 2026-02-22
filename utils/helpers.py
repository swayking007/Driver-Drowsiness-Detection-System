"""
Helper utility functions for common operations
"""

import cv2
import numpy as np
from typing import Tuple, List


def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1: (x, y) coordinates of first point
        point2: (x, y) coordinates of second point
    
    Returns:
        Distance between the two points
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_ear(eye_points: List[Tuple[float, float]]) -> float:
    """
    Calculate Eye Aspect Ratio (EAR)
    EAR = (vertical_distance_1 + vertical_distance_2) / (2 * horizontal_distance)
    
    Uses 6 points: left, right, top-left, top-right, bottom-left, bottom-right
    Or simplified 4 points: left, right, top, bottom
    
    Args:
        eye_points: List of eye landmark points
                   If 4 points: [left, right, top, bottom]
                   If 6 points: [left, right, top-left, top-right, bottom-left, bottom-right]
    
    Returns:
        Eye Aspect Ratio value
    """
    if len(eye_points) < 4:
        return 0.0
    
    # If we have 6 points (full eye contour)
    if len(eye_points) >= 6:
        # Extract points
        left = eye_points[0]
        right = eye_points[1]
        top_left = eye_points[2]
        top_right = eye_points[3]
        bottom_left = eye_points[4]
        bottom_right = eye_points[5]
        
        # Calculate vertical distances (average of left and right vertical distances)
        vertical_dist_1 = calculate_distance(top_left, bottom_left)
        vertical_dist_2 = calculate_distance(top_right, bottom_right)
        
        # Calculate horizontal distance
        horizontal_dist = calculate_distance(left, right)
    else:
        # Simplified 4-point calculation
        left_point = eye_points[0]
        right_point = eye_points[1]
        top_point = eye_points[2]
        bottom_point = eye_points[3]
        
        # Calculate vertical distances
        vertical_dist_1 = calculate_distance(top_point, bottom_point)
        vertical_dist_2 = calculate_distance(top_point, bottom_point)  # Same for simplified
        
        # Calculate horizontal distance
        horizontal_dist = calculate_distance(left_point, right_point)
    
    # Avoid division by zero
    if horizontal_dist == 0:
        return 0.0
    
    # Calculate EAR
    ear = (vertical_dist_1 + vertical_dist_2) / (2.0 * horizontal_dist)
    return ear


def draw_text_with_background(img, text: str, position: Tuple[int, int], 
                              font_scale: float = 0.7, 
                              text_color: Tuple[int, int, int] = (255, 255, 255),
                              bg_color: Tuple[int, int, int] = (0, 0, 0),
                              thickness: int = 2) -> None:
    """
    Draw text with a background rectangle for better visibility
    
    Args:
        img: Image to draw on
        text: Text string to display
        position: (x, y) position of text
        font_scale: Font size multiplier
        text_color: Text color (BGR)
        bg_color: Background color (BGR)
        thickness: Text thickness
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get text size to create background rectangle
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle
    cv2.rectangle(img, 
                  (position[0] - 5, position[1] - text_height - 5),
                  (position[0] + text_width + 5, position[1] + baseline + 5),
                  bg_color, -1)
    
    # Draw text
    cv2.putText(img, text, position, font, font_scale, text_color, thickness, cv2.LINE_AA)


def resize_frame(frame, width: int = None, height: int = None) -> np.ndarray:
    """
    Resize frame while maintaining aspect ratio
    
    Args:
        frame: Input frame
        width: Target width (optional)
        height: Target height (optional)
    
    Returns:
        Resized frame
    """
    if width is None and height is None:
        return frame
    
    h, w = frame.shape[:2]
    
    if width is None:
        # Calculate width based on height
        aspect_ratio = w / h
        width = int(height * aspect_ratio)
    elif height is None:
        # Calculate height based on width
        aspect_ratio = h / w
        height = int(width * aspect_ratio)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

