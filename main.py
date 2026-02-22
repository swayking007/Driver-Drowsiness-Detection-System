"""
Driver Drowsiness Detection System - Main Application
Real-time drowsiness detection using webcam and computer vision
"""

import cv2
import time
import sys
from typing import Optional

# Import configuration
import config

# Import modules
from modules.face_detector import FaceDetector
from modules.eye_detector import EyeDetector
from modules.drowsiness_detector import DrowsinessDetector
from modules.alert_system import AlertSystem

# Import utilities
from utils.helpers import draw_text_with_background
from utils.constants import COLOR_GREEN, COLOR_RED, COLOR_WHITE


class DriverDrowsinessSystem:
    """
    Main application class for driver drowsiness detection
    """
    
    def __init__(self):
        """
        Initialize the drowsiness detection system
        """
        # Initialize camera
        self.cap = None
        
        # Initialize detection modules
        self.face_detector = FaceDetector()
        self.eye_detector = EyeDetector()
        self.drowsiness_detector = DrowsinessDetector()
        self.alert_system = AlertSystem()
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0.0
        
        # System state
        self.running = False
    
    def initialize_camera(self) -> bool:
        """
        Initialize webcam capture
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        print("Initializing camera...")
        
        try:
            # Open camera
            self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
            
            if not self.cap.isOpened():
                print(f"ERROR: Could not open camera {config.CAMERA_INDEX}")
                print("Trying to open default camera...")
                self.cap = cv2.VideoCapture(0)
                
                if not self.cap.isOpened():
                    print("ERROR: No camera found!")
                    return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, config.FPS)
            
            # Get actual camera properties
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"Camera initialized successfully!")
            print(f"  Resolution: {actual_width}x{actual_height}")
            print(f"  FPS: {actual_fps}")
            
            return True
            
        except Exception as e:
            print(f"ERROR initializing camera: {e}")
            return False
    
    def update_fps(self):
        """
        Update FPS counter
        """
        self.fps_counter += 1
        current_time = time.time()
        elapsed = current_time - self.fps_start_time
        
        # Update FPS every second
        if elapsed >= 1.0:
            self.current_fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def process_frame(self, frame) -> Optional[dict]:
        """
        Process a single video frame
        
        Args:
            frame: Input video frame
        
        Returns:
            Dictionary with detection results or None
        """
        # Detect face and get landmarks
        face_detected, landmarks = self.face_detector.detect_face(frame)
        
        if not face_detected or landmarks is None:
            # No face detected
            return {
                'face_detected': False,
                'status': 'NO_FACE',
                'message': 'No face detected - Please position yourself in front of camera'
            }
        
        # Calculate Eye Aspect Ratio
        left_ear, right_ear, avg_ear = self.eye_detector.calculate_ear(landmarks)
        
        # Update drowsiness detection
        current_time = time.time()
        drowsiness_data = self.drowsiness_detector.update(avg_ear, current_time)
        
        # Get eye status
        eye_status = self.eye_detector.get_eye_status()
        
        # Combine all data
        result = {
            'face_detected': True,
            'landmarks': landmarks,
            'left_ear': left_ear,
            'right_ear': right_ear,
            'avg_ear': avg_ear,
            'status': drowsiness_data['status'],
            'drowsy': drowsiness_data['drowsy'],
            'drowsy_duration': drowsiness_data['drowsy_duration'],
            'blink_count': drowsiness_data['blink_count'],
            'blink_rate': drowsiness_data['blink_rate'],
            'fatigue_score': drowsiness_data['fatigue_score'],
            'alert_triggered': drowsiness_data['alert_triggered'],
            'eye_status': eye_status
        }
        
        return result
    
    def draw_frame(self, frame, result: dict) -> None:
        """
        Draw detection results on frame
        
        Args:
            frame: Video frame to draw on
            result: Detection results dictionary
        """
        h, w = frame.shape[:2]
        
        # Draw face landmarks (optional)
        if config.SHOW_LANDMARKS and result.get('face_detected'):
            frame = self.face_detector.draw_landmarks(frame)
        
        # Draw eye information
        if result.get('face_detected'):
            # Draw EAR values
            avg_ear = result.get('avg_ear', 0.0)
            left_ear = result.get('left_ear', 0.0)
            right_ear = result.get('right_ear', 0.0)
            
            # EAR text color (green if above threshold, red if below)
            ear_color = COLOR_GREEN if avg_ear >= config.EAR_THRESHOLD else COLOR_RED
            
            draw_text_with_background(
                frame,
                f"EAR: {avg_ear:.3f}",
                (10, 30),
                font_scale=0.7,
                text_color=COLOR_WHITE,
                bg_color=ear_color
            )
            
            draw_text_with_background(
                frame,
                f"L: {left_ear:.3f}  R: {right_ear:.3f}",
                (10, 60),
                font_scale=0.6,
                text_color=COLOR_WHITE,
                bg_color=(50, 50, 50)
            )
        
        # Draw status message
        if not result.get('face_detected'):
            message = result.get('message', 'No face detected')
            draw_text_with_background(
                frame,
                message,
                (w // 2 - 200, h // 2),
                font_scale=0.8,
                text_color=COLOR_WHITE,
                bg_color=COLOR_RED
            )
        
        # Draw alert if drowsy
        if result.get('drowsy', False):
            drowsy_duration = result.get('drowsy_duration', 0.0)
            frame = self.alert_system.trigger_alert(frame, drowsy_duration)
        
        # Draw status panel
        frame = self.alert_system.draw_status_panel(frame, result)
        
        # Draw FPS
        if config.SHOW_FPS:
            draw_text_with_background(
                frame,
                f"FPS: {self.current_fps:.1f}",
                (10, h - 30),
                font_scale=0.6,
                text_color=COLOR_WHITE,
                bg_color=(0, 0, 0)
            )
        
        # Draw instructions
        draw_text_with_background(
            frame,
            "Press 'q' to quit",
            (10, h - 60),
            font_scale=0.5,
            text_color=COLOR_WHITE,
            bg_color=(0, 0, 0)
        )
    
    def run(self):
        """
        Main application loop
        """
        print("\n" + "="*50)
        print("Driver Drowsiness Detection System")
        print("="*50)
        print("\nStarting system...")
        
        # Initialize camera
        if not self.initialize_camera():
            print("\nERROR: Failed to initialize camera!")
            print("Please check:")
            print("  1. Camera is connected")
            print("  2. No other application is using the camera")
            print("  3. Camera permissions are granted")
            return
        
        print("\nSystem ready! Starting video feed...")
        print("Instructions:")
        print("  - Position yourself in front of the camera")
        print("  - Keep your face visible")
        print("  - Close your eyes for 2+ seconds to test alert")
        print("  - Press 'q' to quit\n")
        
        self.running = True
        
        try:
            while self.running:
                # Read frame from camera
                ret, frame = self.cap.read()
                
                if not ret:
                    print("ERROR: Could not read frame from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                result = self.process_frame(frame)
                
                if result is None:
                    continue
                
                # Draw results on frame
                self.draw_frame(frame, result)
                
                # Update FPS
                self.update_fps()
                
                # Display frame
                cv2.imshow('Driver Drowsiness Detection', frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\nQuitting...")
                    break
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        except Exception as e:
            print(f"\nERROR during execution: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """
        Cleanup resources
        """
        print("\nCleaning up...")
        
        if self.cap is not None:
            self.cap.release()
        
        self.face_detector.release()
        cv2.destroyAllWindows()
        
        print("Cleanup complete. Goodbye!")


def main():
    """
    Main entry point
    """
    # Create and run system
    system = DriverDrowsinessSystem()
    system.run()


if __name__ == "__main__":
    main()
