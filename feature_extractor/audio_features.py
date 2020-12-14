import os
from pyAudioAnalysis.MidTermFeatures import mid_feature_extraction, beat_extraction
from pyAudioAnalysis import audioBasicIO
import numpy as np

AUDIO_FEAT_NAMES = [
    'zcr_mean', 'energy_mean', 'energy_entropy_mean', 'spectral_centroid_mean', 'spectral_spread_mean'
    , 'spectral_entropy_mean', 'spectral_flux_mean', 'spectral_rolloff_mean', 'mfcc_1_mean'
    , 'mfcc_2_mean', 'mfcc_3_mean', 'mfcc_4_mean', 'mfcc_5_mean', 'mfcc_6_mean'
    , 'mfcc_7_mean', 'mfcc_8_mean', 'mfcc_9_mean', 'mfcc_10_mean', 'mfcc_11_mean'
    , 'mfcc_12_mean', 'mfcc_13_mean', 'chroma_1_mean', 'chroma_2_mean'
    , 'chroma_3_mean', 'chroma_4_mean', 'chroma_5_mean', 'chroma_6_mean'
    , 'chroma_7_mean', 'chroma_8_mean', 'chroma_9_mean', 'chroma_10_mean'
    , 'chroma_11_mean', 'chroma_12_mean', 'chroma_std_mean', 'delta zcr_mean'
    , 'delta energy_mean', 'delta energy_entropy_mean', 'delta spectral_centroid_mean'
    , 'delta spectral_spread_mean', 'delta spectral_entropy_mean', 'delta spectral_flux_mean'
    , 'delta spectral_rolloff_mean', 'delta mfcc_1_mean', 'delta mfcc_2_mean'
    , 'delta mfcc_3_mean', 'delta mfcc_4_mean', 'delta mfcc_5_mean', 'delta mfcc_6_mean'
    , 'delta mfcc_7_mean', 'delta mfcc_8_mean', 'delta mfcc_9_mean', 'delta mfcc_10_mean'
    , 'delta mfcc_11_mean', 'delta mfcc_12_mean', 'delta mfcc_13_mean', 'delta chroma_1_mean'
    , 'delta chroma_2_mean', 'delta chroma_3_mean', 'delta chroma_4_mean', 'delta chroma_5_mean'
    , 'delta chroma_6_mean', 'delta chroma_7_mean', 'delta chroma_8_mean', 'delta chroma_9_mean'
    , 'delta chroma_10_mean', 'delta chroma_11_mean', 'delta chroma_12_mean', 'delta chroma_std_mean'
    , 'zcr_std', 'energy_std', 'energy_entropy_std', 'spectral_centroid_std', 'spectral_spread_std'
    , 'spectral_entropy_std', 'spectral_flux_std', 'spectral_rolloff_std', 'mfcc_1_std'
    , 'mfcc_2_std', 'mfcc_3_std', 'mfcc_4_std', 'mfcc_5_std', 'mfcc_6_std', 'mfcc_7_std'
    , 'mfcc_8_std', 'mfcc_9_std', 'mfcc_10_std', 'mfcc_11_std', 'mfcc_12_std', 'mfcc_13_std'
    , 'chroma_1_std', 'chroma_2_std', 'chroma_3_std', 'chroma_4_std', 'chroma_5_std', 'chroma_6_std'
    , 'chroma_7_std', 'chroma_8_std', 'chroma_9_std', 'chroma_10_std', 'chroma_11_std', 'chroma_12_std'
    , 'chroma_std_std', 'delta zcr_std', 'delta energy_std', 'delta energy_entropy_std', 'delta spectral_centroid_std'
    , 'delta spectral_spread_std', 'delta spectral_entropy_std', 'delta spectral_flux_std', 'delta spectral_rolloff_std'
    , 'delta mfcc_1_std', 'delta mfcc_2_std', 'delta mfcc_3_std', 'delta mfcc_4_std', 'delta mfcc_5_std'
    , 'delta mfcc_6_std', 'delta mfcc_7_std', 'delta mfcc_8_std', 'delta mfcc_9_std', 'delta mfcc_10_std'
    , 'delta mfcc_11_std', 'delta mfcc_12_std', 'delta mfcc_13_std', 'delta chroma_1_std', 'delta chroma_2_std'
    , 'delta chroma_3_std', 'delta chroma_4_std', 'delta chroma_5_std', 'delta chroma_6_std', 'delta chroma_7_std'
    , 'delta chroma_8_std', 'delta chroma_9_std', 'delta chroma_10_std', 'delta chroma_11_std'
    , 'delta chroma_12_std', 'delta chroma_std_std', 'beat', 'beat_conf'
]


class AudioFeatureExtractor():
    def __init__(self,
                 mid_window=2,
                 mid_step=1,
                 short_window=0.05,
                 short_step=0.025,
                 get_names=True):
        """
        :param mid_window: the mid-term window in seconds
        :param mid_step: the mid-term step
        :param short_window: the short-term window
        :param short_step: the short-term step
        :param get_names: defines whether the function will return the feature names or not.
                default value is False.
        """
        self.mid_window = mid_window
        self.mid_step = mid_step
        self.short_window = short_window
        self.short_step = short_step
        self.get_names = get_names
        self.feature_names = AUDIO_FEAT_NAMES

    def get_feature_names(self):
        return self.feature_names

    def extract_audio_features(self, file_path):
        """
        Method to extract audio features from an audio file
        :param file_path: Name of the audio file
        :return: Numpy array containing audio features,
                (list of mid-feature names if get_names=True)
        """
        # check for empty file
        if os.stat(file_path).st_size == 0:
            print("   (EMPTY FILE -- SKIPPING)")
            # read sampling rate
        [sampling_rate, signal] = audioBasicIO.read_audio_file(file_path)
        signal = audioBasicIO.stereo_to_mono(signal)
        mid_term_features = np.array([])
        mid_features, short_features, _ = \
            mid_feature_extraction(signal, sampling_rate,
                                   round(self.mid_window * sampling_rate),
                                   round(self.mid_step * sampling_rate),
                                   round(sampling_rate * self.short_window),
                                   round(sampling_rate * self.short_step))
        beat, beat_conf = beat_extraction(short_features, self.short_step)
        mid_features = np.transpose(mid_features)
        # long term averaging of mid-term statistics
        mid_features = mid_features.mean(axis=0)
        if (not np.isnan(mid_features).any()) and \
                (not np.isinf(mid_features).any()):
            mid_features = np.append(mid_features, beat)
            mid_features = np.append(mid_features, beat_conf)
            if len(mid_term_features) == 0:
                # append feature vector
                mid_term_features = mid_features
            else:
                mid_term_features = np.vstack((mid_term_features, mid_features))

        if self.get_names:
            return mid_term_features, self.feature_names
        else:
            return mid_term_features
