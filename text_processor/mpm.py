import json
from kiwipiepy import Kiwi
from collections import defaultdict
from typing import List, Dict

# KIWI 형태소 분석기 초기화
kiwi = Kiwi()

def parse_script(data: Dict) -> List[Dict]:
    """
    스크립트 JSON 데이터에서 각 단어와 타임스탬프 추출.
    """
    words_data = data['words']
    return [
        {
            "word": word['word'],
            "start": word['start'],
            "end": word['end']
        }
        for word in words_data
    ]

def analyze_morphemes_with_timestamp(words: List[Dict]) -> List[Dict]:
    """
    KIWI를 이용해 형태소 분석 및 형태소 개수 추출.
    형태소 개수에 따라 타임스탬프를 N등분하여 각 형태소에 할당.
    """
    analyzed_morphemes = []
    for word_data in words:
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        analysis = kiwi.analyze(word)
        if not analysis:
            continue
        
        morphemes = analysis[0][0]
        morpheme_count = len(morphemes)

        if morpheme_count == 1:
            analyzed_morphemes.append({
                "morpheme": morphemes[0].form,
                "start": start,
                "end": end
            })
        else:
            time_interval = (end - start) / morpheme_count
            for idx, token in enumerate(morphemes):
                morpheme_start = start + idx * time_interval
                morpheme_end = morpheme_start + time_interval
                analyzed_morphemes.append({
                    "morpheme": token.form,
                    "start": morpheme_start,
                    "end": morpheme_end
                })
    return analyzed_morphemes

def calculate_morphemes_per_10s(morphemes: List[Dict], interval: int = 10) -> Dict[int, float]:
    """
    10초 단위로 분당 형태소 수 계산.
    """
    interval_morphemes = defaultdict(int)
    max_time = max(morpheme['end'] for morpheme in morphemes) if morphemes else 0

    for morpheme_data in morphemes:
        start_time = morpheme_data['start']
        interval_key = int(start_time // interval)
        interval_morphemes[interval_key] += 1

    morphemes_per_10s = {}
    for i in range(0, int(max_time // interval) + 1):
        if i in interval_morphemes:
            morphemes_per_10s[i] = (interval_morphemes[i] / interval) * 60
        else:
            morphemes_per_10s[i] = 0.0

    return morphemes_per_10s

def save_mpm_to_db(file_path: str):
    """
    JSON 파일을 읽어 mpm 분석 결과를 계산.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON")
        return

    try:
        # Step 1: 스크립트 데이터 파싱
        words = parse_script(data)

        # Step 2: 형태소 분석 및 타임스탬프 분할
        analyzed_morphemes = analyze_morphemes_with_timestamp(words)

        # Step 3: 분당 형태소 수 계산
        morphemes_per_10s = calculate_morphemes_per_10s(analyzed_morphemes)

        return morphemes_per_10s

    except Exception as e:
        print(f"Error: {e}")


def main():
    file_path = '../whisper/result.json'  # JSON 파일 경로
    mpm_result = save_mpm_to_db(file_path)
    if mpm_result:
        print("분당 형태소 수(MPM):", mpm_result)


if __name__ == "__main__":
    main()
