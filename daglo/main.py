import requests
import json

token = "kjWcz_KV29LE1qbkAdz2uTWo"

url = "https://apis.daglo.ai/stt/v1/async/transcripts"

files = { "file": "open('../rtzr_stt/example2.m4a', 'rb')" }
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}

response = requests.post(url, files=files, headers=headers)

print(response.json())

with open('./result3.json', 'w', encoding='utf-8') as json_file:
        json.dump(response.json(), json_file, ensure_ascii=False, indent=4)

# rid = response.json()['rid']

# url = f"https://apis.daglo.ai/stt/v1/async/transcripts/{rid}/srt"

# headers = {
#     "Accept": "text/plain, application/json",
#     "Authorization": "Bearer " + token
# }

# response2 = requests.get(url, headers=headers)
# print(response2.json())
# with open('./result3.json', 'w', encoding='utf-8') as json_file:
#         json.dump(response2.json(), json_file, ensure_ascii=False, indent=4)