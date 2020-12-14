import subprocess
from shlex import quote


def blend_audio_with_video(input_video, input_audio, output_video, delay):
    in_v = "-i '{}' ".format(input_video)
    in_a = "-i '{}' ".format(input_audio)
    filter_complex = """-filter_complex "[1]adelay={},volume=2.0[aud];[0:1]volume=2.0[sa];[sa][aud]amix" """.format(
        delay)
    out = "-c:v copy '{}'".format(output_video)
    command = "ffmpeg " + in_v + in_a + filter_complex + out
    subprocess.call(command, shell=True)


def extract_subclip(input_video, start_timestamp, end_timestamp, targetname):
    in_v = " -i {} ".format(quote(input_video))
    search_start = " -ss {}".format(start_timestamp)
    search_length = " -t {}".format(end_timestamp - start_timestamp)
    # codecs = " -map 0 -codec copy -sn "
    codecs = " -map 0 -c:v libx264 -preset superfast -crf 17 -acodec copy -sn "
    cmd = "ffmpeg -y" + search_start + in_v + search_length + codecs + targetname
    subprocess.call(cmd, shell=True)


def get_cropped_target_name(input_file, target_directory, index, file_type='.mp4'):
    stripped = input_file[:-4]
    target_name = target_directory+stripped+'__'+str(index)+file_type
    return target_name


def video_chunker(input_file, target_directory, target_name, file_type, file_length, chunk_size=15, start=0):
    file_names = []
    chunk_index = 0
    while chunk_index <= file_length:
        starting_point = start/1000 + chunk_index
        if file_length-chunk_index >= chunk_size:
            file_name = get_cropped_target_name(target_name, target_directory, chunk_index, file_type)
            print('exporting chunk ' + file_name)
            extract_subclip(input_file, starting_point, starting_point+chunk_size, file_name)
            file_names.append(file_name)
            chunk_index += chunk_size
        else:
            chunk_index += chunk_size
    return file_names