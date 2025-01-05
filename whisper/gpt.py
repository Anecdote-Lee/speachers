from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 오디오 파일 경로
audio_file_path = "../rtzr_stt/example2.m4a"

# 텍스트 파일 저장 경로
output_file_path = "./result/transcription_gpt.txt"

# 시스템 프롬프트 정의
system_prompt = "Full transcription을 바탕으로 segmented transcription에 해당하는 부분만 문맥에 맞게 글자 오류 및 발음의 유사성으로 잘못된 단어를 수정해주고 수정된 segmented transcription만 timestamp와 함께 반환해줘, 기존 timestamp에서 바뀌면 안되고 마음대로 글을 정리하는 등 기존 글에서 벗어나지 말아줘"

def transcribe_audio(file_path, prompt):
    """
    오디오 파일을 Whisper API로 전사.
    """
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            language="ko",
            temperature=0.0,
            response_format="verbose_json",
            timestamp_granularities=["word"],
            prompt=prompt
        )
    return transcription


def generate_corrected_transcript(temperature, system_prompt, original_text):
    """
    GPT-4를 사용하여 전사된 텍스트를 수정.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question_1},
            {"role": "assistant", "content": original_text},
            {"role": "user", "content": question_2},
            {"role": "assistant", "content": original_text},
            {"role": "user", "content": question_3},
            {"role": "assistant", "content": original_text},
            {"role": "user", "content": question_4},
            {"role": "assistant", "content": original_text},
            {"role": "user", "content": original_text},
            {"role": "assistant", "content": original_text},

        ]
    )
    return response.choices[0].message.content


# 메인 실행 로직
try:
    # 전사 요청
    transcription = transcribe_audio(audio_file_path, prompt="어, 음, 그, 저, 아")
    print(1)
    # 전체 텍스트와 세그먼트 추출
    full_text = transcription.text
    segments = transcription.words

    file_path = "./result/transcription.txt"
        # 텍스트 파일로 저장
    with open(file_path, "w", encoding="utf-8") as file:
        # 전체 텍스트 저장
        file.write("Full Transcription:\n")
        file.write(full_text + "\n\n")

        # 세그먼트별 텍스트 저장
        file.write("Segmented Transcription:\n")
        for segment in segments:
            start_time = segment.start
            end_time = segment.end
            text = segment.word

            file.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")


    corrected_text = generate_corrected_transcript(0, system_prompt, full_text)
    print(2)
    # 텍스트 파일로 저장
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as file:
        # 전체 텍스트 저장
        file.write("Full Transcription:\n")
        file.write(corrected_text + "\n\n")

        # # 세그먼트별 텍스트 저장
        # file.write("Segmented Transcription:\n")
        # for segment in segments:
        #     start_time = segment.get("start", 0.0)
        #     end_time = segment.get("end", 0.0)
        #     text = segment.get("text", "")

        #     file.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")

    print(f"Transcription saved to {output_file_path}")

    # 수정된 텍스트 생성
    # print("\nCorrected Text:")
    # print(corrected_text)

except Exception as e:
    print(f"Error: {e}")