/**
 * Main JavaScript file for Hand Gesture Recognition App
 * Handles camera controls, gesture updates, and UI interactions
 */

class GestureRecognitionApp {
    constructor() {
        this.isRunning = false;
        this.gestureUpdateInterval = null;
        this.initializeEventListeners();
        this.initializeGestureIcons();
        
        // Don't auto-start camera - wait for user to click
        // This prevents timeout issues in environments without cameras
    }

    initializeEventListeners() {
        // Camera control buttons
        document.getElementById('startCamera').addEventListener('click', () => {
            this.startCamera();
        });

        document.getElementById('stopCamera').addEventListener('click', () => {
            this.stopCamera();
        });

        // Handle video feed errors
        const videoFeed = document.getElementById('videoFeed');
        videoFeed.addEventListener('error', () => {
            this.handleVideoError();
        });

        videoFeed.addEventListener('load', () => {
            this.hideVideoOverlay();
        });
    }

    initializeGestureIcons() {
        this.gestureIcons = {
            'Open Palm': '<i class="fas fa-hand-paper fa-3x text-success"></i>',
            'Fist': '<i class="fas fa-fist-raised fa-3x text-danger"></i>',
            'Peace Sign': '<i class="fas fa-peace fa-3x text-info"></i>',
            'Thumbs Up': '<i class="fas fa-thumbs-up fa-3x text-warning"></i>',
            'No Hand Detected': '<i class="fas fa-hand-paper fa-3x text-muted"></i>',
            'Unknown Gesture': '<i class="fas fa-question fa-3x text-secondary"></i>'
        };
    }

    async startCamera() {
        try {
            this.showVideoOverlay('Starting camera...');
            
            const response = await fetch('/start_camera');
            const result = await response.json();
            
            if (result.success) {
                this.isRunning = true;
                this.updateCameraButtons();
                this.startGestureUpdates();
                
                // Hide overlay after a short delay to allow video to load
                setTimeout(() => {
                    this.hideVideoOverlay();
                }, 2000);
                
                this.showNotification('Camera started successfully', 'success');
            } else {
                throw new Error('Failed to start camera');
            }
        } catch (error) {
            console.error('Error starting camera:', error);
            this.showNotification('Failed to start camera. Please check camera permissions.', 'danger');
            this.hideVideoOverlay();
        }
    }

    async stopCamera() {
        try {
            const response = await fetch('/stop_camera');
            const result = await response.json();
            
            if (result.success) {
                this.isRunning = false;
                this.updateCameraButtons();
                this.stopGestureUpdates();
                this.resetGestureDisplay();
                this.showNotification('Camera stopped', 'info');
            }
        } catch (error) {
            console.error('Error stopping camera:', error);
            this.showNotification('Error stopping camera', 'warning');
        }
    }

    startGestureUpdates() {
        if (this.gestureUpdateInterval) {
            clearInterval(this.gestureUpdateInterval);
        }

        this.gestureUpdateInterval = setInterval(async () => {
            try {
                const response = await fetch('/gesture_info');
                const gestureData = await response.json();
                this.updateGestureDisplay(gestureData);
            } catch (error) {
                console.error('Error fetching gesture info:', error);
            }
        }, 100); // Update every 100ms for smooth real-time display
    }

    stopGestureUpdates() {
        if (this.gestureUpdateInterval) {
            clearInterval(this.gestureUpdateInterval);
            this.gestureUpdateInterval = null;
        }
    }

    updateGestureDisplay(gestureData) {
        const { gesture, confidence } = gestureData;
        
        // Update gesture name
        const gestureElement = document.getElementById('currentGesture');
        const gestureIconElement = document.getElementById('gestureIcon');
        
        if (gestureElement.textContent !== gesture) {
            gestureElement.textContent = gesture;
            gestureIconElement.innerHTML = this.gestureIcons[gesture] || this.gestureIcons['Unknown Gesture'];
            
            // Add pulse animation for gesture changes
            gestureIconElement.classList.add('gesture-detected');
            setTimeout(() => {
                gestureIconElement.classList.remove('gesture-detected');
            }, 500);
        }
        
        // Update confidence bar
        const confidencePercent = Math.round(confidence * 100);
        const confidenceBar = document.getElementById('confidenceBar');
        const confidenceText = document.getElementById('confidenceText');
        
        confidenceBar.style.width = `${confidencePercent}%`;
        confidenceText.textContent = `Confidence: ${confidencePercent}%`;
        
        // Update confidence bar color based on confidence level
        confidenceBar.className = 'progress-bar';
        if (confidencePercent >= 80) {
            confidenceBar.classList.add('bg-success');
        } else if (confidencePercent >= 60) {
            confidenceBar.classList.add('bg-warning');
        } else {
            confidenceBar.classList.add('bg-danger');
        }
    }

    resetGestureDisplay() {
        document.getElementById('currentGesture').textContent = 'No Hand Detected';
        document.getElementById('gestureIcon').innerHTML = this.gestureIcons['No Hand Detected'];
        document.getElementById('confidenceBar').style.width = '0%';
        document.getElementById('confidenceText').textContent = 'Confidence: 0%';
    }

    updateCameraButtons() {
        const startBtn = document.getElementById('startCamera');
        const stopBtn = document.getElementById('stopCamera');
        
        if (this.isRunning) {
            startBtn.disabled = true;
            startBtn.classList.add('disabled');
            stopBtn.disabled = false;
            stopBtn.classList.remove('disabled');
        } else {
            startBtn.disabled = false;
            startBtn.classList.remove('disabled');
            stopBtn.disabled = true;
            stopBtn.classList.add('disabled');
        }
    }

    showVideoOverlay(message = 'Loading...') {
        const overlay = document.getElementById('videoOverlay');
        if (overlay) {
            const messageElement = overlay.querySelector('h4');
            if (messageElement) {
                messageElement.textContent = message;
            }
            overlay.style.display = 'flex';
        }
    }

    hideVideoOverlay() {
        const overlay = document.getElementById('videoOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    handleVideoError() {
        this.showNotification('Video feed error. Please restart the camera.', 'danger');
        this.showVideoOverlay('Video feed error - Click Start Camera to retry');
    }

    showNotification(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gestureApp = new GestureRecognitionApp();
});

// Handle page visibility changes to manage camera resources
document.addEventListener('visibilitychange', () => {
    if (window.gestureApp) {
        if (document.hidden) {
            // Page is hidden, stop gesture updates to save resources
            window.gestureApp.stopGestureUpdates();
        } else if (window.gestureApp.isRunning) {
            // Page is visible again, restart gesture updates
            window.gestureApp.startGestureUpdates();
        }
    }
});

// Handle window unload to cleanup camera resources
window.addEventListener('beforeunload', () => {
    if (window.gestureApp && window.gestureApp.isRunning) {
        fetch('/stop_camera').catch(console.error);
    }
});
