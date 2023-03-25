from flask import Flask, render_template, request, send_from_directory
from flask import Flask, request, Response
from flask_ngrok import run_with_ngrok

import os
import warnings
import json

import torch, torchvision
import numpy as np
from pytorch_grad_cam import GradCAM
import base64
import cv2
from PIL import Image



class SimilarityToConceptTarget:

    # Source: https://github.com/jacobgil/pytorch-grad-cam/blob/master/tutorials/Pixel%20Attribution%20for%20embeddings.ipynb

    def __init__(self, features):
        self.features = features
    
    def __call__(self, model_output):
        cos = torch.nn.CosineSimilarity(dim=0)
        return cos(model_output, self.features)
    

class GradCamScanner:
    def __init__(self, model, target, layers, device = 'cuda') -> None:
        self.model = model
        self.target = target
        self.target_layers = layers
        self.use_cuda = device == 'cuda'

    def scan(self, image):
        with GradCAM(model=self.model, target_layers=self.target_layers, use_cuda=False) as cam:
            return cam(input_tensor=image[None,], targets=[self.target])[0, :]  



html_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
app = Flask(__name__, template_folder='.')
warnings.warn("Be careful! This server isn't protected ad therefore should only be used in debugging; never in production.")
model = torchvision.models.resnet50(pretrained = 'imagenet').cuda()

@app.route('/<path:path>/<file>.<extension>')
def file(path, file, extension):
    return send_from_directory(html_dir, f"{path}/{file}.{extension}")

@app.route('/<path:path>/')
def route(path):
    return render_template(f"{path}/index.html")

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

@app.route('/', methods = ['POST'])
def index():

    # Get the file from the request
    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return 'errors.EmptyFileError'
    print(file)
    data = np.array(Image.open(file).convert('RGB').resize((224, 224)))
    print(data.shape)

    data = np.stack([data, np.roll(data, 10, 1), np.roll(data, -10, 1), np.roll(data, 10, 0), np.roll(data, -10, 0)]).transpose(0, 3, 1, 2).astype(np.uint8) / 255
    print(data.shape)
    data = torch.from_numpy(data).float().cuda()
    with torch.no_grad():
        out = torch.nn.functional.sigmoid(model(data)).cpu().numpy()
        response = [{'label': np.argmax(o), 'confidence': np.max(o), 'keywords': ['Not', 'Implemented', 'Yet']} for o in out]
    
    layers = list(model.modules())[:-5]
    concept = model(data)[0]
    scanner = GradCamScanner(model, SimilarityToConceptTarget(concept.detach()), layers)

    p = 0.61

    heatmap = scanner.scan(data[0])
    heatmap = 255 * (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    image = (255 * data[0].cpu().numpy().mean(0)) * (1 - p) + heatmap * p
    cv2.imwrite('tmp.png', image.astype(np.uint8))
    with open("tmp.png", "rb") as image_file:
        b64 = base64.b64encode(image_file.read()).decode()
    

    
    json_string = {'response': response, 'heatmap': b64 , 'aggregation': response[0]}

    response = Response(response=json.dumps(json_string, default=np_encoder), status=200, mimetype="application/json")
    # Add an 'Access-Control-Allow-Origin' header to the response to allow requests from any origin
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

ip = "localhost:8080" #"0.0.0.0:5000"
ip, port = ip.split(':')

run_with_ngrok(app)
app.run()
