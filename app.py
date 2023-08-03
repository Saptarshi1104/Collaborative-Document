import os
from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC63a912284e734e7648f9efcc4c67e984'
    TWILIO_SYNC_SERVICE_SID = 'IS69d2e8bd7599e338f7093e2412555098'
    TWILIO_API_KEY = 'SK5be847e41408e1253a72b8ed49876974'
    TWILIO_API_SECRET = 'GUbp78iHuVyngAEIS0550JSJEV6NCBlb'
    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)
    path_to_store_txt = "workfile.txt"
    return send_file(path_to_store_txt, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)