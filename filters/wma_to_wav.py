import os
import subprocess

def main():
    input_dir = "compressed_audio/"
    output_dir = "audio_samples/"

    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.wma'):
                command = "ffmpeg -i {} -c:a pcm_s321e {}{}.wav".format(os.path.join(root, f), output_dir, f[:-4])
                subprocess.call(command, shell=True)