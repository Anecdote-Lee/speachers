# 모듈 설치: !pip install moviepy
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_file_path, audio_file_path):
    # mp4 등 비디오 파일 불러오기
    video = VideoFileClip(video_file_path)
    video.audio.write_audiofile(audio_file_path, codec='pcm_s16le')
    

video_file = '../data/ex1.mp4'  # 변환하고 싶은 비디오 파일의 경로
audio_file = '../data/output_ex1.wav'  # 저장할 오디오 파일의 경로, 이름 지정

extract_audio_from_video(video_file, audio_file)