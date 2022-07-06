from flask import Flask, render_template, request, send_from_directory
import os
import warnings
import json

html_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
app = Flask(__name__, template_folder='.')
warnings.warn("Be careful! This server isn't protected ad therefore should only be used in debugging; never in production.")

@app.route('/<path:path>/<file>.<extension>')
def file(path, file, extension):
    return send_from_directory(html_dir, f"{path}/{file}.{extension}")

@app.route('/<path:path>/')
def route(path):
    return render_template(f"{path}/index.html")

@app.route('/')
def index():
    return render_template(f"index.html")

ip = "0.0.0.0:5000"
ip, port = ip.split(':')

app.run(host=ip, port = int(port[:]), debug = True)
