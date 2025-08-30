# Real-Time Hand Gesture Recognition System

A Flask-based web application that performs real-time static hand gesture recognition using MediaPipe and computer vision techniques.

## Author
AI Intern Assessment Submission - Hand Gesture Recognition System

## Overview

This application uses a webcam to detect and classify static hand gestures in real-time. It can recognize four distinct gestures: Open Palm, Fist, Peace Sign (V-sign), and Thumbs Up. The system provides visual feedback with bounding boxes around detected hands and displays the recognized gesture name with confidence scores.

## Technology Stack & Justification

### Backend Technologies

**MediaPipe** - Primary choice for hand detection and landmark extraction
- **Justification**: MediaPipe offers state-of-the-art hand detection with 21 landmark points per hand. It's optimized for real-time performance and provides accurate hand tracking even in varying lighting conditions. The pre-trained models eliminate the need for custom training data.
- **Advantages**: 
  - Real-time performance (30+ FPS)
  - Accurate hand landmark detection
  - Cross-platform compatibility
  - No custom training required

**OpenCV (cv2)** - Video processing and image manipulation
- **Justification**: Industry-standard computer vision library that provides efficient video capture, frame processing, and image encoding capabilities.
- **Use cases**: Webcam integration, frame manipulation, video streaming

**Flask** - Web framework for real-time streaming
- **Justification**: Lightweight framework perfect for creating streaming applications with minimal overhead. Provides easy routing for video feeds and API endpoints.

**NumPy** - Mathematical operations for gesture classification
- **Justification**: Essential for efficient numerical computations on landmark coordinates and distance calculations.

### Frontend Technologies

**Bootstrap 5** - Responsive UI framework
- **Justification**: Provides a professional, mobile-responsive interface with minimal custom CSS required.

**Vanilla JavaScript** - Real-time UI updates
- **Justification**: Handles camera controls, gesture status updates, and user interactions without additional framework overhead.

## Gesture Recognition Methodology

### Hand Detection Process
1. **Video Capture**: Real-time video stream from webcam using OpenCV
2. **Hand Detection**: MediaPipe detects hands and extracts 21 landmark points
3. **Landmark Analysis**: Extract 3D coordinates for each finger joint and palm
4. **Gesture Classification**: Rules-based algorithm analyzes finger positions

### Gesture Classification Logic

The system uses a rules-based approach analyzing finger extension states:

#### 1. Open Palm
- **Logic**: All five fingers are extended
- **Detection Method**: Compare finger tip positions with PIP (Proximal Interphalangeal) joints
- **Confidence**: High (0.9) when all fingers clearly extended

#### 2. Fist
- **Logic**: All fingers are folded/closed
- **Detection Method**: All finger tips below their respective PIP joints
- **Confidence**: High (0.9) when no fingers extended

#### 3. Peace Sign (V-sign)
- **Logic**: Only index and middle fingers extended
- **Detection Method**: Index and middle finger tips above PIP joints, other fingers folded
- **Confidence**: Medium-High (0.85) due to finger occlusion possibilities

#### 4. Thumbs Up
- **Logic**: Only thumb extended horizontally
- **Detection Method**: Thumb tip positioned further from wrist than other thumb joints, all other fingers folded
- **Confidence**: Medium-High (0.85) due to thumb orientation sensitivity

### Technical Implementation Details

**Finger Extension Detection**:
```python
def is_finger_extended(landmarks, finger_tip, finger_pip, finger_mcp):
    tip_y = landmarks[finger_tip].y
    pip_y = landmarks[finger_pip].y
    mcp_y = landmarks[finger_mcp].y
    return tip_y < pip_y and tip_y < mcp_y
