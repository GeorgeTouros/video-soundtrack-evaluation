from pydub import AudioSegment
import os
import subprocess


def load_and_convert_with_ffmpeg(audio_file, output, sample_rate=8000, channels=1, file_type='mp3'):
    call = "ffmpeg -y -i {input} -sn -ar {sample_rate} -f {file_type} -ac {channels} {output}"
    data = {'input': """\"""" + str(audio_file) + """\"""",
            'channels': channels,
            'sample_rate': sample_rate,
            'output': """\"""" + str(output) + """\"""",
            'file_type': file_type}
    subprocess.call(call.format(**data), shell=True)
    loaded = AudioSegment.from_file(output)
    return loaded


def load_and_convert_stereo_to_mono_8k(audio_file, format='mp3', output_dir=None):
    file = AudioSegment.from_file(audio_file, format=format)
    smpl_width = convert_stereo_to_mono_8k(file)
    if output_dir:
        smpl_width.export(output_dir+'/'+audio_file, format=format)
    else:
        return smpl_width


def convert_stereo_to_mono_8k(file):
    mono = file.set_channels(1)
    smpl_width = mono.set_frame_rate(8000)
    return smpl_width


def copy_and_convert_dir(in_dir, out_dir, sample_rate=8000, channels=1):
    os.chdir(in_dir)
    for file in os.listdir(in_dir):
        new_output_name = out_dir+file
        load_and_convert_with_ffmpeg(file, new_output_name, sample_rate=sample_rate, channels=channels)


def copy_and_convert_files_list(files_list, out_dir, sample_rate=8000, channels=1, file_type='mp3'):
    for file in files_list:
        file_stripped = file[:-3]
        new_output_name = out_dir+file_stripped+file_type
        load_and_convert_with_ffmpeg(file, new_output_name,
                                     sample_rate=sample_rate, channels=channels, file_type=file_type)
