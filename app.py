import os
import logging
import time
from flask import Flask, render_template, Response, jsonify
from camera_handler import CameraHandler
from gesture_recognizer import GestureRecognizer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "hand-gesture-recognition-secret-key")

# Initialize camera handler and gesture recognizer
camera_handler = CameraHandler()
gesture_recognizer = GestureRecognizer()

@app.route('/')
def index():
    """Main page with video feed and gesture recognition interface"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag"""
    def generate():
        frame_count = 0
        while frame_count < 100:  # Limit frames to prevent infinite loops
            try:
                frame = camera_handler.get_frame()
                if frame is not None:
                    # Process frame for gesture recognition
                    processed_frame, gesture_info = gesture_recognizer.process_frame(frame)
                    
                    # Encode frame as JPEG
                    ret, buffer = camera_handler.encode_frame(processed_frame)
                    if ret and buffer is not None:
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                        time.sleep(0.03)  # ~30 FPS
                    else:
                        # Send placeholder frame if encoding fails
                        yield (b'--frame\r\n'
                               b'Content-Type: text/plain\r\n\r\n' + b'Camera Error\r\n')
                        break
                else:
                    # Send placeholder when no frame available
                    yield (b'--frame\r\n'
                           b'Content-Type: text/plain\r\n\r\n' + b'No Camera Feed\r\n')
                    break
                frame_count += 1
            except Exception as e:
                logging.error(f"Error in video feed generation: {e}")
                yield (b'--frame\r\n'
                       b'Content-Type: text/plain\r\n\r\n' + b'Camera Error\r\n')
                break
    
    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_info')
def gesture_info():
    """API endpoint to get current gesture information"""
    gesture_data = gesture_recognizer.get_current_gesture()
    return jsonify(gesture_data)

@app.route('/start_camera')
def start_camera():
    """Start the camera"""
    success = camera_handler.start()
    return jsonify({'success': success})

@app.route('/stop_camera')
def stop_camera():
    """Stop the camera"""
    camera_handler.stop()
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
