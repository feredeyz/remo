from flask import Flask, render_template, request
from ..functions import load_config
import subprocess as sp

# uncomment to disable werkzeug logging
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)
CONFIG_PATH = "config.json"
config = load_config(CONFIG_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proceed', methods=["POST"])
def proceed_command():
    command = request.json['command']
    if command in config['dangerous']:
        return {"output": "Ай-ай-ай!! Опасная команда"}, 200
    try:
        result = sp.run(command, shell=True, capture_output=True, text=True).stdout.strip()
        return {"output": result}, 200
    except Exception as e:
        return {"output": f"Ошибка: {str(e)}"}, 400

def run_server():
    """
    Функция запуска Flask-сервера.
    """
    app.run(host='0.0.0.0', port=5000)
