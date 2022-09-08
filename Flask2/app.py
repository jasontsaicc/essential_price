import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory, render_template
import numpy as np
import tempfile
import cv2
from md_test import milk_model
from perdiction import image, predict

# 檔案上傳的路徑
UPLOAD_FOLDER = './test_img/'


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file'].read()
        file = np.fromstring(file, np.uint8)
        file = cv2.imdecode(file, cv2.IMREAD_COLOR)[:, :, ::-1]
        milk_model(file)
        result = milk_model(file)


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


if __name__ == '__main__':
    app.run(debug=True)
