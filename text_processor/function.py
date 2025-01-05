from typing import List, Dict, Any
from collections import defaultdict
import json

# 필러 단어 정의 (예시)
FILLER_WORDS = ["음", "어", "아"]

def extract_pause_words(transcript_data: Dict[str, Any], pause_threshold: float = 1.0) -> List[Dict[str, Any]]:
    """Pause Words 추출."""
    words = transcript_data["words"]
    pause_words = []
    for i in range(1, len(words)):
        prev_word = words[i - 1]
        current_word = words[i]
        pause_duration = current_word["start"] - prev_word["end"]
        if pause_duration > pause_threshold:
            pause_words.append({
                "word": prev_word["word"] + " ... " + current_word["word"],
                "start_time": prev_word["end"],
                "end_time": current_word["start"]
            })
    return pause_words

def extract_sentence_starters(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Sentence Starters 추출 및 2회 이상 반복된 단어 필터링."""
    words = transcript_data["words"]
    sentence_starters = []

    for i, word in enumerate(words):
        if i > 0 and words[i - 1]["word"].endswith("."):
            sentence_starters.append({
                "word": word["word"],
                "start_time": word["start"],
                "end_time": word["end"]
            })
        elif i > 0 and "," in word["word"]:
            sentence_starters.append({
                "word": word["word"].split(",")[1],
                "start_time": word["start"],
                "end_time": word["end"]
            })


    starter_count = defaultdict(list)
    for starter in sentence_starters:
        starter_count[starter["word"]].append(starter)

    repeated_starters = []
    for word, occurrences in starter_count.items():
        if len(occurrences) > 1:
            repeated_starters.append({
                "word": word,
                "count": len(occurrences),
                "start_time": occurrences[0]["start_time"],
                "end_time": occurrences[-1]["end_time"]
            })
    
    return repeated_starters

def extract_repeated_words(transcript_data: dict, min_repetition: int = 2) -> List[Dict[str, Any]]:
    """반복된 단어 추출."""
    words = transcript_data["words"]
    repeated_words = []
    
    i = 0
    while i < len(words) - 1:
        current_word = words[i]["word"]
        start_time = words[i]["start"]
        count = 1
        
        while i + 1 < len(words) and words[i + 1]["word"] == current_word:
            count += 1
            i += 1
        
        end_time = words[i]["end"]
        
        if count >= min_repetition:
            repeated_words.append({
                "word": current_word,
                "count": count,
                "start_time": start_time,
                "end_time": end_time
            })
        
        i += 1
    
    return repeated_words

def extract_filler_words(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filler Words 추출."""
    words = transcript_data["words"]
    filler_words = [
        {
            "word": word["word"],
            "start_time": word["start"],
            "end_time": word["end"]
        }
        for word in words if "어," in word["word"]
    ]
    return filler_words

def calculate_metrics_over_time(extracted_data: List[Dict[str, Any]], interval: int = 10) -> Dict[int, int]:
    """10초 단위로 데이터 계산."""
    time_intervals = defaultdict(int)
    for item in extracted_data:
        start_time = item["start_time"]
        interval_key = int(start_time // interval)
        time_intervals[interval_key] += 1
    return time_intervals

def analyze_transcription(transcript_data: Dict[str, Any]) -> Dict[str, Any]:
    """전체 분석 수행."""
    pause_words = extract_pause_words(transcript_data)
    sentence_starters = extract_sentence_starters(transcript_data)
    repeated_words = extract_repeated_words(transcript_data)
    filler_words = extract_filler_words(transcript_data)

    # 10초 단위 계산
    pause_words_metrics = calculate_metrics_over_time(pause_words)
    filler_words_metrics = calculate_metrics_over_time(filler_words)
    
    analysis_result = {
        # "pause_words": pause_words,
        "sentence_starters": sentence_starters,
        "repeated_words": repeated_words,
        "filler_words": filler_words,
        # "pause_words_metrics": pause_words_metrics,
        "filler_words_metrics": filler_words_metrics
    }
    return analysis_result

# JSON 파일 읽기
def read_json_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return {}
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON")
        return {}

# 실행
file_path = '../whisper/punctuated_result.json'  # JSON 파일 경로
def main():

    print(analyze_transcription(read_json_file(file_path)))


if __name__ == "__main__":
    main()
