import cv2
import time
from gaze_tracking import GazeTracking

def calculate_center_time_ratio(video_path):
    gaze = GazeTracking()
    video = cv2.VideoCapture(video_path)

    # 비디오 정보 가져오기
    fps = video.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수
    frame_duration = 1 / fps  # 각 프레임의 시간 (초)

    total_time = 0.0  # 전체 비디오 시간 (초)
    center_time = 0.0  # 중앙에 있는 시간 (초)

    while True:
        # 비디오에서 프레임 읽기
        ret, frame = video.read()
        if not ret:
            break

        # GazeTracking을 이용해 눈 추적
        gaze.refresh(frame)
        # 얼굴이 감지되지 않으면 해당 프레임 제외
        if not gaze.pupils_located:
            continue
        total_time += frame_duration

        # 시선이 중앙에 있는지 확인
        if gaze.is_center():
            center_time += frame_duration

    # 비율 계산
    video.release()
    if total_time == 0:
        return 0.0, 0.0
    return center_time, (center_time / total_time) * 100

if __name__ == "__main__":
    video_path = "../data/pr_example.mp4"  # 분석할 동영상 경로
    start_time = time.time()
    center_time, ratio = calculate_center_time_ratio(video_path)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total Center Time: {center_time:.2f} seconds")
    print(f"Eye Center Time Ratio: {ratio:.2f}%")
    print(f"Execution Time: {execution_time:.2f} seconds")
