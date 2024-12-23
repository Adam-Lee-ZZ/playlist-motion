from flask import Flask, request, jsonify, render_template, send_file,request
from flask_cors import CORS
import os
import getlist
import main_ana
from celery import Celery

app = Flask(__name__, template_folder='templates',static_folder='static')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config.update(
    CELERY_BROKER_URL=os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
)


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

CORS(app, resources={r"/*": {"origins": "*"}})  
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_fallback_secret_key')

CLIENT_ID = 
CLIENT_SECRET = 
REDIRECT_URI = 

@celery.task(bind=True)
def analyze_task(self, text):

    self.update_state(state='PROGRESS', meta={'current': 1, 'total': 5, 'status': 'Starting analysis'})
    playlist_data = main_ana.get_playlist(text)

    self.update_state(state='PROGRESS', meta={'current': 2, 'total': 5, 'status': 'Playlist gained'})
    lyrics = main_ana.lyrics(playlist_data)

    self.update_state(state='PROGRESS', meta={'current': 3, 'total': 5, 'status': 'Lyrics gained'})
    d,wordcloud_path = main_ana.plot_wordcloud(lyrics, 'Cloud Plot of Your List', 20000)

    sixd_path = main_ana.sixd(d)

    result = {
        'wordcloud_path': wordcloud_path,
        'six_dimensions_path': sixd_path
    }
    return {'current': 5, 'total': 5, 'status': 'Complete', 'result': result }


@app.route('/')
def home():
    return render_template('web.html')  

@app.route('/generate_subsite', methods=['POST'])
def generate_subsite():

    data = request.get_json()
    if not data or 'inputData' not in data:
        return jsonify({'error': 'No input provided'}), 400

    user_input = data['inputData']
    ll = getlist.get_list(user_input)

    body = ''
    body += '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">'
    body += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    body += '<title>PlaylistMotion</title>'
    body += '''<style>
                body {
                    background-image: url('static/css/A.png');
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    height: auto;
                    overflow-y: auto;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    position: relative;
                    flex-direction: column;
                }
                
                .header {
                    position: absolute;
                    top: 20px;
                    left: 20px;
                }
                
                .header h1 {
                    font-style: italic;
                    color: black;
                    background-color: green;
                    display: inline-block;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                
                .content {
                    margin-top: 20px;
                }
                
                
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center; 
                    flex-wrap: wrap;
                    margin-top: 100px; 
                    padding-top: 20px;
                }
                
                .playlist-card {
                    background-color: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    padding: 10px;
                    width: 40%;
                }
                .playlist-card img {
                    width: 100%;
                    height: auto;
                    border-radius: 10px;
                }
                .playlist-card h3 {
                    margin: 10px 0;
                    font-size: 1.2rem;
                }
                .playlist-card h2{
                    margin: 10px 0;
                    font-size: 0.8rem;
                }
                .playlist-card p {
                    color: #555;
                    font-size: 0.9rem;
                }
                .playlist-card a {
                    text-decoration: none;
                    color: #007BFF;
                    font-weight: bold;
                }
                .playlist-card a:hover {
                    text-decoration: underline;
                }
                
                .description {
                    margin-top: 20px; 
                    padding: 10px;
                    font-size: 16px;
                    color: #333;
                    background-color: rgba(255, 255, 255, 0.7);
                    border-radius: 10px;
                    text-align: center;
                    width: 100%;
                    margin-left: auto;
                    margin-right: auto;
                    flex-direction: column;
                }
                
                .playlist-card:first-child {
                    scroll-margin-top: 100px;
                }

                .pale{
                    height: 50px;
                }
                
                .selectbutton{
                    margin-top: 10px;
                    padding: 10px 20px;
                    margin-left: 10px;
                    background-color: green;
                    color: black;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 700;
                }
                </style>'''
    body += '</head><body><div class="header"><h1>PlaylistMotion</h1></div>\n'
    body += '<div class="pale"></div><div class="pale"></div>'
    body += '<div><p class="description">\n<strong>## Please select the proper playlist. ##</strong>\n<strong>After selection, please wait 30 seconds for a pop-up window and pressing OK.</strong></p>\n'
    body += '</div><div class="pale"></div><div class="pale"></div>'
    for line in ll:
        if line[0] != '' and line[2]!='By Spotify':
            body += f'<div class="playlist-card">'
            body += f'<img src="{line[3]}" alt="Playlist Image">'
            body += f'<h3>{line[1]}</h3><p>Creator: {line[2]}</p><p><h2>{line[0]}</h2></p>'
            body += '<div class="pale"></div><button class="selectbutton" onclick="selectData(event)">Select</button>'
            body += '</div><div class="pale"></div>'
    body += '</body></html>'

    file_path = os.path.join(UPLOAD_FOLDER, 'sub.html')
    with open(file_path, 'w') as f:
        f.write(body)

    return send_file(file_path, mimetype='text/html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')

    task = analyze_task.apply_async(args=[text])

    return jsonify({'task_id': task.id}), 202 

from celery.result import AsyncResult

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id, app=celery)

    if task.state == 'PENDING':
        response = {'status': 'Pending', 'progress': None}
    elif task.state == 'PROGRESS':
        response = {'status': 'In Progress', 'progress': task.info}
    elif task.state == 'SUCCESS':
        response = {'status': 'Complete', 'result': task.info['result']}
    else:
        response = {'status': task.state, 'error': str(task.info)}

    return jsonify(response)

@app.route('/show_results', methods=['POST'])
def show_results():

    data = request.get_json()
    wordcloud_path = data.get('wordcloud_path')
    six_dimensions_path = data.get('six_dimensions_path')

    return render_template(
        'results.html', 
        word=wordcloud_path, 
        six=six_dimensions_path
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
