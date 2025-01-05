import json
from pororo import Pororo

# Pororo punctuation 모델 불러오기
punctuator = Pororo(task="punctuation", lang="ko")

# JSON 파일 경로
input_json_path = "../whisper/result.json"
output_json_path = "../whisper/punctuated_result.json"

# JSON 파일 읽기
with open(input_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# text 필드에 문장 부호 추가
if "text" in data:
    original_text = data["text"]
    punctuated_text = punctuator(original_text)
    data["text"] = punctuated_text
    print(f"문장 부호 추가된 text: {punctuated_text}")

# words 필드의 word에 문장 부호 추가
if "words" in data:
    words = data["words"]
    # 모든 단어를 공백으로 결합하여 텍스트로 변환
    combined_text = " ".join([word["word"] for word in words])
    punctuated_combined_text = punctuator(combined_text)

    # 문장 부호가 추가된 텍스트를 단어로 분리
    punctuated_words = punctuated_combined_text.split()

    # 기존 words 배열에 문장 부호가 추가된 단어 반영
    for i, word in enumerate(words):
        if i < len(punctuated_words):
            word["word"] = punctuated_words[i]
    
    print("문장 부호가 추가된 words:")
    for word in words[:10]:  # 첫 10개 단어만 출력
        print(word)

# 수정된 데이터를 새로운 JSON 파일로 저장
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"문장 부호가 추가된 JSON 파일이 '{output_json_path}'에 저장되었습니다.")
