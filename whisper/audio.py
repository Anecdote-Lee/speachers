import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import json
# 전체 실행 시간 측정 시작
start_time = time.perf_counter()
# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 오디오 파일 경로
audio_path = "../data/output_ex1.wav"
output_file_path = "./audio_result.txt"
# 파일 전체를 바이너리로 읽고 Base64로 인코딩
with open(audio_path, "rb") as audio_file:
    encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": [
                { 
                    "type": "text",
                    "text": "이 발표에서 잘한 점과 부족한 점을 알려주세요"
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_string,
                        "format": "wav"
                    }
                }
            ]
        },
    ]
)

# print(completion.choices[0].message)
# JSON 파일 저장
with open("./result.json", "w", encoding="utf-8") as json_file:
    json.dump(completion.choices[0], json_file, ensure_ascii=False, indent=4)  # JSON 직렬화
    print("Transcription saved to result.json")
# with open(output_file_path, "w", encoding="utf-8") as file:
#     # 전체 텍스트 저장
#     file.write(completion.choices[0] + "\n\n")

    # # 세그먼트별 텍스트 저장
    # file.write("Segmented Transcription:\n")
    # for segment in segments:
    #     start_time = segment.get("start", 0.0)
    #     end_time = segment.get("end", 0.0)
    #     text = segment.get("text", "")

    #     file.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")

print(f"Transcription saved to {output_file_path}")
# 전체 실행 시간 측정 종료
end_time = time.perf_counter()

# 실행 시간 출력
total_time = end_time - start_time
print(f"전체 실행 시간: {total_time:.2f}초")