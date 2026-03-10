import dlib
import cv2
import numpy as np
from scipy.spatial import distance as dist

class BioSentinelEngine:
    def __init__(self):
        # Load the pre-trained model you just downloaded
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        
        # Landmark indices for the eyes
        self.L_EYE = list(range(42, 48))
        self.R_EYE = list(range(36, 42))

    def calculate_ear(self, eye):
        # EAR formula: (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    def get_stress_status(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        for rect in rects:
            shape = self.predictor(gray, rect)
            # Convert to numpy array
            coords = np.matrix([[p.x, p.y] for p in shape.parts()])
            
            left_ear = self.calculate_ear(coords[self.L_EYE])
            right_ear = self.calculate_ear(coords[self.R_EYE])
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Threshold: < 0.20 typically indicates fatigue or high stress
            return "LOCKDOWN" if avg_ear < 0.20 else "STABLE"
        return "STABLE"