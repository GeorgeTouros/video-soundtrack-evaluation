from pydub import AudioSegment
import os


def convert_stereo_to_mono_wav(audio_file, output_dir):
    file = AudioSegment.from_file(audio_file, format='mp3')
    mono = file.set_channels(1)
    smpl_width = mono.set_sample_width(1)
    smpl_width.export(output_dir+'/'+audio_file, format='mp3')


def copy_and_convert_dir(in_dir, out_dir):
    os.chdir(in_dir)
    for file in os.listdir(in_dir):
        convert_stereo_to_mono_wav(file, out_dir)
