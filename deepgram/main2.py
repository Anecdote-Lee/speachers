# main.py (python example)

from dotenv import load_dotenv
import os
import requests


from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import time

# 전체 실행 시간 측정 시작
start_time = time.perf_counter()

# Path to the audio file
AUDIO_FILE = "../data/example2.m4a"
OUTPUT_FILE = "./result/result.json"  # 저장할 텍스트 파일 경로
load_dotenv()
print(os.environ.get("DEEPGRAM_API_KEY"))

def main():
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient()

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            # keywords = ["어:5.0", "음:1.0", "아:1.0"],
            filler_words=True,
            language="ko",        # 언어 설정
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        # Extract the transcription text
        transcription_text = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        # 변환된 결과를 JSON 형식으로 출력
        response_json = response.to_json(indent=4, ensure_ascii=False)
        # Print the transcription text
        # print(f"Transcription:\n{transcription_text}")

        # STEP 4: Save transcription to a file
        # JSON 파일로 저장
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_file:
            json_file.write(response_json)
        print(f"JSON 파일이 저장되었습니다: {OUTPUT_FILE}")
        with open("./result/full_result.txt", "w", encoding="utf-8") as output_file:
            output_file.write(transcription_text)
        print(f"Transcription saved to full_result.txt")

    except Exception as e:
        print(f"Exception: {e}")

    # 전체 실행 시간 측정 종료
    end_time = time.perf_counter()

    # 실행 시간 출력
    total_time = end_time - start_time
    print(f"전체 실행 시간: {total_time:.2f}초")
if __name__ == "__main__":
    main()