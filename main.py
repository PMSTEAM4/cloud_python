
# [START gae_python37_app]
from flask import Flask, request
import urllib.request
import logging
import os
import datetime
import uuid
import shutil


from artist import run_artist
from firebase import firebase 
firebase = firebase.FirebaseApplication('https://pickmyservice-fca10.firebaseio.com/', None)




import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('pickmyservice-fca10-firebase-adminsdk-s13ms-55e69462d4.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pickmyservice-fca10.appspot.com'
})

bucket = storage.bucket()

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    target_url = 'https://firebasestorage.googleapis.com/v0/b/pickmyservice-fca10.appspot.com/o/videoes%2Ftest.mp4?alt=media&token=61deca79-d532-47cd-841c-616fbabd8c68'
    urllib.request.urlretrieve(target_url, 'source.mp4')
    return 'Hello World!'

    
@app.route('/artist', methods=['POST'])
def generateArtist():
    url = request.form['url']
    providerId = request.form['providerId']
    urllib.request.urlretrieve(url, 'source.mp4')
    run_artist.videoStyles('source.mp4')
    saveInFirebase(providerId, 'animal')
    saveInFirebase(providerId, 'patterns')
    saveInFirebase(providerId, 'people')
    saveInFirebase(providerId, 'seaneries')
    return "200"

# @app.route('/upload', methods=['POST'])
# def save():
#     providerId = request.form['providerId']
#     saveInFirebase(providerId, 'animal')
#     saveInFirebase(providerId, 'patterns')
#     saveInFirebase(providerId, 'people')
#     saveInFirebase(providerId, 'seaneries')
#     return "200"


#upload the result to firebase and save the url in database
# def saveInFirebase(providerId):
#     saveName = '/' + uuid.uuid4().hex + '.jpg'
#     print(saveName)
#     blob = bucket.blob('gallery/'+ providerId + saveName)

#     # blob = bucket.blob('gallery/'+ providerId + '/animal2.jpg')
#     outfile = 'artist/gallery/animal/img_33.jpg'
#     result = blob.upload_from_filename(outfile)
#     app.logger.info('LOG Storage', blob)
#     blob.make_public()
#     app.logger.info('LOG Storage', blob.public_url)
#     putre = firebase.put('/Service_providersInformation/'+providerId+'/gallery/animal','image1', blob.public_url)
#     app.logger.info('LOG putre', putre)
#     return "200"

#upload the result to firebase and save the url in database - NEW
def saveInFirebase(providerId, imageType):
    path = 'artist/gallery/'+imageType
    files = os.listdir(path)
    if len(files) < 1:
        return "500"
    uploadFile = '/' + files[0]
    saveName = '/' + uuid.uuid4().hex + '.jpg'

    blob = bucket.blob('gallery/'+ providerId + saveName)
    outfile = path + uploadFile
    result = blob.upload_from_filename(outfile)
    blob.make_public()
    app.logger.info('LOG Storage', blob.public_url)
    putre = firebase.put('/Service_providersInformation/'+providerId+'/gallery/'+imageType,'image1', blob.public_url)    
    app.logger.info('LOG putre', putre)

    shutil.rmtree(path)
    os.mkdir(path)

    return "200"



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END gae_python37_app]
