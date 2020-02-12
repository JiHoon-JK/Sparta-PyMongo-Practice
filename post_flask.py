# Ctrl+alt+O => import 값 정렬 단축키
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('post.html')
    # template 에서 열어야하는 html 파일 정확하게 정의하기


@app.route('/post', methods=['POST'])
def saving():
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분 'url_give' 같은 것은 백엔드 개발자가 정의
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    # 클라이언트가 보내준 url을 url_receive에 넣는다.

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {
        'url': url_receive, 'comment': comment_receive, 'image': url_image,
        'title': url_title, 'desc': url_description
    }
    # article 이라는 새로운 데이터값을 정의
    db.articles.insert_one(article)

    return jsonify({'result': 'success'})
    # 성공하면 success 값을 보낸다 / 실패하면 잘 안됐다고 알려주면 됨


@app.route('/post', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({}, {'_id': 0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'articles': result})
    # DB에 저장되어있는 article 값을 result로!


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
    # 백엔드 서버를 띄워주는 구문
