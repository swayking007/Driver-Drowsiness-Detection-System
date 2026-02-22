"""
Drowsiness Detection Module
Main logic for detecting driver drowsiness based on eye closure patterns
"""

import time
from collections import deque
from typing import Deque
import config
from utils.constants import STATUS_NORMAL, STATUS_DROWSY, STATUS_ALERT


class DrowsinessDetector:
    """
    Detects drowsiness based on eye closure duration and patterns
    """
    
    def __init__(self):
        """
        Initialize drowsiness detector
        """
        # Frame counter for consecutive eye closures
        self.eye_closed_counter = 0
        
        # Timer for drowsiness duration
        self.drowsy_start_time = None
        self.drowsy_duration = 0.0
        
        # Blink tracking
        self.blink_counter = 0
        self.last_blink_time = time.time()
        self.blink_times = deque(maxlen=30)  # Store last 30 blink times
        
        # EAR history for averaging
        self.ear_history = deque(maxlen=10)  # Store last 10 EAR values
        
        # Current status
        self.status = STATUS_NORMAL
        self.alert_triggered = False
        
        # Fatigue score (0-100)
        self.fatigue_score = 0.0
        self.last_update_time = time.time()
    
    def update(self, avg_ear: float, current_time: float = None) -> dict:
        """
        Update drowsiness detection based on current EAR value
        
        Args:
            avg_ear: Average Eye Aspect Ratio
            current_time: Current timestamp (if None, uses time.time())
        
        Returns:
            Dictionary with detection results
        """
        if current_time is None:
            current_time = time.time()
        
        # Add EAR to history
        if avg_ear > 0:
            self.ear_history.append(avg_ear)
        
        # Check if eyes are closed
        eyes_closed = avg_ear < config.EAR_THRESHOLD
        
        # Update eye closed counter
        if eyes_closed:
            self.eye_closed_counter += 1
        else:
            # Reset counter if eyes open
            if self.eye_closed_counter > 0:
                # Check if this was a blink
                if config.BLINK_CONSECUTIVE_FRAMES <= self.eye_closed_counter <= 10:
                    self._register_blink(current_time)
            self.eye_closed_counter = 0
            self.drowsy_start_time = None
            self.alert_triggered = False
        
        # Detect drowsiness
        drowsy = False
        if self.eye_closed_counter >= config.EAR_CONSECUTIVE_FRAMES:
            # Eyes have been closed for consecutive frames
            if self.drowsy_start_time is None:
                self.drowsy_start_time = current_time
            
            # Calculate drowsiness duration
            self.drowsy_duration = current_time - self.drowsy_start_time
            
            # Check if drowsy for too long
            if self.drowsy_duration >= config.DROWSY_TIME_THRESHOLD:
                drowsy = True
                self.status = STATUS_DROWSY
                
                # Trigger alert if not already triggered
                if not self.alert_triggered:
                    self.alert_triggered = True
        else:
            self.drowsy_duration = 0.0
            self.status = STATUS_NORMAL
        
        # Update fatigue score
        self._update_fatigue_score(drowsy, current_time)
        
        # Calculate blink rate
        blink_rate = self._calculate_blink_rate(current_time)
        
        # Additional drowsiness check: low blink rate
        if blink_rate < config.DROWSY_BLINK_RATE and len(self.blink_times) > 5:
            if self.status == STATUS_NORMAL:
                self.status = STATUS_DROWSY
        
        # Check average EAR
        if len(self.ear_history) >= 5:
            avg_ear_history = sum(self.ear_history) / len(self.ear_history)
            if avg_ear_history < config.DROWSY_EAR_AVERAGE:
                if self.status == STATUS_NORMAL:
                    self.status = STATUS_DROWSY
        
        return {
            'drowsy': drowsy,
            'status': self.status,
            'eye_closed_counter': self.eye_closed_counter,
            'drowsy_duration': self.drowsy_duration,
            'blink_count': self.blink_counter,
            'blink_rate': blink_rate,
            'fatigue_score': self.fatigue_score,
            'alert_triggered': self.alert_triggered
        }
    
    def _register_blink(self, current_time: float):
        """
        Register a blink event
        
        Args:
            current_time: Current timestamp
        """
        self.blink_counter += 1
        self.blink_times.append(current_time)
        self.last_blink_time = current_time
    
    def _calculate_blink_rate(self, current_time: float) -> float:
        """
        Calculate blink rate (blinks per second)
        
        Args:
            current_time: Current timestamp
        
        Returns:
            Blink rate in blinks per second
        """
        if len(self.blink_times) < 2:
            return 0.0
        
        # Calculate time window (last 10 seconds or all blinks if less)
        time_window = min(10.0, current_time - self.blink_times[0])
        
        if time_window <= 0:
            return 0.0
        
        # Count blinks in time window
        recent_blinks = [bt for bt in self.blink_times if current_time - bt <= time_window]
        
        if len(recent_blinks) < 2:
            return 0.0
        
        return len(recent_blinks) / time_window
    
    def _update_fatigue_score(self, drowsy: bool, current_time: float):
        """
        Update fatigue score based on drowsiness state
        
        Args:
            drowsy: Whether driver is currently drowsy
            current_time: Current timestamp
        """
        # Calculate time delta
        time_delta = current_time - self.last_update_time
        
        if drowsy:
            # Increase fatigue score
            self.fatigue_score += config.FATIGUE_INCREASE_RATE * time_delta
        else:
            # Decrease fatigue score
            self.fatigue_score -= config.FATIGUE_DECREASE_RATE * time_delta
        
        # Clamp fatigue score between 0 and max
        self.fatigue_score = max(0.0, min(config.FATIGUE_SCORE_MAX, self.fatigue_score))
        
        self.last_update_time = current_time
    
    def reset(self):
        """
        Reset all detection counters and timers
        """
        self.eye_closed_counter = 0
        self.drowsy_start_time = None
        self.drowsy_duration = 0.0
        self.blink_counter = 0
        self.blink_times.clear()
        self.ear_history.clear()
        self.status = STATUS_NORMAL
        self.alert_triggered = False
        self.fatigue_score = 0.0
        self.last_update_time = time.time()

