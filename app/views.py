from flask import render_template
from flask import Flask, request, render_template, session, redirect, flash, url_for, send_from_directory
import numpy as np
import pandas as pd
from app import app
import os
from werkzeug.utils import secure_filename
import numpy as np #Converts the image into an array
from keras.preprocessing import image
import tensorflow as tf
from keras.models import load_model
import os

BASE_DIR = os.getcwd()
UPLOADS = f"{BASE_DIR}/app/static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOADS

MODEL = f"{BASE_DIR}/model"
loadModel = load_model(f"{MODEL}/Student_Engagement_Model.h5")

print(BASE_DIR)
print(MODEL)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify(sample):
    print(f"{BASE_DIR}/{sample}")
    test_image = image.load_img(f"{BASE_DIR}/app/{sample}", target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = loadModel.predict(test_image/255.0)
    return result[0][0]


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/app')
def application():
    return render_template("app.html", display = 'False')

@app.route('/sourcecode')
def sourceCode():
    return render_template("source.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = classify(url_for('static', filename=f"uploads/{filename}"))
            if result > 0.5:
              prediction = 'Not Engaged'
            else:
              prediction = 'Engaged'
            return render_template("app.html", display = 'True', image=f"uploads/{filename}", confidence = result, prediction = prediction)
