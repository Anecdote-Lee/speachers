import requests
import json
import time

# 전체 실행 시간 측정 시작
start_time = time.perf_counter()
resp = requests.post(
    'https://openapi.vito.ai/v1/authenticate',
    data={'client_id': 'vjwkZkjlKsz_TjkevCCr',
          'client_secret': 'phZu2fbSz4knyMBL2zBtXLccSLdbJrYQCJ4xjAuo'}
)

resp.raise_for_status()

auth_token = resp.json()['access_token']
# print(auth_token)

# URL과 헤더 설정
url = "https://openapi.vito.ai/v1/transcribe"
headers = {
    "accept": "application/json",
    "Authorization": 'Bearer ' + auth_token,  
    # "Content-Type": "multipart/form-data"
}
file_name = "test.webm"
# 파일과 config 데이터 설정
files = {
    'file': open(f'../data/{file_name}', 'rb')  
}

# config 데이터는 Python 딕셔너리 형식으로 작성
config_data = {
    "model_name": "sommers",
    "use_diarization": True,
    "use_disfluency_filter": False,
    "use_word_timestamp": True
}

# config 딕셔너리를 JSON 문자열로 변환하여 전송
data = {
    'config': json.dumps(config_data)  # Python 딕셔너리를 JSON 문자열로 변환
}

# POST 요청 보내기
response = requests.post(url, headers=headers, files=files, data=data)

# 응답에서 id 추출
task_id = response.json().get('id')
print(f"작업 ID: {task_id}")

# 상태 확인을 위한 URL 설정
status_url = f"https://openapi.vito.ai/v1/transcribe/{task_id}"

# 반복해서 상태 확인
while True:
    status_response = requests.get(status_url, headers=headers)
    status_response.raise_for_status()
    status_data = status_response.json()

    # 상태 확인
    status = status_data.get('status')
    print(f"현재 상태: {status}")
    
    # 완료 시 파일 저장
    if status == 'completed':
        with open(f'./result_{file_name}.json', 'w', encoding='utf-8') as json_file:
            json.dump(status_data, json_file, ensure_ascii=False, indent=4)
        print("응답 JSON이 'result.json' 파일로 저장되었습니다.")


        # 텍스트 추출 및 파일 저장
        transcription_text = status_data.get('results', {}).get('utterances', [])
        with open(f'./full_result_{file_name}.txt', 'w', encoding='utf-8') as txt_file:
            for utterance in transcription_text:
                txt_file.write(utterance.get('msg', '') + '\n')
        print("전사 텍스트가 'full_result.txt' 파일로 저장되었습니다.")
        break
    elif status == 'failed':
        print("전사 작업이 실패했습니다.")
        break

    # 일정 시간 대기 후 다시 상태 확인
    time.sleep(5)  # 5초 대기 후 재확인


# 전체 실행 시간 측정 종료
end_time = time.perf_counter()

# 실행 시간 출력
total_time = end_time - start_time
print(f"전체 실행 시간: {total_time:.2f}초")