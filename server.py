from flask import Flask, render_template, request, redirect, url_for
from kakao import *
from notion import *

app = Flask(__name__)

images = {}
for result in readDatabase("img", databaseId, headers)["results"]:
    images[result["properties"]["이름"]["title"][0]["text"]["content"]] = result["properties"]["사진이나 동영상"]["files"][0]["file"]["url"]

reportContents = {}

news_titles = {
    "정치" : ["조현민이 학생회장이 되어야 하는 이유", "조현민 커리어 소개", "학생회장 조현민 당선!"],
    "스포츠-연예" : ["서중 축구대회 승자는 누구?", "조현민 같은 얼굴도 여친이 없다??"],
    "학교밖" : []
}

@app.route('/')
def index():
    return render_template("index.html", images=images)

@app.route('/공지')
def 공지():
    return render_template("공지.html", images=images)

@app.route('/사진▣◈ㅁㄴ라ㅜㅁ히마ㅓㅗ')
def 사진():
    return render_template("사진.html", images=images)

@app.route('/정치/')
def 정치():
    try:
        title = request.args.get('title', default = None, type = str)
        return render_template(f"정치{news_titles['정치'].index(title)+1}.html", images=images, title=title)
    except ValueError:
        return render_template("정치.html", images=images, news_titles=news_titles["정치"])

@app.route('/스포츠-연예/')
def 스포츠_연예():
    try:
        title = request.args.get('title', default = None, type = str)
        return render_template(f"스포츠-연예{news_titles['스포츠-연예'].index(title)+1}.html", images=images, title=title)
    except ValueError:
        return render_template("스포츠-연예.html", images=images, news_titles=news_titles["스포츠-연예"])

@app.route('/학교밖/')
def 학교밖():
    try:
        title = request.args.get('title', default = None, type = str)
        return render_template(f"학교밖{news_titles['학교밖'].index(title)+1}.html", images=images, title=title)
    except ValueError:
        return render_template("학교밖.html", images=images, news_titles=news_titles["학교밖"])

@app.route('/제보', methods=["POST", "GET"])
def 제보():
    if request.method == "POST":
        reportContents["name"] = request.form["name"]
        reportContents["phoneNumber"] = request.form["phoneNumber"]
        reportContents["contents"] = request.form["contents"]
        if reportContents["name"] == "사진" and reportContents["phoneNumber"] == "24" and reportContents["contents"] == "pw:ilovesans":
            return redirect(url_for('사진'))
        else:
            return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code&scope=talk_message")
    if request.method == "GET":
        try:
            authorize_code = request.args.get("code", default = None, type = str)
            r_token = f_auth(authorize_code)
            token = f_auth_refresh(r_token)  
            response = f_send_talk (token, "이름: {0}\n전화번호: {1}\n내용: {2}".format(reportContents["name"], reportContents["phoneNumber"], reportContents["contents"]))
            print(response.status_code)
            if response.json().get("result_code") == 0:
                print("메시지 보내기 성공!")
            else:
                print("메시지 보내기 실패 ㅠㅠ 오류메시지:", str(response.json()))

            return render_template("제보.html", images=images)
        except KeyError:
            return render_template("제보.html", images=images)

if __name__ == '__main__':
    app.run(debug=True, port="5000")