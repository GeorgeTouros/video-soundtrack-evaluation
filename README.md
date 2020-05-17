# Data-Set Creation for the Task of Music Composition for Videos

## Objective
We are trying to build a dataset that can tackle the task of music composition for films and videos 
with deep learning. The task is challenging, as there are multiple ways to compose music through deep 
learning, yet conditioning on features from other modalities, such as video, is not trivial. Some approaches, 
usually based on recurrent networks and autoencoders, need symbolic representations of music (such as a music sheet, 
or MIDI), and others, such as WaveNet and Transformer models, work directly on raw audio or on combinations
of symbols and audio.  
There is an abundance of audio, video and midi files, but so far we haven't been able to find some accurate 
combination of all three. 
## Challenges 
The main challenge has been the combination of audio, midi and video, given the fact that for a deep 
learning model to work, massive amounts of data are usually needed. We therefore set out to build a large, 
open source dataset, that will accommodate the following traits:  
* Large enough size to train some deep architecture
* Scalable method of obtaining the data
* Application of relevant data augmentation methods
* Appropriate data management techniques that will ensure re-usability and
scalability
## Approach 
Most of the approaches use either RNNs or Variational Autoencoders (or some combination of both), and 
in all of these cases a symbolic representation of music is needed (i.e. a representation of notes and 
note-length). The most common way to get that symbolic representation is by using MIDI files, a common 
format for music encoding since the 80's. These models are usually trained on massive data-sets that are 
in most cases relative to either classical music, or pop/rock songs. The latter case is of interest to us, as 
these types of songs are often used as soundtracks in popular films.  
To that end, we used the midi data-set that can be found [here](https://composing.ai/dataset) 
*(last retrieved on 2020-05-02)*. The main problem of this dataset, is it's lack of
structure. The files come from different data sources, using different naming 
conventions and directory structures, making it quite hard to determine which songs
are actually available in this directory. 
In order to tackle this issue, we created a cataloging script 
[catalog_work.py](https://github.com/GeorgeTouros/thesis_dataset_creation/blob/master/catalog_work.py) 
that goes through the directories and uses RegEx to ignore irrelevant filenames. We then
use a combination of RegEx and the Spotify API in order to get the proper name of each MIDI 
filename, as well as relevant artist and URL information. The match rate is currently at 61%.

The resulting MIDI file set is useful, but comes with its own limitation for the task at hand, 
which has to do with the fact that it mostly consists of know pop and rock songs. While a lot of 
films use these as background music for montages, due to the fact that they are usually expensive to 
obtain, this limits the pool of films and scenes we can draw from. Films usually also have their own
score, which is unique to the film and in most cases carries the bulk of the scenes and the emotional 
core of the film. Nevertheless, as this is the only large enough file set of MIDI files that we could
find for free, we decided to work with this. 

We then used the Spotify API to get the songs that are featured in well-known films, in 
[get_soundtracks.py](https://github.com/GeorgeTouros/thesis_dataset_creation/blob/master/get_soundtracks.py).
We started from a list of films that we already know use mainly pop and rock songs, in order to 
increase our chances of having them in our MIDI fileset. Usually the songs that are used come in compilation 
albums, but these are not always published in their entirety due to copyright issues. We overcame this 
problem using the community-based Spotify playlists, that are created by common users, and in most cases 
are more complete than the official compilation albums for the film soundtracks. In order to get the most
relevant playlist, we used filtering and appropriate RegEx. 

Having used the same source for the ground truth of a song's identity (Spotify), we then proceed to query
our MIDI fileset using the film soundtracks. The match rate is currently at 25%. 
 