import cv2
import logging
import threading
import time

class CameraHandler:
    def __init__(self):
        """Initialize camera handler"""
        self.camera = None
        self.is_active = False
        self.frame = None
        self.lock = threading.Lock()
        logging.info("Camera handler initialized")
    
    def start(self):
        """Start the camera capture"""
        try:
            if self.camera is not None:
                self.camera.release()
            
            # Try different camera indices with timeout protection
            camera_found = False
            for camera_idx in [0, 1, 2]:
                try:
                    logging.info(f"Attempting to open camera {camera_idx}")
                    self.camera = cv2.VideoCapture(camera_idx)
                    if self.camera.isOpened():
                        # Test if we can actually read a frame
                        ret, test_frame = self.camera.read()
                        if ret and test_frame is not None:
                            logging.info(f"Camera opened successfully with index {camera_idx}")
                            camera_found = True
                            break
                        else:
                            logging.warning(f"Camera {camera_idx} opened but cannot read frames")
                    self.camera.release()
                    self.camera = None
                except Exception as e:
                    logging.warning(f"Error trying camera {camera_idx}: {e}")
                    if self.camera:
                        self.camera.release()
                        self.camera = None
            
            if not camera_found:
                logging.error("Failed to open any camera or no cameras available")
                return False
            
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_active = True
            
            # Start frame capture thread
            self.capture_thread = threading.Thread(target=self._capture_frames)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            logging.info("Camera started successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error starting camera: {e}")
            if self.camera:
                self.camera.release()
                self.camera = None
            return False
    
    def _capture_frames(self):
        """Continuous frame capture in a separate thread"""
        while self.is_active and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                with self.lock:
                    self.frame = frame
            else:
                logging.warning("Failed to capture frame")
                time.sleep(0.1)
    
    def get_frame(self):
        """Get the latest captured frame"""
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return self._generate_placeholder_frame()
    
    def _generate_placeholder_frame(self):
        """Generate a placeholder frame when no camera is available"""
        import numpy as np
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "No Camera Available", (180, 220), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Click 'Start Camera' to try again", (140, 260), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        cv2.putText(frame, "Demo Mode - Gesture Recognition Ready", (110, 300), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
        return frame
    
    def encode_frame(self, frame):
        """Encode frame as JPEG for streaming"""
        if frame is None:
            return False, None
        
        try:
            ret, buffer = cv2.imencode('.jpg', frame, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 80])
            return ret, buffer
        except Exception as e:
            logging.error(f"Error encoding frame: {e}")
            return False, None
    
    def stop(self):
        """Stop camera capture"""
        self.is_active = False
        
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join(timeout=2.0)
        
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        logging.info("Camera stopped")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop()
