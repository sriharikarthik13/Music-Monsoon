import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary 
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField,FileField,StringField
import pickle
import io
import librosa
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
#Using the librosa library to extract the MFCC(Mel-Frequency Cepstral Coefficients) from each of the provided .wav file in the GTZAN dataset
def extract_features(file_path, n_mfcc=40):
    audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
    return np.mean(mfccs.T, axis=0)

#Loading the CNN model
model =  pickle.load(open('./model_final.pickle',mode='rb'))
#Performing the preprocessing steps required to train the CNN model and extract features from the audio files.
label_encoder = LabelEncoder()
df = pd.read_csv('Music_Data.csv')
df['genre'] = label_encoder.fit_transform(df['genre'])
def song_genre(file_path):
    features = extract_features(file_path)
    features = features.reshape(1, -1, 1, 1)
    prediction = model.predict(features)    
    music_genre = label_encoder.inverse_transform([np.argmax(prediction)])
    return music_genre[0]

app = Flask(__name__)

app.config["SECRET_KEY"] = "key"
app.config['UPLOAD_FOLDER'] = "uploads"

##SQL SECTION

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)



class MusicDatas(db.Model):
    __tablename__ = "musicdata"
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String)
    song_genre = db.Column(db.String)
    song_file = db.Column(LargeBinary)


class MusicForm(FlaskForm):
    songinput = FileField('Image')
    submit = SubmitField('Submit')


#Setting up the flask views
@app.route('/')
def index():
    return render_template('home.html')



@app.route('/upload', methods=['GET','POST'])
def music_upload():
    db.create_all()
    form = MusicForm()
    if form.validate_on_submit():

        songfile = form.songinput.data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], songfile.filename)
        songfile.save(file_path)
        print(file_path)

        sg = song_genre(file_path)

        with open(file_path,'rb') as f:
            file_data = f.read()
        
        new_song = MusicDatas(song_name = songfile.filename,song_genre= sg ,song_file = file_data )
        db.session.add(new_song)
        db.session.commit()
        
        return render_template("download_success.html")

    return render_template("music_form.html",form = form)




@app.route('/download/<SongName>')
def download_song(SongName):
    song = MusicDatas.query.filter_by(song_name=SongName).first()
    print(f"song name in download {song.song_name}")
    return send_file(io.BytesIO(song.song_file), as_attachment=True, download_name=f"{song.song_name}.mp3", mimetype='audio/mpeg')


@app.route('/play/<song_name>')
def play_song(song_name):
    return render_template('audio_player.html', song_name=song_name)



@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/musiclist')
def musiclist():
    return render_template('musiclist.html')


@app.route('/sunny')
def sunny():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="rock").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="country").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="metal").all():
        lista.append(i.song_name)
    
    for i in MusicDatas.query.filter_by(song_genre="reggae").all():
        lista.append(i.song_name)


    return render_template('sunny.html',lista=lista)


@app.route('/snow')
def snow():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="pop").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="hiphop").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="classical").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="disco").all():
        lista.append(i.song_name)
    


    return render_template('snow.html',lista=lista)


@app.route('/rain')
def rain():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="jazz").all():
        lista.append(i.song_name)

    for i in MusicDatas.query.filter_by(song_genre="blues").all():
        lista.append(i.song_name)



    return render_template('rain.html',lista=lista)


@app.route('/classical')
def classical():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="classical").all():
        lista.append(i.song_name)
    return render_template('classical.html',lista=lista)

@app.route('/country')
def country():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="country").all():
        lista.append(i.song_name)
    return render_template('country.html',lista=lista)


@app.route('/hiphop')
def hiphop():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="hiphop").all():
        lista.append(i.song_name)
    return render_template('hiphop.html',lista=lista)

@app.route('/jazz')
def jazz():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="jazz").all():
        lista.append(i.song_name)
    return render_template('jazz.html',lista=lista)


@app.route('/rock')
def rock():
    lista=[]
    for i in MusicDatas.query.filter_by(song_genre="rock").all():
        lista.append(i.song_name)
    return render_template('rock.html',lista=lista)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"))
