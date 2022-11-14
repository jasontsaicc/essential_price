# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D, MaxPooling2D, BatchNormalization
# from tensorflow.keras.models import Model
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.callbacks import ReduceLROnPlateau
# from sklearn.model_selection import train_test_split
# import os, shutil
# from sklearn.preprocessing import LabelEncoder
# from keras.models import model_from_json, load_model

# test_i = './test_img/linmilk._2.jpg'

def milk_model(test_i):
	new_model = tf.keras.models.load_model('./model_0830.h5')
	new_model.compile(
		optimizer='adam',
		loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
		metrics=['accuracy']
	)

	test_img = []

	# test_i = './test_img/linmilk._2.jpg'
	# test_i = cv2.imread(test_i)
	# print(test_i)
	test_i = cv2.resize(test_i, (256, 256))
	test_img.append(np.array(test_i))
	test_img = np.array(test_img)

	new_model.predict(test_img)
	brand = {'義美全脂鮮乳': 0, '林鳳營全脂鮮乳': 1, '乳香世家鮮乳': 2, '福樂一番鮮特極鮮乳': 3, '光泉鮮乳': 4,
			 '瑞穗全脂鮮奶': 5, '瑞穗全脂鮮奶': 6, '瑞穗低脂鮮奶': 7, '瑞穗低脂鮮奶': 8}
	result = np.argmax(new_model.predict(test_img), axis=1)

	if result[0] == brand['義美全脂鮮乳']:
		return '義美全脂鮮乳'
	elif result[0] == brand['林鳳營全脂鮮乳']:
		return '林鳳營全脂鮮乳'
	elif result[0] == brand['乳香世家鮮乳']:
		return '乳香世家鮮乳'
	elif result[0] == brand['福樂一番鮮特極鮮乳']:
		return '福樂一番鮮特極鮮乳'
	elif result[0] == brand['光泉鮮乳']:
		return '光泉鮮乳'
	elif result[0] == brand['瑞穗全脂鮮奶']:
		return '瑞穗全脂鮮奶'
	elif result[0] == brand['瑞穗全脂鮮奶']:
		return '瑞穗全脂鮮奶'
	elif result[0] == brand['瑞穗低脂鮮奶']:
		return '瑞穗低脂鮮奶'
	elif result[0] == brand['瑞穗低脂鮮奶']:
		return '瑞穗低脂鮮奶'


if __name__=='__main__':
	milk_model()
