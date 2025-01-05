from openai import OpenAI
from dotenv import load_dotenv
import json
import time
import os
# 전체 실행 시간 측정 시작
start_time = time.perf_counter()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 발급받은 API 키 설정
# openai API 키 인증
audio_file= open("../data/example2.m4a", "rb")
transcription = client.audio.transcriptions.create(
   file=audio_file,
    model="whisper-1",
    # language="ko",
    response_format="verbose_json",
    timestamp_granularities=["word"],
)
# `transcription`을 dict로 변환
transcription_dict = transcription.to_dict()
# 전체 텍스트와 세그먼트 추출
full_text = transcription.text
segments = transcription.words
# 파일 경로 설정
file_path = "./result/transcription.txt"


with open("./segmented_full_result.txt", "w", encoding="utf-8") as output_file:
    output_file.write(full_text)
    print(f"Transcription saved to full_result.txt")

# JSON 파일 저장
with open("./segmented_result.json", "w", encoding="utf-8") as json_file:
    json.dump(transcription_dict, json_file, ensure_ascii=False, indent=4)  # JSON 직렬화
    print("Transcription saved to result.json")

    # # 세그먼트별 텍스트 저장
    # file.write("Segmented Transcription:\n")
    # for segment in segments:
    #     start_time = segment.start
    #     end_time = segment.end
    #     text = segment.word

    #     file.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")


# 전체 실행 시간 측정 종료
end_time = time.perf_counter()

# 실행 시간 출력
total_time = end_time - start_time
print(f"전체 실행 시간: {total_time:.2f}초")