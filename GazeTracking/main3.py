import cv2
import time
from gaze_tracking import GazeTracking

def calculate_center_time_ratio(video_path, sample_rate=2):
    gaze = GazeTracking()
    video = cv2.VideoCapture(video_path)

    # 비디오 정보 가져오기
    fps = video.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수
    frame_duration = 1 / fps  # 각 프레임의 시간 (초)

    # 샘플링: 균등 분포로 프레임 선택
    sampled_frame_indices = [i for i in range(0, total_frames, sample_rate)]  # 샘플링된 프레임 인덱스

    valid_frame_count = 0  # 얼굴이 감지된 유효 샘플 프레임 수
    center_frame_count = 0  # 중앙에 있는 프레임 수

    for frame_idx in sampled_frame_indices:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # 샘플링된 프레임으로 이동
        ret, frame = video.read()
        if not ret:
            break

        # GazeTracking으로 눈 추적
        gaze.refresh(frame)

        # 얼굴이 감지되지 않으면 해당 프레임 제외
        if not gaze.pupils_located:
            continue

        valid_frame_count += 1  # 유효 샘플 프레임 수 증가

        # 시선이 중앙에 있는지 확인
        if gaze.is_center():
            center_frame_count += 1

    video.release()

    # 총 시간 계산
    total_time = total_frames * frame_duration  # 전체 비디오 시간
    valid_time = valid_frame_count * sample_rate * frame_duration  # 유효 프레임 시간
    center_time = center_frame_count * sample_rate * frame_duration  # 중앙 프레임 시간

    # 비율 계산
    if valid_time == 0:
        return 0.0, 0.0

    center_ratio = (center_time / valid_time) * 100  # 중앙 비율
    return center_time, center_ratio

if __name__ == "__main__":
    video_path = "../data/pr_example.mp4"  # 분석할 동영상 경로
    start_time = time.time()
    center_time, ratio = calculate_center_time_ratio(video_path, sample_rate=1)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Total Center Time: {center_time:.2f} seconds")
    print(f"Eye Center Time Ratio: {ratio:.2f}%")
    print(f"Execution Time: {execution_time:.2f} seconds")