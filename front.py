from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import getlist
import main_ana

app = Flask(__name__,template_folder='templates')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)  # Allow all domains (you can specify domains if needed)

@app.route('/')
def home():
    return render_template('web.html')  # 如果放在 templates 目錄中

@app.route('/submit', methods=['POST'])
def submit():
    # 檢查請求的 Content-Type
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type. Content-Type must be 'application/json'"}), 415

    # 獲取 JSON 數據
    data = request.get_data()
    if not data or 'title' not in data:
        return jsonify({"error": "Invalid JSON or missing 'title' field"}), 400

    # 提取數據並調用處理函數
    l_u = data['title']
    main_ana.main(l_u)  # 假設 main_ana.main() 是你的一個處理函數

    # 返回渲染的 HTML 頁面
    return render_template('sub.html')

@app.route('/show')
def show():
    return render_template('show.html')

@app.route('/', methods=['POST'])
def playlist_selet():
    # 獲取 JSON 數據
    data = request.get_json()
    if not data or 'inputData' not in data:
        return jsonify({'error': 'No input provided'}), 400

    user_input = data['inputData']
    ll = getlist.get_list(user_input)
    ll.to_csv('test.csv')
    body = ''
    body +='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>PlaylistMotion</title><link rel="stylesheet" href="'+'{{'+' url_for(\'static\', filename=\'css/style_sub.css\') }}">\n'
    body+='</head><body><div class="header"><h1>PlaylistMotion</h1></div>\n<div class="pale"></div><div class="pale"></div>\n<div><p class="description">\n<strong>## Please select the proper playlist. ##</strong></p>\n</div><div class="pale"></div><div class="pale"></div>'
    with open ('test.csv','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            if line[0] != '':
                body+=f'\n        <div class="playlist-card"><img src="{line[2]}" alt="Playlist Image"><h3>{line[3]}</h3><p>Creator: {line[4]}</p><p><h2>{line[1]}</h2></a></p>\n<div class="pale"></div><button class="selectbutton" onclick="selectData(event)">Select</button></div><div class="pale"></div>\n'
    body+='\n</body1>\n</html>'
    getlist.export(body)
    
    return jsonify({'data': body}), 200
 
if __name__ == '__main__':
    app.run(host = '192.168.0.205', port= '8000', debug=True)
