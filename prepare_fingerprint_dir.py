import os
from cataloger.catalog_utils import get_temp_directory, setup_collection_directory
from cataloger.catalog_utils import get_collection_directory, setup_batch_temp_folders
from common import SAMPLE_RATE, CHANNELS, BATCH_SIZE, AUDIO_FILE_TYPE
from paths import local_temp_dir
from media_manipulation.audio_conversions import copy_and_convert_files_list

collected_audio_dir = get_collection_directory('audio')
try:
    local_audio_temp_dir = get_temp_directory('audio')
except FileNotFoundError:
    local_midi_temp_dir, local_audio_temp_dir, local_video_temp_dir = setup_collection_directory(
        new_dir=local_temp_dir)

temp_folder_names = setup_batch_temp_folders(batch_size=BATCH_SIZE,
                                             input_folder=collected_audio_dir,
                                             temp_dir=local_audio_temp_dir)
batch_number = 0
os.chdir(collected_audio_dir)
audio_files = os.listdir(collected_audio_dir)
for i in range(0, len(audio_files), BATCH_SIZE):
    files_list = audio_files[i: min(i + BATCH_SIZE, len(audio_files))]
    copy_and_convert_files_list(files_list, temp_folder_names[batch_number],
                                sample_rate=SAMPLE_RATE, channels=CHANNELS, file_type=AUDIO_FILE_TYPE)
    batch_number += 1
