import cv2
import mediapipe as mp
import numpy as np
import math
import logging

class GestureRecognizer:
    def __init__(self):
        """Initialize MediaPipe hands solution and gesture recognition"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.current_gesture = "No Hand Detected"
        self.gesture_confidence = 0.0
        
        # Gesture names
        self.gesture_names = {
            'open_palm': 'Open Palm',
            'fist': 'Fist',
            'peace': 'Peace Sign',
            'thumbs_up': 'Thumbs Up',
            'unknown': 'Unknown Gesture'
        }
        
        logging.info("Gesture recognizer initialized successfully")
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_finger_extended(self, landmarks, finger_tip, finger_pip, finger_mcp):
        """Check if a finger is extended by comparing tip position to pip and mcp"""
        tip_y = landmarks[finger_tip].y
        pip_y = landmarks[finger_pip].y
        mcp_y = landmarks[finger_mcp].y
        
        # For most fingers, extended means tip is above pip
        return tip_y < pip_y and tip_y < mcp_y
    
    def is_thumb_extended(self, landmarks):
        """Special case for thumb extension detection"""
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = landmarks[self.mp_hands.HandLandmark.THUMB_IP]
        thumb_mcp = landmarks[self.mp_hands.HandLandmark.THUMB_MCP]
        
        # Thumb is extended if tip is further from wrist than other joints
        return thumb_tip.x > thumb_ip.x and thumb_tip.x > thumb_mcp.x
    
    def get_finger_states(self, landmarks):
        """Get the state (extended/folded) of all fingers"""
        finger_states = {
            'thumb': self.is_thumb_extended(landmarks),
            'index': self.is_finger_extended(landmarks, 
                                           self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                           self.mp_hands.HandLandmark.INDEX_FINGER_PIP,
                                           self.mp_hands.HandLandmark.INDEX_FINGER_MCP),
            'middle': self.is_finger_extended(landmarks,
                                            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                            self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                                            self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
            'ring': self.is_finger_extended(landmarks,
                                          self.mp_hands.HandLandmark.RING_FINGER_TIP,
                                          self.mp_hands.HandLandmark.RING_FINGER_PIP,
                                          self.mp_hands.HandLandmark.RING_FINGER_MCP),
            'pinky': self.is_finger_extended(landmarks,
                                           self.mp_hands.HandLandmark.PINKY_TIP,
                                           self.mp_hands.HandLandmark.PINKY_PIP,
                                           self.mp_hands.HandLandmark.PINKY_MCP)
        }
        return finger_states
    
    def classify_gesture(self, landmarks):
        """Classify the gesture based on hand landmarks"""
        finger_states = self.get_finger_states(landmarks)
        
        # Count extended fingers
        extended_count = sum(finger_states.values())
        
        # Gesture classification logic
        if extended_count == 5:
            # All fingers extended - Open Palm
            return 'open_palm', 0.9
        
        elif extended_count == 0:
            # No fingers extended - Fist
            return 'fist', 0.9
        
        elif extended_count == 2 and finger_states['index'] and finger_states['middle']:
            # Index and middle finger extended - Peace Sign
            if not finger_states['thumb'] and not finger_states['ring'] and not finger_states['pinky']:
                return 'peace', 0.85
        
        elif extended_count == 1 and finger_states['thumb']:
            # Only thumb extended - Thumbs Up
            if not any([finger_states['index'], finger_states['middle'], 
                       finger_states['ring'], finger_states['pinky']]):
                return 'thumbs_up', 0.85
        
        # If no specific gesture matches
        return 'unknown', 0.5
    
    def process_frame(self, frame):
        """Process a frame and detect hand gestures"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Draw hand landmarks and classify gesture
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Classify gesture
                gesture_key, confidence = self.classify_gesture(hand_landmarks.landmark)
                self.current_gesture = self.gesture_names[gesture_key]
                self.gesture_confidence = confidence
                
                # Draw bounding box around hand
                h, w, _ = frame.shape
                x_coords = [landmark.x * w for landmark in hand_landmarks.landmark]
                y_coords = [landmark.y * h for landmark in hand_landmarks.landmark]
                
                x_min, x_max = int(min(x_coords)) - 20, int(max(x_coords)) + 20
                y_min, y_max = int(min(y_coords)) - 20, int(max(y_coords)) + 20
                
                # Draw bounding box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                
                # Draw gesture text
                cv2.putText(frame, f"Gesture: {self.current_gesture}", 
                           (x_min, y_min - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
                
                cv2.putText(frame, f"Confidence: {confidence:.2f}", 
                           (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 2)
        else:
            self.current_gesture = "No Hand Detected"
            self.gesture_confidence = 0.0
        
        # Add status text to frame
        cv2.putText(frame, f"Status: {self.current_gesture}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        gesture_info = {
            'gesture': self.current_gesture,
            'confidence': self.gesture_confidence
        }
        
        return frame, gesture_info
    
    def get_current_gesture(self):
        """Get the current gesture information"""
        return {
            'gesture': self.current_gesture,
            'confidence': self.gesture_confidence
        }
