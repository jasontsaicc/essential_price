import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory, render_template
import numpy as np
import tempfile
import cv2
from md_test import milk_model
import tensorflow as tf


cv2.imdecode
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file'].read()
        file = np.fromstring(file, np.uint8)
        file = cv2.imdecode(file, cv2.IMREAD_COLOR)

        img = cv2.resize(file, (224, 224))
        img = img.astype(np.float32)
        img_array = []
        img_array.append(img)
        img_array = np.asarray(img_array)
        
        result = predict(img_array)
        


        return redirect(url_for('uploaded_file', filename=result))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

#
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('result.html', filename=filename)

def predict(img_array):
    
    img = img_array
    model_pred= tf.lite.Interpreter('./tflite_model.tflite')
    model_pred.allocate_tensors()
    input_index = model_pred.get_input_details()[0]["index"]
    output_index = model_pred.get_output_details()[0]["index"]

    model_pred.set_tensor(input_index, img)
    model_pred.invoke()

    output_data = model_pred.get_tensor(output_index)
    print(output_data)
    x = np.argmax(output_data)

    brand = {0: '義美全脂鮮乳', 1: '林鳳營全脂鮮乳', 2: '乳香世家鮮乳', 3: '福樂一番鮮特極鮮乳', 4: '光泉鮮乳', 
            5: '瑞穗全脂鮮奶', 6: '瑞穗全脂鮮奶', 7: '瑞穗低脂鮮奶', 8: '瑞穗低脂鮮奶'}

    for i in brand:
        if i == x:
            pd_name = brand[i]
            print("Prediction:", pd_name)
    return pd_name



if __name__ == '__main__':
    app.run(debug=True)
