import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def midi_header():
    return "midi_id", "directory", "filename", "title", 'spotify_name', 'spotify_artist', 'spotify_URL'


def audio_header():
    return "audio_id", "directory", "filename", "title", 'spotify_name', 'spotify_artist', 'spotify_URL'


class Audio(Base):
    __tablename__ = 'audio'
    audio_id = sql.Column("audio_id", sql.Integer, primary_key=True)
    audio_path = sql.Column("directory", sql.String)
    audio_filename = sql.Column("filename", sql.String)
    audio_title = sql.Column("title", sql.String)
    audio_sp_name = sql.Column("spotify_name", sql.String)

    def __init__(self, audio_id="", audio_features="", audio_path=""):
        self.audio_id = audio_id
        self.audio_features = audio_features
        self.audio_path = audio_path

    def __repr__(self):
        return "{audio_id}, {audio_features}, {path}".format(
            path=self.audio_path,
            audio_features=self.audio_features,
            audio_id=self.audio_id)

    def get_row(self):
        return self.audio_id, self.audio_features, self.audio_path


class Clip(Base):
    __tablename__ = 'clips'
    clip_id = sql.Column(sql.String, primary_key=True)
    clip_description = sql.Column(sql.String)
    clip_title = sql.Column(sql.String)
    url = sql.Column(sql.String)
    mismatch_title = sql.Column(sql.String)
    mismatch_url = sql.Column(sql.String)
    start_time = sql.Column(sql.Integer)
    end_time = sql.Column(sql.Integer)
    clip_path = sql.Column(sql.String)
    video_features = sql.Column("video_features", sql.String)
    audio_from_clip = sql.Column(
        sql.String)

    def __init__(self,
                 clip_id="",
                 url="",
                 start_time=0,
                 end_time=0,
                 clip_title="",
                 clip_description="",
                 clip_path="",
                 video_features="",
                 audio_from_clip="",
                 mismatch_url="",
                 mismatch_title=""):
        self.clip_id = clip_id
        self.clip_description = clip_description
        self.clip_title = clip_title
        self.url = url
        self.start_time = start_time
        self.end_time = end_time
        self.clip_path = clip_path
        self.video_features = video_features
        self.audio_from_clip = audio_from_clip
        self.mismatch_title = mismatch_title
        self.mismatch_url = mismatch_url

    def __repr__(self):
        return "{id}, {url}, {start_time}, {end_time}," \
               "{title}, {descr}, {path}, {feat}, {audio}".format(id=self.clip_id,
                                                                  title=self.clip_title,
                                                                  start_time=self.start_time,
                                                                  end_time=self.end_time,
                                                                  descr=self.clip_description,
                                                                  url=self.url,
                                                                  path=self.clip_path,
                                                                  feat=self.video_features,
                                                                  audio=self.audio_from_clip)

    def get_row(self):
        return (self.clip_id, self.url, self.clip_title, self.clip_description, self.clip_path,
                self.video_features, self.audio_from_clip)


class Feature(Base):
    __tablename__ = 'features'
    features_type = sql.Column(sql.String, primary_key=True)
    feature_names = sql.Column(sql.String)

    def __init__(self, features_type, feature_names=""):
        self.features_type = features_type
        self.feature_names = feature_names

    def get_row(self):
        return self.features_type, self.feature_names


class UserEvaluation(Base):
    __tablename__ = 'user evaluation'
    clip_id = sql.Column(sql.String, primary_key=True)
    clip_title = sql.Column(sql.String)
    url = sql.Column(sql.String)
    start_time = sql.Column(sql.Integer)
    # start time + 20 from download_video_from_url
    end_time = sql.Column(sql.Integer)
    clip_path = sql.Column(sql.String)
    video_features = sql.Column("video_features", sql.String)
    audio_id = sql.Column(sql.String)
    voted_model = sql.Column(sql.Integer)

    def __init__(self,
                 clip_id="",
                 url="",
                 start_time=0,
                 end_time=0,
                 clip_title="",
                 clip_path="",
                 video_features="",
                 audio_id="",
                 voted_model=""):
        self.clip_id = clip_id
        self.clip_title = clip_title
        self.url = url
        self.start_time = start_time
        self.end_time = end_time
        self.clip_path = clip_path
        self.video_features = video_features
        self.audio_id = audio_id
        self.voted_model = voted_model

    def __repr__(self):
        return "{id}, {url}, {start_time}, {end_time}," \
               "{title}, {path}, {feat}, {audio}, {model}".format(id=self.clip_id,
                                                                  title=self.clip_title,
                                                                  start_time=self.start_time,
                                                                  end_time=self.end_time,
                                                                  url=self.url,
                                                                  path=self.clip_path,
                                                                  feat=self.video_features,
                                                                  audio=self.audio_id,
                                                                  model=self.voted_model)

    def get_row(self):
        return (self.clip_id, self.url, self.clip_title, self.clip_path, self.video_features, self.audio_id,
                self.voted_model)