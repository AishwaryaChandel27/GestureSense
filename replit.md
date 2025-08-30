# Real-Time Hand Gesture Recognition System

## Overview

This is a Flask-based web application that performs real-time static hand gesture recognition using MediaPipe and computer vision. The system uses a webcam to detect and classify four distinct hand gestures: Open Palm, Fist, Peace Sign (V-sign), and Thumbs Up. It provides a live video feed with real-time gesture detection overlay and a responsive web interface for user interaction.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Single Page Application**: Uses vanilla HTML, CSS, and JavaScript with Bootstrap 5 for responsive design
- **Real-time Video Streaming**: Displays live video feed from Flask backend using multipart HTTP streaming
- **Dynamic UI Updates**: JavaScript handles camera controls, gesture status updates, and user interactions
- **Responsive Design**: Bootstrap-based layout that works across desktop and mobile devices

### Backend Architecture
- **Flask Web Framework**: Lightweight Python web server handling HTTP routes and video streaming
- **Modular Design**: Separated into distinct components:
  - `app.py` - Main Flask application with routing
  - `camera_handler.py` - Camera capture and frame management
  - `gesture_recognizer.py` - MediaPipe-based gesture detection and classification
  - `main.py` - Application entry point
- **Threading Model**: Uses background threads for continuous video capture to maintain real-time performance
- **RESTful API**: JSON endpoints for gesture information retrieval

### Computer Vision Pipeline
- **MediaPipe Integration**: Google's MediaPipe library for hand detection and 21-point landmark extraction
- **OpenCV Processing**: Video capture, frame manipulation, and image encoding
- **Rules-based Classification**: Algorithmic gesture recognition using finger position analysis rather than machine learning models
- **Real-time Performance**: Optimized for 30+ FPS processing with minimal latency

### Data Processing
- **NumPy Calculations**: Mathematical operations for landmark coordinate analysis and distance calculations
- **Frame Encoding**: JPEG compression for efficient video streaming over HTTP
- **Gesture State Management**: Thread-safe storage of current gesture information

## External Dependencies

### Core Libraries
- **MediaPipe**: Google's machine learning framework for hand detection and landmark extraction
- **OpenCV (cv2)**: Computer vision library for video capture and image processing
- **Flask**: Python web framework for HTTP server and routing
- **NumPy**: Mathematical computing library for coordinate calculations

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded from CDN for responsive UI components
- **Font Awesome 6**: Icon library loaded from CDN for gesture visualization and UI elements

### System Requirements
- **Webcam Access**: Requires camera permissions and hardware for video input
- **Python Runtime**: Backend requires Python environment with computer vision libraries
- **Web Browser**: Modern browser with support for multipart streaming and webcam access