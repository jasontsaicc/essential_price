import numpy as np
import tensorflow as tf
import cv2
import os


def image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype(np.float32)
    img_array = []
    img_array.append(img)
    img_array = np.asarray(img_array)
    return img_array

def predict(img_path):
    img = image(img_path)

    model_pred= tf.lite.Interpreter('./tflite_model.tflite')
    model_pred.allocate_tensors()
    input_index = model_pred.get_input_details()[0]["index"]
    output_index = model_pred.get_output_details()[0]["index"]

    model_pred.set_tensor(input_index, img)
    model_pred.invoke()

    output_data = model_pred.get_tensor(output_index)
    x = np.where(output_data == 1)

    brand = {'iMeiMilk': 0, 'LimFengInMilk': 1, 'JuHsiangMilk': 2, 'FreshDelightMilk': 3, 'KuangChuanMilk': 4, 
        'LargeReiSuiMilk': 5, 'SmallReiSuiMilk': 6, 'LowFatLargeReiSuiMilk': 7, 'LowFatSmallReiSuiMilk': 8}

    for i in brand:
        idx = brand[i]
        if idx == x[1]:
            print("Prediction:", i)


path = './test_pic'
for i in os.listdir(path):
    img_path = path + f"/{i}"
    print(i)
    predict(img_path)