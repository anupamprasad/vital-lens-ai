"""
Face Detection Module - MediaPipe Implementation
Vital Lens AI Phase 2
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class FaceDetectionResult:
    """Result from face detection"""
    bbox: Optional[np.ndarray]  # [x, y, w, h]
    landmarks: Optional[np.ndarray]  # 468 landmark points
    confidence: float
    is_frontal: bool  # Face orientation check
    roi_mask: Optional[np.ndarray]  # Region of interest mask


class FaceDetector:
    """
    Face detection using MediaPipe.
    Detects face, landmarks, and validates face orientation.
    """
    
    def __init__(
        self,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """
        Initialize face detector.
        
        Args:
            model_complexity: Complexity of face landmark model (0, 1)
            min_detection_confidence: Minimum detection confidence
            min_tracking_confidence: Minimum tracking confidence
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        
        # Face orientation thresholds (in degrees)
        self.yaw_threshold = 20.0  # Side-to-side
        self.pitch_threshold = 15.0  # Up-down
        self.roll_threshold = 10.0  # Tilt
    
    def detect_face(self, frame: np.ndarray) -> FaceDetectionResult:
        """
        Detect face in frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            FaceDetectionResult with detection details
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        
        # Run face detection
        results = self.face_mesh.process(frame_rgb)
        
        if not results.multi_face_landmarks:
            return FaceDetectionResult(
                bbox=None,
                landmarks=None,
                confidence=0.0,
                is_frontal=False,
                roi_mask=None,
            )
        
        # Get first face landmarks
        landmarks = results.multi_face_landmarks[0]
        
        # Convert landmarks to pixel coordinates
        landmark_points = np.array(
            [(lm.x * w, lm.y * h) for lm in landmarks.landmark],
            dtype=np.float32
        )
        
        # Calculate bounding box
        bbox = self._get_bounding_box(landmark_points)
        
        # Check face orientation
        is_frontal = self._check_orientation(landmark_points)
        
        # Create ROI mask (face region)
        roi_mask = self._create_roi_mask(frame.shape, landmark_points)
        
        return FaceDetectionResult(
            bbox=bbox,
            landmarks=landmark_points,
            confidence=0.95,  # MediaPipe doesn't provide per-detection confidence
            is_frontal=is_frontal,
            roi_mask=roi_mask,
        )
    
    def _get_bounding_box(self, landmarks: np.ndarray) -> np.ndarray:
        """Calculate bounding box from landmarks."""
        x_coords = landmarks[:, 0]
        y_coords = landmarks[:, 1]
        
        x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
        y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))
        
        w = x_max - x_min
        h = y_max - y_min
        
        return np.array([x_min, y_min, w, h], dtype=np.int32)
    
    def _check_orientation(self, landmarks: np.ndarray) -> bool:
        """
        Check if face is frontal (not too tilted/rotated).
        
        Uses key facial landmarks to estimate orientation angles.
        """
        # Use specific landmarks for orientation estimation
        nose_tip = landmarks[1]  # Nose tip
        left_eye = landmarks[33]  # Left eye
        right_eye = landmarks[263]  # Right eye
        left_mouth = landmarks[78]  # Left mouth corner
        right_mouth = landmarks[308]  # Right mouth corner
        
        # Calculate yaw (side-to-side rotation)
        eye_distance = np.linalg.norm(right_eye - left_eye)
        nose_to_left = np.linalg.norm(nose_tip - left_eye)
        nose_to_right = np.linalg.norm(nose_tip - right_eye)
        yaw = abs(nose_to_right - nose_to_left) / eye_distance
        
        # Calculate pitch (up-down rotation)
        mouth_distance = np.linalg.norm(right_mouth - left_mouth)
        nose_to_mouth = np.linalg.norm(nose_tip - (left_mouth + right_mouth) / 2)
        pitch = nose_to_mouth / mouth_distance
        
        # Check if within acceptable range
        # (These are approximate thresholds)
        is_frontal = (yaw < 0.3) and (0.3 < pitch < 0.7)
        
        return is_frontal
    
    def _create_roi_mask(self, frame_shape: Tuple, landmarks: np.ndarray) -> np.ndarray:
        """
        Create a mask for the face region (ROI).
        Used for signal extraction.
        """
        h, w = frame_shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # Use face contour landmarks (from MediaPipe)
        face_contour_indices = [
            10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
            397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
            172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
        ]
        
        face_contour = landmarks[face_contour_indices]
        
        # Draw filled polygon
        pts = np.array(face_contour, dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)
        
        return mask
    
    def get_roi(
        self,
        frame: np.ndarray,
        landmarks: np.ndarray,
        roi_mask: np.ndarray
    ) -> np.ndarray:
        """
        Extract region of interest (ROI) from frame.
        
        Args:
            frame: Input frame
            landmarks: Face landmarks
            roi_mask: Face region mask
            
        Returns:
            ROI extracted and normalized
        """
        # Apply mask to frame
        roi = cv2.bitwise_and(frame, frame, mask=roi_mask)
        
        # Optionally crop to bounding box for efficiency
        x, y, w, h = self._get_bounding_box(landmarks)
        roi_cropped = roi[y:y+h, x:x+w]
        
        return roi_cropped


# Example usage
if __name__ == "__main__":
    # Test face detection on a video file
    detector = FaceDetector()
    
    # Load test video
    cap = cv2.VideoCapture('test_video.mp4')
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect face
        result = detector.detect_face(frame)
        
        if result.bbox is not None:
            # Draw bounding box
            x, y, w, h = result.bbox
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw landmarks
            if result.landmarks is not None:
                for lm in result.landmarks[::10]:  # Draw every 10th point
                    cv2.circle(frame, tuple(lm.astype(int)), 2, (0, 0, 255), -1)
        
        # Display
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
