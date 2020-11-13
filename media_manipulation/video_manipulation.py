import subprocess
from shlex import quote

# ffmpeg -i 'barry.s01e01.720p.web.h264-tbs[ettv].mkv' -i 'M414A5061_Alice Cooper - No More Mr. Nice Guy.mp3' -filter_complex "[1]adelay=62000,volume=2.0[aud];[0:1]volume=2.0[sa];[sa][aud]amix" -c:v copy out.mp4


def blend_audio_with_video(input_video, input_audio, output_video, delay):
    in_v = "-i '{}' ".format(input_video)
    in_a = "-i '{}' ".format(input_audio)
    filter_complex = """-filter_complex "[1]adelay={},volume=2.0[aud];[0:1]volume=2.0[sa];[sa][aud]amix" """.format(delay)
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
