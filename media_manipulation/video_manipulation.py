import subprocess
from shlex import quote


# ffmpeg -i 'barry.s01e01.720p.web.h264-tbs[ettv].mkv' -i 'M414A5061_Alice Cooper - No More Mr. Nice Guy.mp3' -filter_complex "[1]adelay=62000,volume=2.0[aud];[0:1]volume=2.0[sa];[sa][aud]amix" -c:v copy out.mp4


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
    codecs = " -map 0 -vcodec copy -acodec copy "

    cmd = "ffmpeg -y" + in_v + " -sn" + search_start + search_length + codecs + targetname
    subprocess.call(cmd, shell=True)


def crop_video_to_matches(trim_df, video_path, target_folder):
    start_time = trim_df['start']
    end_time = trim_df['end']
    target_id = trim_df['video_audio_match_id']
    file_type = trim_df['video_type']
    target_name = target_folder + target_id + '_' + str(start_time) + '.' + file_type
    extract_subclip(video_path, int(start_time) / 1000, int(end_time) / 1000,
                    targetname=target_name)


def get_cropped_target_name(input_file, target_directory, index, file_type='.mp4'):
    stripped = input_file[:-4]
    target_name = target_directory+stripped+'__'+str(index)+file_type
    return target_name


def video_chunker(input_file, target_directory, file_type, file_length, chunk_size=15):
    chunk_index = 0
    while chunk_index <= file_length:
        if file_length-chunk_index>=15:
            file_name = get_cropped_target_name(input_file, target_directory, chunk_index, file_type)
            print('exporting chunk ' + file_name)
            extract_subclip(input_file, chunk_index, chunk_index+chunk_size, file_name)
            chunk_index += chunk_size
        else:
            chunk_index += chunk_size
