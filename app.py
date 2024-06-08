from flask import Flask, jsonify, request
from flask import Flask, jsonify, Blueprint, send_from_directory
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import cross_origin
load_dotenv()
import os, json
from db import Mongodb

from bson import json_util
def parse_json(data):
    return json.loads(json_util.dumps(data))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # 정적 파일 캐시 비활성화
CORS(app)

app.config['DB_USERNAME'] = os.getenv('MONGO_USER')
app.config['DB_PW'] = os.getenv('MONGO_PW')

# MongoDB 설정
app.config["MONGO_URI"] = "mongodb://"+ app.config['DB_USERNAME'] +":" + app.config['DB_PW'] + "@uskawjdu.iptime.org:17017/"
mongo = PyMongo(app)
db = Mongodb(app.config["MONGO_URI"], "SysMonLog")


@app.route('/')
def home():
    return "Hello, Flask with MongoDB!"


# 데이터 입력
@app.route('/add', methods=['POST'])
def add_data():
    # body에 있는 json 그대로 
    if request.is_json :
        data = request.get_json()
    else :
        data = request.form.to_dict()
    # ret = data.copy()
    db.refreshSock()
    coll = db.get_collection("logs")
    coll.insert_one(data)
    
    return parse_json(data), 200


@app.route('/deleteAllData', methods=['GET'])
def delete_AllData():
    try : 
        coll = db.get_collection("logs")
        coll.delete_many({})
    except :
        db.refreshSock()
        coll = db.get_collection("logs")
        coll.delete_many({})
        
    return "success", 200

@app.route('/getAllData', methods=['GET'])
def get_AllData():
    result = []
    data = {}
    try : 
        coll = db.get_collection("logs")
        data = coll.find()
    except :
        db.refreshSock()
        coll = db.get_collection("logs")
        data = coll.find()
    
    for row in data :
        row["_id"] = row["_id"].__str__()
        result.append(row)
    result.reverse()
    return jsonify(result)

    
# ==== swagger 설정 서버 동작과 상관 없음 ====
SWAGGER_URL =  "/docs/"
API_URL = "/docs/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint( 
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : "Test Craling db application"
    },
)

@app.route("/docs/swagger.json")
@cross_origin()  # 이 라우트에 대해 CORS 허용
def send_swagger_json():
    # print("file")
    response = send_from_directory('docs', 'swagger.json')
    # 브라우저가 캐시 사용하는 것을 막음
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# ==== 경계선 ====



if __name__ == '__main__':
    app.run(debug=True, port=8004, host='0.0.0.0')
    
    