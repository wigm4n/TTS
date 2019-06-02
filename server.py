# -*- coding: utf-8 -*-

import os

from flask import Flask, send_file, make_response
from flask import request
from flask import jsonify
import threading
import time
import requests

from text_processing.dictionary import Preprocessing as prp
from audio_processing.synthesize import start_process
from utils import create_json_error_response

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
                time.sleep(1)

    thread = threading.Thread(target=start_loop)
    thread.start()


@app.route('/check')
def check():
    data = {"status": "OK"}
    return make_response(jsonify(data), 200)


@app.route('/get_words', methods=['POST'])
def get_words():
    if request.method == 'POST':
        prepared_text = word_processing.process_input_text(request.json.get("input"))
        data = {"text": str(prepared_text)}
        return jsonify(data)


@app.route('/get_audio', methods=['POST'])
def get_audio():
    if request.method == 'POST':
        flag = 0
        try:
            print("files in sounds/all: " + str(len(os.listdir(os.getcwd() + "/static/sounds/all/")) - 1))
            prepared_text = word_processing.process_input_text(request.json.get("input"))
            if len(prepared_text) < 1:
                return make_response(jsonify(create_json_error_response("wrong input data, see api description")), 422)
            flag = 1
            saved_path, file_name = start_process(request.json.get("input"), prepared_text)
            file_name_wav = file_name + '.wav'
            return make_response(send_file(saved_path, attachment_filename=file_name_wav), 200)
        except Exception as e:
            if flag == 0:
                return make_response(jsonify(create_json_error_response("wrong input data, see api description")), 422)
            # somethings goes wrong, try later
            return make_response(jsonify(create_json_error_response(repr(e))), 500)


@app.errorhandler(404)
def url_path_not_found(e):
    return make_response(jsonify(create_json_error_response("wrong url path, see api description")), 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(create_json_error_response("http method not allowed, see api description")), 405)


if __name__ == '__main__':
    port = 5000 if cf_port is None else int(cf_port)
    start_runner(port)
    app.run(host='0.0.0.0', port=port, debug=True)
