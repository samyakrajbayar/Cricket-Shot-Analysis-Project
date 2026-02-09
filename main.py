import cv2
import time
from pose_module import PoseEstimator
from shot_analysis import ShotAnalyzer
from visualizer import ShotVisualizer

def main():
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    
    # Initialize Modules
    pose_estimator = PoseEstimator()
    shot_analyzer = ShotAnalyzer()
    visualizer = ShotVisualizer()
    
    pTime = 0
    
    print("Starting Cricket Shot Analysis... Press 'q' to quit.")
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera.")
            break
            
        # 1. Pose Estimation
        img = pose_estimator.find_pose(img, draw=False)
        
        # 2. Shot Analysis
        analysis_results = shot_analyzer.analyze_shot(img, pose_estimator)
        
        # 3. Visualization
        img = visualizer.draw_skeleton(img, pose_estimator)
        img = visualizer.draw_dashboard(img, analysis_results)
        img = visualizer.draw_feedback(img, shot_analyzer.feedback, shot_analyzer.state)
        
        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        # Display Result
        cv2.imshow("Cricket Shot Analysis", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
