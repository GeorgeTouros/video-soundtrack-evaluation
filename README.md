# Evaluation of Video Soundtracks using Machine Learning
### Addressing the issues of data availability, feature extraction and classification

This repo is created for my thesis, to complete my MSc in Data Science, 
from the University of Peloponnese and NCSR Demokritos. 

![Data Science](/var/graphs/dpms-logo.jpg)

## Objective
The aim of this thesis is to address the challenges of combining multimodal data to evaluate video soundtracks. 
To tackle tasks in the field of soundtrack generation, retrieval, or evaluation, data needs to be collected from 
as many relevant modalities as possible, such as audio, video, and symbolic representations of music. 
We propose a method of collecting relevant data from all of these modalities, and from them, we attempt to describe 
and extract a comprehensive multimodal feature library. We construct a database by applying our method on a small 
set of available data from the three relevant modalities. We implement and tune a classifier in our constructed 
database of features with adequate results. The classifier attempts to discriminate between real and fake examples of 
video soundtracks. 

## Repo Structure

* config: the central position of settings, paths and credentials
  * credentials.py is where the credentials are stored for interacting with external APIs (database, Spotify etc.).
  * paths.py is where all the paths are stored for data inputs and outputs, as well as for temporary folders.
  * settings.py is where the parameters for audio and video processing are stored. These include: 
    * CHUNK_SIZE_SECONDS: the size of the chunks for audio recognition within video files in seconds.
    * CHUNK_SIZE_MS: the size of the chunks for audio recognition within video files in milliseconds (for direct use 
      within ffmpeg).
    * SAMPLE_RATE: the sample rate used for fingerprinting as well as for parsing audio files
    * CHANNELS: set 1 for mono and 2 for stereo.
    * BATCH_SIZE: the number of video files processed in each batch.
    * AUDIO_FILE_TYPE: the output type for audio files. 
  * db_handler: contains db_handler.py wherein exists the DatabaseHandler class, a wrapper class around the 
    [sqlalchemy](https://www.sqlalchemy.org/) package. This class is used for invoking database operations, such as 
    creating databases, tables, inserting lines, deleting schemas, tables, lines and simple queries. 
    *  feature_extractor: contains three modules with classes that extract features for each of the modalities of interest. 
        *  audio_features.py, which contains the AudioFeatureExtractor class. 
        *  video_features.py, which contains the VideoFeatureExtractor class. 
        *  symbolic_features.py, which contains the SymbolicFeatureExtractor class. 
    *  fingerprinting: contains djv.py which has the wrapper functions around the 
       [pyDejavu](https://github.com/worldveil/dejavu) library, for fingerprinting.  
    *  media_manipulation: a module that contains all the scripts for manipulating audio and video data.
        *  audio_conversions.py: includes wrapper functions for invoking ffmpeg commands to convert audio files into 
           the appropriate format for fingerprinting. 
        *  song_retrieval.py: contains all the functions needed to search within a video for songs. 
        *  video_manipulation.py: includes wrapper functions for invoking ffmpeg commands to crop videos and mix audio with video.
    *  spotify_wrapper: includes a wrapper class around the [spotipy](https://spotipy.readthedocs.io/en/2.16.1/) 
       library. We use this class to retrieve information on song titles, during the matching of audio and MIDI files.
    *  utils: a module containing various utilities for the all the other modules and scripts. These include:
        *  catalog_utils.py: which contains utility functions for scanning folder directories and creating catalog 
           entries within the database. 
        *  common_utils.py: which contains utility functions for time calculations, and other miscellaneous tasks.
    
## Pipeline and order of execution

![data collection](/var/graphs/Data%20Collection.png)

![Feature Extraction](/var/graphs/Feature%20Extraction.png)

## Dependencies with 3rd Party Libraries

All code is written in Python, bash and SQL, run and tested in Ubuntu Linux 20.04. 
There are some dependencies with 3rd party software beyond those that are mentioned in requirements.txt 
These are:
* [ffmpeg](https://ffmpeg.org/): A complete, cross-platform solution to record, convert and stream audio and video. 
* [MySQL](https://www.mysql.com/): An open-source database
* [Cuda Toolkit](https://developer.nvidia.com/cuda-downloads) (optional) If available, it would speed up the 
  extraction of visual features.
* [MuseScore 3](https://musescore.org/en): an open source software for visualizing MusicXML files. 
* [FluidSynth](http://www.fluidsynth.org/): a real-time software synthesizer based on the SoundFont 2 specifications
* [QjackCtl](https://qjackctl.sourceforge.io/): a simple Qt application to control the JACK sound server daemon, 
  specific for the Linux Audio Desktop infrastructure. 
* [QSynth](https://qsynth.sourceforge.io/): a fluidsynth GUI front-end application written in C++ around the Qt 
  framework using Qt Designer.
* [lilypond](http://lilypond.org/): a music engraving program, devoted to producing the highest-quality sheet music 
  possible. We use it for some of the visualizations of sheet music in this thesis. 

The MIDI data that we used comes from [composing.ai](https://composing.ai/dataset). MP3 and video data came from a 
personal collection. 

## The Spotify API
In order to match the audio and MIDI files, we needed to use a knowledge base that could provide a ground truth for song information. We chose the popular music streaming platform [Spotify](www.spotify.com). The platform provides a web-based API, which we access using the relevant Python library [spotipy](https://spotipy.readthedocs.io/en/2.16.1/). To run the code it is necessary to set up a free account in order to complete the user authorization in each call. An app needs to be registered at [MyDashboard](https://developer.spotify.com/documentation/web-api/) to get the credentials necessary to make authorized calls (a client id and client secret). In order to achieve the maximum reply rate possible, we used the client credentials authorisation flow. These credentials are stored in the file config/credentials.py.

The class that we have created, named _Spotify_, is a rudimentary wrapper class. It exposes the functions that are useful for the matching process, namely the song searching function, that returns a song name and metadata. 
