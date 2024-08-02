# Welcome to the Music Monsoon - Weather based song recommendation Project


-This project was built to recommend songs to users based on the weather condition at their respective locations.

- This project is built with a CNN model that is used to predict the song genre of an audio file.

- First we utilize the Librosa library to extract the features of an audio file and we make use of the GTZAN genre music dataset to train the CNN model, which has filters of 32,64,125,256 to capture the features of the audio file/song , we further convert the input into a form that the CNN model can understand. We achieve this by flattening the present 2D array into a 1D array and build the CNN model

- We train the model on our train data, and compile the model and test it on our test data. (attained through a train test split on our GTZAN data).

- The model can then be used to predict the genres of audio files in the genres of => jazz, rock, pop, disco, hiphop, classical, metal, etc.

- Also included in a weather app built using javascript that uses WeatherAPI to determine the weather of a provided location.

- This project then uses the already build Deep learning model and the retrieved weather data and makes recommendations accordingly, the users can then listen to the songs of their choice based on the recommendation.

- This project was built mainly from my passion and love for music and songs, and hope that it brings more people to fall in love with the magic of music.
 
# Music Monsoon
