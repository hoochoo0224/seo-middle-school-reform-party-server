import requests
import json

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'  
rest_api_key = '72a798ae5b6a1ad7489c438c2cce0615'  
redirect_uri = 'http://127.0.0.1:5000/제보'


def f_auth(authorize_code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    r_token = ts["refresh_token"]
    
    return r_token

def f_auth_refresh(r_token):
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": r_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open(r"kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    token = ts["access_token"]

    return token

def f_send_talk(token, text):
    header = {'Authorization': 'Bearer ' + token}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'  
    post = {
        'object_type': 'text',
        'text': text,
        'link': {
            'web_url': 'https://developers.kakao.com',
            'mobile_web_url': 'https://developers.kakao.com'
        },
        # 'button_title': '버튼'
    }
    data = {'template_object': json.dumps(post)}

    return requests.post(url, headers=header, data=data)