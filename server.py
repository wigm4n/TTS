# -*- coding: utf-8 -*-

import os

from flask import Flask, send_file
from flask import request
from flask import jsonify
import threading
import time
import requests

from dictionary import Preprocessing as prp

app = Flask(__name__)

cf_port = os.getenv("PORT")
word_processing = prp()


@app.before_first_request
def activate_job():
    def run_job():
        word_processing.prepare_dictionaries()

    thread = threading.Thread(target=run_job)
    thread.start()


def start_runner(init_port):
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('http://127.0.0.1:' + str(init_port) + '/check')
                if r.status_code == 200:
                    not_started = False
            except:
                time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()


@app.route('/check')
def check():
    data = {"status": "OK"}
    return jsonify(data)


@app.route('/get_words', methods=['POST'])
def get_words():
    if request.method == 'POST':
        prepared_text = word_processing.process_input_text(request.json.get("input"))
        data = {"text": str(prepared_text)}
        return jsonify(data)


@app.route('/get_audio', methods=['POST'])
def get_audio():
    if request.method == 'POST':
        project_path = os.path.dirname(__file__)
        complete_name = project_path + "/samples/19.wav"
        return send_file(complete_name, attachment_filename='19.wav')


if __name__ == '__main__':
    port = 5000 if cf_port is None else int(cf_port)
    start_runner(port)
    app.run(host='0.0.0.0', port=port, debug=True)
