import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect,url_for,render_template,request, jsonify
from pymongo import MongoClient
from datetime import datetime

# URL = "mongodb+srv://aryogmeet:12345aryo@cluster0.rbtnrar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(URL)
# db = client.dbaryo
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    # Add 'file' attribute explicitly to each article
    for article in articles:
        article['file'] = article.get('file', '')  # Use get() to avoid KeyError if 'file' is not present
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]

    # Construct file paths
    filename = f'static/post-{mytime}.{extension}'
    profile = request.files['profile_give']
    profile_extension = profile.filename.split('.')[-1]
    profile_filename = f'static/profile-{mytime}.{profile_extension}'

    # Save files
    file.save(filename)
    profile.save(profile_filename)

    doc = {
        'file': filename,
        'profile': profile_filename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)