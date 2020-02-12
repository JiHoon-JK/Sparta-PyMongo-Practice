# Ctrl+alt+O => import 값 정렬
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


#제일 처음에 나오는 shop.html 이 나오는 api
@app.route('/')
def home():
    return render_template('shop.html')
    # template 에서 열어야하는 html 파일 정확하게 정의하기

#고객이 입력한 정보를 저장하는 api : clientlist_post
@app.route('/order', methods=['POST'])
def clientlist_post():
    name_receive = request.form['name_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    client_list = {
        'name': name_receive,
        'amount': amount_receive,
        'address': address_receive,
        'phone': phone_receive
    }

    db.shop_client_list.insert_one(client_list)
    # 다했으면 성공여부만 보냄
    return jsonify({'result': 'success'})

#shop_client_list 에 저장된 정보를 가져오는 api : clientlist_get
@app.route('/order', methods=['GET'])
def clinetlist_get():
    # id 값은 제외하고, 모든 값을 가져오기
    orders = list(db.shop_client_list.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
    # 백엔드 서버를 띄워주는 구문
