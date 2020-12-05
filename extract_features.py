from feature_extractor.audio_features import AudioFeatureExtractor
from feature_extractor.visual_features import VisualFeatureExtractor

if __name__ == '__main__':

    v_e = VisualFeatureExtractor()
    v_file = './temp/test_dataset/V2A2822_4985000__30.mp4'
    features_stats, f_names_stats, feature_matrix, f_names, shot_change_times = \
        v_e.extract_visual_features(v_file, process_mode=3, save_results=False)

    for feature in f_names:
        print(feature)

    a_e = AudioFeatureExtractor()
    a_file = './temp/test_dataset/M19182A50503_059 - Elton John - Tiny Dancer.mp3'
    mid_term_features, mid_feature_names = a_e.extract_audio_features(a_file)

    for feature in mid_feature_names:
        print(feature)