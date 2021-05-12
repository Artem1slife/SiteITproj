from flask import render_template, request
from app_block import app, firebase, auth
import json
from app_block.txt_handler import TextHandlerFrequency, TextHandlerSemantic, TextHandlerCloud

import urllib
import base64
import matplotlib.pyplot as plt

from werkzeug.utils import secure_filename

MAX_FILE_SIZE = 16 * 1024 * 1024

storage = firebase.storage()


@app.route('/api/<username>')
def userinfo(username):
    return 200


@app.route('/', methods=['GET', 'POST'])
def sign_in():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('new.html', s=successful)
        except:
            return render_template('new.html', us=unsuccessful)
    return render_template('new.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return 200
    return render_template('create_account.html')

@app.route('/upload/<username>/<file>', methods=['POST'])
def upload_file(username, file):
    path = '/bucketname/' + str(secure_filename(file.filename))
    if file:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
        except Exception as e:
            console.log('error uploading user photo: ' % e)
    return "thanks"


@app.route('/api/frequency_analysis', methods=['GET'])
def frequency_analysis():
    txthandler = TextHandlerFrequency()
    textes = ["text.txt", "text2.txt"]
    result = txthandler.frequency_analysis(textes)
    return json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


@app.route('/comparison_frequency_analysis/<username>/<cloudfilename>', methods=['GET'])
def comparison_frequency_analysis(username, cloudfilename):
    url = storage.child(username).child(cloudfilename).get_url(None)
    f = urllib.request.urlopen(url).read()
    f_str = f.decode('utf-8')
    # f = urllib.request.urlopen(url).read()
    txthandler = TextHandlerFrequency()
    # textes = ["text.txt", "text2.txt"]
    textes = []
    textes.append(f_str)
    result = txthandler.comparison_frequency_analysis_str(textes)
    return json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


@app.route('/api/comparison_semantic_analysis', methods=['GET'])
def comparison_semantic_analysis():
    txthandler = TextHandlerSemantic()
    textes = ["text.txt", "text2.txt"]
    result = txthandler.comparison_semantic_analysis(textes)
    df = result.to_json(force_ascii=False)
    df_html = result.to_html()
    return df_html


@app.route('/api/semantic_analysis', methods=['GET'])
def semantic_analysis():
    txthandler = TextHandlerSemantic()

    textes = ["text.txt", "text2.txt"]
    result = txthandler.semantic_analysis(textes)

    return json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


@app.route('/api/WordCloud', methods=['GET'])
def WordCloud():
    txthandler = TextHandlerCloud()

    result = txthandler.WordCloud("FatDAta - это программа. Она работает. Мммм работа")
    plt.imshow(result, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('saved_figure.png')
    image = open('saved_figure.png', 'rb')  # open binary file in read mode
    image_read = image.read()
    base64image = base64.b64encode(image_read)
    return base64image


@app.route('/get_tf_idf_query_similarity/<username>/<cloudfilename>', methods=['GET'])
def get_tf_idf_query_similarity(username, cloudfilename):
    url = storage.child(username).child(cloudfilename).get_url(None)
    f = urllib.request.urlopen(url).read()
    f_str = f.decode('utf-8')
    txthandler = TextHandlerSemantic()
    textes = []
    textes.append(f_str)
    # textes = ["Как работает эта программа! А я понял! Она берет текст и обрабатывает его, чтобы выдать корректный результат. Здорово!",
    # "FatDAta - это программа. Она обрабатывает текст и возвращает корректный результат. Я понял как она работает. Здорово...",
    # "FatDAta... Как работает эта программа! А я понял! СПАСИБО", "FatDAta - это программа. Она обрабатывает текст и возвращает корректный результат. Я понял как она работает. Здорово..."]
    result = txthandler.get_tf_idf_query_similarity(textes)
    js_result = result.to_json(force_ascii=False)
    return result.to_html()
