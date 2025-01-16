import cv2
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO
import torch

# Define skeleton structure based on the provided diagram
skeleton_connections = [
    (5, 7), (7, 9),  # Left shoulder to left hand
    (6, 8), (8, 10), # Right shoulder to right hand
    (5, 6),           # Shoulder to shoulder
    (5, 11), (6, 12), # Shoulders to hips
    (11, 12),         # Hip to hip
    (11, 13), (13, 15), # Left hip to left foot
    (12, 14), (14, 16)  # Right hip to right foot
]

# Initialize YOLOv8 Pose model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO("yolov8n-pose.pt").to(device)
print("YOLOv8 Pose model loaded.")

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Align depth to color stream
align = rs.align(rs.stream.color)

try:
    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert frames to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Perform pose detection
        results = model(color_image)

        for result in results:
            if result.keypoints:
                keypoints = result.keypoints.xy.cpu().numpy()  # Extract keypoints

                # Draw keypoints and skeleton connections
                for person in keypoints:
                    # Draw keypoints
                    for i, (x, y) in enumerate(person):
                        if x > 0 and y > 0:  # Valid keypoints
                            cv2.circle(color_image, (int(x), int(y)), 5, (0, 255, 0), -1)

                    # Draw skeleton connections
                    for joint_start, joint_end in skeleton_connections:
                        if joint_start < len(person) and joint_end < len(person):
                            x_start, y_start = person[joint_start]
                            x_end, y_end = person[joint_end]
                            if x_start > 0 and y_start > 0 and x_end > 0 and y_end > 0:  # Valid keypoints
                                # Set color for connections
                                if (joint_start, joint_end) in [(5, 7), (7, 9), (6, 8), (8, 10)]:
                                    color = (0, 255, 255)  # Yellow for arms
                                elif (joint_start, joint_end) in [(11, 13), (13, 15), (12, 14), (14, 16)]:
                                    color = (255, 0, 0)  # Blue for legs
                                else:
                                    color = (0, 255, 0)  # Green for torso
                                cv2.line(
                                    color_image,
                                    (int(x_start), int(y_start)),
                                    (int(x_end), int(y_end)),
                                    color,
                                    2,
                                )

        # Display results
        cv2.imshow("Filtered Pose Detection", color_image)

        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()