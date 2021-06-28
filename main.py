import base64
from flask import Flask, render_template, request, redirect, url_for
import json
from werkzeug.utils import secure_filename


app = Flask(__name__)

name = '';


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/homepage')
def homepage(email=None):
    return render_template('homepage.html', email=email)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def do_login():
    email = request.form.get('email')
    data = open('signup-cred.json', 'r')
    signuplist = json.load(data)
    for x in signuplist:
        print(x)
        if x.get('email') == email:
            return render_template('face-verify.html')
    return render_template('login.html')


@app.route("/signup", methods=['POST'])
def do_signup():
    email = request.form.get('email')
    username = request.form.get('userName')
    password = request.form.get('password')
    global name
    name = username
    with open('signup-cred.json', 'r+') as f:
        data = json.load(f)
        data.append({
            "name": username,
            "email": email,
            "password": password
        })
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return redirect(url_for('upload'))


@app.route('/upload', methods=["GET"])
def upload():
    if len(name) > 0:
        return render_template('upload.html')
    else:
        return render_template('index.html')


@app.route('/upload', methods=['POST'])
def do_upload():
    image = request.form.get('image')
    global name
    if len(image) > 0:
        file_encode = bytes(image, 'utf-8')
        with open("signup-images\\" + name + ".png", "wb") as fh:
            fh.write(base64.decodebytes(file_encode))
    else:
        file = request.files['file']
        file.save(f"signup-images\\{secure_filename(file.filename)}")
    name = ''
    return redirect(url_for('homepage'))


@app.route('/face-verify', methods=["GET"])
def face_verify():
    return redirect(url_for('login'))


@app.route('/face-verify', methods=['POST'])
def do_face_verify():
    image = request.form.get('image')
    file_encode = bytes(image, 'utf-8')
    with open("login-images\\file.png", "wb") as fh:
        fh.write(base64.decodebytes(file_encode))
    return redirect(url_for('homepage'))


