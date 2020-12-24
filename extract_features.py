from feature_extractor.audio_features import AudioFeatureExtractor
from feature_extractor.visual_features import VisualFeatureExtractor
from feature_extractor.symbolic_features import SymbolicFeatureExtractor
from db_handler.db_handler import DatabaseHandler
import pandas as pd
from media_manipulation.video_manipulation import video_chunker
from utils.catalog_utils import purge_temp_folder, get_temp_directory

if __name__ == '__main__':

    db = DatabaseHandler('file_system_catalogs')
    db_connection = db.connection
    feat_tables = ['audio_features', 'video_features', 'symbolic_features']
    for table in feat_tables:
        if not db.check_for_existing_tables(table=table):
            db.execute_from_file('./db_handler/sql/create_' + table + '_table.sql')

    temp_folder = get_temp_directory('video')
    with open('db_handler/sql/collect_feature_extraction_dirs.sql') as q_file:
        sql = q_file.read()
        raw_data = pd.read_sql(sql=sql, con=db_connection, index_col='id')

    v_e = VisualFeatureExtractor(process_mode=3, get_names=False, online_display=True)
    # v_features_names = v_e.get_features_names(scope=2)
    a_e = AudioFeatureExtractor(get_names=False)
    # a_features_names = a_e.get_feature_names()
    m_e = SymbolicFeatureExtractor(quarter_length_divisors=(16, 12), get_names=False)
    # s_features_names = m_e.get_feature_names()

    # audio files
    already_there = pd.read_sql_table('audio_features', con=db_connection)
    audio_files = raw_data.loc[~raw_data['audio_id'].isin(already_there['audio_id']), ['audio_id', 'audio_file_path']]
    audio_files.drop_duplicates(inplace=True)
    for index, row in audio_files.iterrows():
        features = a_e.extract_audio_features(row['audio_file_path'])
        f_l = features.tolist()
        f_l.insert(0, row['audio_id'])
        db.insert_row_into_table('audio_features', tuple(f_l))

    # midi files
    already_there = pd.read_sql_table('symbolic_features', con=db_connection)
    midi_files = raw_data.loc[~raw_data['midi_id'].isin(already_there['midi_id']), ['midi_id', 'midi_file_path']]
    midi_files.drop_duplicates(inplace=True)
    for index, row in midi_files.iterrows():
        features = m_e.extract_symbolic_features(row['midi_file_path'])
        f_l = list(features)
        f_l.insert(0, row['midi_id'])
        db.insert_row_into_table('symbolic_features', tuple(f_l))

    # video files
    problems = []
    already_there = pd.read_sql_table('video_features', con=db_connection)
    video_files = raw_data.loc[~raw_data['clip_id'].isin(already_there['clip_id']), ['clip_id',
                                                                                     'video_id',
                                                                                     'start', 'end',
                                                                                     'video_file_path',
                                                                                     'video_type']]
    video_files.drop_duplicates(inplace=True)
    video_files['target_name'] = 'V' + video_files['clip_id'].astype('str') + '_' + video_files['start'].astype('str') \
                                 + '.' + video_files['video_type']
    video_files['length'] = round(video_files['end'] / 1000 - video_files['start'] / 1000, 0)
    for index, row in video_files.iterrows():
        target_files = video_chunker(input_file=row['video_file_path'],
                                     target_directory=temp_folder,
                                     target_name=row['target_name'],
                                     file_type='.mp4',
                                     file_length=row['length'],
                                     chunk_size=row['length'],
                                     start=row['start'])
        try:
            features, _, _ = v_e.extract_visual_features(target_files[0], print_flag=False)
            f_l = features.tolist()
            f_l.insert(0, row['clip_id'])
            db.insert_row_into_table('video_features', tuple(f_l))
        except RuntimeError:
            problems.append(row['clip_id'])
        purge_temp_folder(temp_folder)
    for prob in problems:
        print(prob)