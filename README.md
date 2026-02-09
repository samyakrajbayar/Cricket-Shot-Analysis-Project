# Cricket Shot Analysis Project

## Overview
This project uses MediaPipe and OpenCV to detect and analyze cricket shot poses (specifically the Cover Drive). It provides real-time feedback on body posture, including knee bend and elbow position.

## Features
- **Pose Detection**: Real-time skeleton tracking.
- **Shot Analysis**: State machine to detect phases (Stance -> Backlift -> Impact).
- **Feedback System**: Visual cues and text feedback for correcting technique.
- **Dashboard**: Live display of key joint angles.

## Installation
1.  **Clone the repository** or download the files.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1.  **Run the main application**:
    ```bash
    python main.py
    ```
2.  **Position yourself**: Ensure the camera can see your full body (side-on view serves best for Cover Drive analysis).
3.  **Perform a shot**: The system will track your movement and provide feedback.
    -   **Stance**: Stand with knees bent.
    -   **Backlift**: Raise the bat (high elbow).
    -   **Impact**: Step forward and play the shot.

## Project Structure
-   `main.py`: Entry point of the application.
-   `pose_module.py`: Handles MediaPipe pose estimation.
-   `shot_analysis.py`: Logic for analyzing cricket shots.
-   `visualizer.py`: Handles drawing and UI overlays.
