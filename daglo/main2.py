import requests
import json
import time
import os

# API 엔드포인트 및 인증 토큰 설정
API_URL = "https://apis.daglo.ai/stt/v1/async/transcripts"  # Daglo STT API 엔드포인트
API_KEY = "kjWcz_KV29LE1qbkAdz2uTWo"  # 환경 변수로 API 키를 불러옴

# 오디오 파일 경로
audio_file_path = "../data/example2.m4a"

# 전체 실행 시간 측정 시작
start_time = time.perf_counter()

# 헤더 설정
headers = {
    "Authorization": f"Bearer {API_KEY}",  # API 키 인증
    "accept": "application/json",
}

# 파일 업로드 및 요청 데이터 준비
files = {
    "file": open(audio_file_path, "rb")
}
nlp = {
        "keywordExtraction": {
        "enable": True,
        "maxCount" : 10
    }
}

data = {
    "sttConfig": {
    "model": "stt-large",  # 사용하고자 하는 STT 모델 이름
    "language": "ko",  # 언어 설정 (예: 한국어)
    # "diarization": True,  # 화자 분리 사용 여부
    "timestamps": True,  # 타임스탬프 활성화
    "keywordBoost": {
        "enable": True,
        "keywords": ["음", "어", "아"]
            },
    },
    "nlpConfig" : nlp

}

# POST 요청 보내기
print("Sending transcription request...")
response = requests.post(API_URL, headers=headers, files=files, data=json.dumps(data))
response.raise_for_status()

# 작업 ID 추출
response_data = response.json()
task_id = response_data.get("rid")
if not task_id:
    print("Error: No task_id returned from the server.")
    exit()

print(f"Task ID received: {task_id}")


# GET 요청을 통해 작업 상태 및 결과 확인
result_url = f"{API_URL}/{task_id}"
while True:
    print("Checking transcription status...")
    result_response = requests.get(result_url, headers=headers)
    result_response.raise_for_status()
    result_data = result_response.json()

    # 상태 확인
    status = result_data.get("status")
    if status == "transcribed":
        print("Transcription completed.")
        break
    elif "error" in status:
        print("Transcription failed.")
        exit()
    else:
        print(f"Current status: {status}. Retrying in 5 seconds...")
        time.sleep(1)
# JSON에서 전체 텍스트와 세그먼트 추출
stt_results = result_data.get("sttResults", [])
if not stt_results:
    print("No transcription results found.")
    exit()

# 전체 텍스트 추출
full_text = stt_results[0].get("transcript", "")

# 세그먼트별 단어 추출
segments = stt_results[0].get("words", [])
# 결과 저장 경로
output_dir = "./results"
os.makedirs(output_dir, exist_ok=True)

# 전체 텍스트 저장
full_text_path = os.path.join(output_dir, "full_result.txt")
with open(full_text_path, "w", encoding="utf-8") as full_text_file:
    full_text_file.write(full_text)
print(f"Full transcription saved to {full_text_path}")

# JSON 파일 저장
json_path = os.path.join(output_dir, "result.json")
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=4)
print(f"Transcription data saved to {json_path}")

# # 세그먼트별 텍스트와 타임스탬프 저장
# segments_path = os.path.join(output_dir, "segment_result.txt")
# with open(segments_path, "w", encoding="utf-8") as segment_file:
#     for segment in segments:
#         start_time = segment.get("start", 0)
#         end_time = segment.get("end", 0)
#         text = segment.get("text", "")
#         segment_file.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")
# print(f"Segmented transcription saved to {segments_path}")

# 전체 실행 시간 측정 종료
end_time = time.perf_counter()
total_time = end_time - start_time
print(f"전체 실행 시간: {total_time:.2f}초")
