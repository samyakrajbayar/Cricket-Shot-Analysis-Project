import cv2
import numpy as np

class ShotVisualizer:
    def __init__(self):
        self.colors = {
            'correct': (0, 255, 0),  # Green
            'incorrect': (0, 0, 255),  # Red
            'neutral': (255, 255, 0),  # Cyan
            'text': (255, 255, 255)   # White
        }

    def draw_skeleton(self, img, pose_estimator):
        img = pose_estimator.find_pose(img, draw=True)
        return img

    def draw_dashboard(self, img, angles):
        # Create a dashboard overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (250, 150), (0, 0, 0), cv2.FILLED)
        alpha = 0.6
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Display angles
        y_offset = 30
        for key, value in angles.items():
            text = f"{key}: {int(value)}"
            cv2.putText(img, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['text'], 2)
            y_offset += 30
        return img

    def draw_feedback(self, img, feedback_list, state):
        # Display current state
        cv2.putText(img, f"State: {state}", (10, img.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['neutral'], 2)

        # Display feedback messages
        y_offset = 50
        for feedback in feedback_list:
            color = self.colors['incorrect']
            if "Good" in feedback:
                color = self.colors['correct']
            
            cv2.putText(img, feedback, (img.shape[1] - 350, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_offset += 30
        return img
