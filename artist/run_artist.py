import cv2
import os
import shutil 
import os.path
from os.path import isfile, join
import numpy as np
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing import image
from keras.models import load_model
from keras import backend as K
K.set_image_dim_ordering('tf')
import tensorflow as tf

classifier_path = 'artist/InceptionResNetV2_model.h5'
classifier = load_model(classifier_path)
global graph
graph = tf.get_default_graph() 

model = InceptionResNetV2(weights='imagenet', include_top=False )

img_directory = 'artist/images/'
num = 0
count = 0
animal = os.path.abspath('artist/gallery/animal')
patterns = os.path.abspath('artist/gallery/patterns')
people = os.path.abspath('artist/gallery/people')
seaneries = os.path.abspath('artist/gallery/seaneries')


def predict(file):
    x = image.load_img(file, target_size=(150,150))
    x = image.img_to_array(x)
    x = x/255
    x = np.expand_dims(x, axis=0) 
    with graph.as_default():
        features = model.predict(x)
        result = classifier.predict_classes(features)
        if result[0] == 0:
            prediction = 'animal'
        elif result[0] == 1:
            prediction = 'patterns'
        elif result[0] == 2:
            prediction = 'people'
        elif result[0] == 3:
            prediction = 'seaneries'   
    return prediction
     

def videoStyles(file):
    global count, head, code,slide, num
    cap = cv2.VideoCapture(file)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        num += 1
        name = 'artist/images/img_' + str(num) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)
        
        
    cap.release() # Creating image frames from video
    
    list_img = os.listdir(img_directory)
    
    for img in list_img:
        temp = predict(img_directory+img)
        if temp == 'animal':
            shutil.move(os.path.abspath(img_directory+img),animal)
        elif temp == 'patterns':
            shutil.move(os.path.abspath(img_directory+img),patterns)
        elif temp == 'people':
            shutil.move(os.path.abspath(img_directory+img),people)
        elif temp == 'seaneries':
            shutil.move(os.path.abspath(img_directory+img),seaneries)
            
def test():
    return "Hello ANjana"







