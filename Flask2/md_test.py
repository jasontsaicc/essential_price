import numpy as np
import cv2
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.model_selection import train_test_split
import os, shutil
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json, load_model


def milk_model(test_i):
	new_model = tf.keras.models.load_model('./my_model.h5')
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
	result = np.argmax(new_model.predict(test_img), axis=1)


	if result[0] == 0:
		re = "林鳳營"
	elif result[0] == 1:
		re = "乳香世家"
	elif result[0] == 2:
		re = "義美"
	elif result[0] == 3:
		re = "瑞穗"
	elif result[0] == 4:
		re = "福樂"
	else:
		re = "我不知道"

	return re



if __name__=='__main__':
	milk_model()
