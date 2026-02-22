"""
Alert System Module
Handles visual and audio alerts when drowsiness is detected
"""

import cv2
import numpy as np
import time
import winsound 
 # Windows built-in sound module
from typing import Tuple
import config
from utils.constants import COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_WHITE


class AlertSystem:
    """
    Manages alerts and notifications for drowsiness detection
    """
    
    def __init__(self):
        """
        Initialize alert system
        """
        self.alert_active = False
        self.last_alert_time = 0
        self.alert_interval = 1.0  # Alert every 1 second when drowsy
        self.beep_duration = 5000  # Beep duration in milliseconds
    
    def trigger_alert(self, frame: np.ndarray, drowsy_duration: float) -> np.ndarray:
        """
        Trigger visual and audio alert
        
        Args:
            frame: Video frame to draw alert on
            drowsy_duration: How long driver has been drowsy (seconds)
        
        Returns:
            Frame with alert overlay
        """
        current_time = time.time()
        
        # Check if it's time to alert again
        if current_time - self.last_alert_time >= self.alert_interval:
            # Play beep sound
            if config.ALERT_SOUND_ENABLED:
                try:
                    # Windows beep: frequency (Hz), duration (ms)
                    winsound.Beep(1000, self.beep_duration)  # 1000 Hz, 500ms
                except Exception as e:
                    print(f"Could not play alert sound: {e}")
            
            self.last_alert_time = current_time
        
        # Draw visual alert
        frame = self._draw_visual_alert(frame, drowsy_duration)
        
        self.alert_active = True
        return frame
    
    def _draw_visual_alert(self, frame: np.ndarray, drowsy_duration: float) -> np.ndarray:
        """
        Draw visual alert overlay on frame
        
        Args:
            frame: Video frame
            drowsy_duration: Drowsiness duration
        
        Returns:
            Frame with alert overlay
        """
        h, w = frame.shape[:2]
        
        # Draw red overlay (semi-transparent)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), COLOR_RED, -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw alert text
        alert_text = "ALERT! DROWSINESS DETECTED!"
        warning_text = f"Eyes closed for {drowsy_duration:.1f}s"
        
        # Calculate text positions (center of frame)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 3
        
        # Get text sizes
        (alert_w, alert_h), _ = cv2.getTextSize(alert_text, font, font_scale, thickness)
        (warn_w, warn_h), _ = cv2.getTextSize(warning_text, font, 0.8, 2)
        
        # Center positions
        alert_x = (w - alert_w) // 2
        alert_y = h // 2 - 20
        warn_x = (w - warn_w) // 2
        warn_y = h // 2 + 40
        
        # Draw background rectangles for text
        cv2.rectangle(frame, 
                     (alert_x - 10, alert_y - alert_h - 10),
                     (alert_x + alert_w + 10, alert_y + 10),
                     COLOR_RED, -1)
        
        cv2.rectangle(frame,
                     (warn_x - 10, warn_y - warn_h - 10),
                     (warn_x + warn_w + 10, warn_y + 10),
                     (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(frame, alert_text, (alert_x, alert_y),
                   font, font_scale, COLOR_WHITE, thickness, cv2.LINE_AA)
        
        cv2.putText(frame, warning_text, (warn_x, warn_y),
                   font, 0.8, COLOR_WHITE, 2, cv2.LINE_AA)
        
        return frame
    
    def draw_status_panel(self, frame: np.ndarray, status_data: dict) -> np.ndarray:
        """
        Draw status information panel on frame
        
        Args:
            frame: Video frame
            status_data: Dictionary with status information
        
        Returns:
            Frame with status panel
        """
        if not config.SHOW_STATUS_PANEL:
            return frame
        
        h, w = frame.shape[:2]
        panel_w = config.PANEL_WIDTH
        panel_h = config.PANEL_HEIGHT
        
        # Panel position (top-right corner)
        panel_x = w - panel_w - 10
        panel_y = 10
        
        # Draw panel background
        overlay = frame.copy()
        cv2.rectangle(overlay, 
                     (panel_x, panel_y),
                     (panel_x + panel_w, panel_y + panel_h),
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw border
        cv2.rectangle(frame,
                     (panel_x, panel_y),
                     (panel_x + panel_w, panel_y + panel_h),
                     COLOR_WHITE, 2)
        
        # Status text
        y_offset = 30
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 1
        line_height = 25
        
        # Status
        status = status_data.get('status', 'NORMAL')
        status_color = COLOR_GREEN if status == 'NORMAL' else COLOR_RED
        cv2.putText(frame, f"Status: {status}", 
                   (panel_x + 10, panel_y + y_offset),
                   font, font_scale, status_color, thickness, cv2.LINE_AA)
        y_offset += line_height
        
        # EAR value
        avg_ear = status_data.get('avg_ear', 0.0)
        cv2.putText(frame, f"EAR: {avg_ear:.3f}", 
                   (panel_x + 10, panel_y + y_offset),
                   font, font_scale, COLOR_WHITE, thickness, cv2.LINE_AA)
        y_offset += line_height
        
        # Blink count
        blink_count = status_data.get('blink_count', 0)
        cv2.putText(frame, f"Blinks: {blink_count}", 
                   (panel_x + 10, panel_y + y_offset),
                   font, font_scale, COLOR_WHITE, thickness, cv2.LINE_AA)
        y_offset += line_height
        
        # Fatigue score
        fatigue = status_data.get('fatigue_score', 0.0)
        fatigue_color = COLOR_GREEN if fatigue < 50 else COLOR_YELLOW if fatigue < 75 else COLOR_RED
        cv2.putText(frame, f"Fatigue: {fatigue:.0f}/100", 
                   (panel_x + 10, panel_y + y_offset),
                   font, font_scale, fatigue_color, thickness, cv2.LINE_AA)
        y_offset += line_height
        
        # Drowsy duration
        if status_data.get('drowsy', False):
            drowsy_dur = status_data.get('drowsy_duration', 0.0)
            cv2.putText(frame, f"Drowsy: {drowsy_dur:.1f}s", 
                       (panel_x + 10, panel_y + y_offset),
                       font, font_scale, COLOR_RED, thickness, cv2.LINE_AA)
        
        return frame
    
    def reset(self):
        """
        Reset alert system
        """
        self.alert_active = False
        self.last_alert_time = 0

