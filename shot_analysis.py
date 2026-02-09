import cv2
import numpy as np

class ShotAnalyzer:
    def __init__(self, mode="Cover Drive"):
        self.mode = mode
        self.state = "IDLE" # IDLE, STANCE, BACKLIFT, IMPACT, FOLLOW_THROUGH
        self.feedback = []
        
        # Thresholds for Cover Drive (approximate)
        self.stance_knee_angle = (130, 160)
        self.backlift_elbow_angle = (70, 100) # Leading arm elbow
        self.impact_knee_angle = (100, 140) # Front knee bent

    def analyze_shot(self, img, pose_estimator):
        lm_list = pose_estimator.find_position(img, draw=False)
        self.feedback = [] # Reset feedback
        
        if len(lm_list) != 0:
            # Right Handed Batsman Assumption
            # 11: left_shoulder, 13: left_elbow, 15: left_wrist
            # 23: left_hip, 25: left_knee, 27: left_ankle
            
            # Calculate angles
            left_elbow_angle = pose_estimator.find_angle(img, 11, 13, 15, draw=True)
            left_knee_angle = pose_estimator.find_angle(img, 23, 25, 27, draw=True)
            right_elbow_angle = pose_estimator.find_angle(img, 12, 14, 16, draw=True)

            # Determine State based on simple heuristics (can be improved with temporal logic)
            # This is a simplified state estimator for demo purposes
            
            # Check for Stance
            if 130 < left_knee_angle < 170 and 130 < right_elbow_angle < 170:
                self.state = "STANCE"
                self.check_stance(left_knee_angle)

            # Check for Backlift (Leading elbow bends, hands go up)
            # Identifying backlift is tricky without temporal data, 
            # we'll look for high elbows or specific wrist positions relative to shoulder
            elif left_elbow_angle < 100 and left_knee_angle > 140:
                self.state = "BACKLIFT"
                self.check_backlift(left_elbow_angle)

            # Check for Impact (Front knee bent, weight transfer)
            elif left_knee_angle < 130: 
                self.state = "IMPACT"
                self.check_impact(left_knee_angle, left_elbow_angle)
            
            else:
                 self.state = "TRANSITION"

            return {
                "Left Elbow": left_elbow_angle,
                "Left Knee": left_knee_angle,
                "Right Elbow": right_elbow_angle
            }
        
        return {}

    def check_stance(self, knee_angle):
        if not (self.stance_knee_angle[0] <= knee_angle <= self.stance_knee_angle[1]):
            self.feedback.append(f"Adjust Knee Bend ({int(knee_angle)})")
        else:
            self.feedback.append("Good Stance Base")

    def check_backlift(self, elbow_angle):
        # Example check
        if elbow_angle > 120:
             self.feedback.append("Lift Elbow Higher")
        else:
             self.feedback.append("Good High Elbow")

    def check_impact(self, knee_angle, elbow_angle):
        if knee_angle > 140:
             self.feedback.append("Bend Front Knee More")
        else:
             self.feedback.append("Good Knee Flex")
        
        # Check if head is over ball (simplified proxy via elbow/shoulder alignment)
        # For now, just a placeholder feedback
