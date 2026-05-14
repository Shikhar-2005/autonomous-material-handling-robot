import cv2
import subprocess
import sys

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
PARAMS = cv2.aruco.DetectorParameters()
DETECTOR = cv2.aruco.ArucoDetector(ARUCO_DICT, PARAMS)

cap = cv2.VideoCapture("http://10.191.58.237:8080/video")
if not cap.isOpened():
    print("Camera not found — check if webcam is connected")
    sys.exit(1)

print("Camera open — show ArUco marker ID 1 or ID 2")
print("Press Q to quit")

detected = False
while not detected:
    ret, frame = cap.read()
    if not ret:
        continue
    corners, ids, _ = DETECTOR.detectMarkers(frame)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        for marker_id in ids.flatten():
            if marker_id in [1, 2]:
                print(f"Detected marker ID: {marker_id} — Navigating to Position {marker_id}")
                cv2.imshow("ArUco Detection", frame)
                cv2.waitKey(1000)
                cap.release()
                cv2.destroyAllWindows()
                subprocess.run(
                    f'bash -c "source /opt/ros/jazzy/setup.bash && echo {marker_id} | python3 ~/navigate_to_goal.py"',
                    shell=True
                )
                detected = True
                break
    cv2.imshow("ArUco Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
