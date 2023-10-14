import os
import subprocess

input_dir = "compressed_audio/"
output_dir = "audio_samples/"

for root, dirs, files in os.walk('compressed_audio/'):
    for f in files:
        if f.endswith('.wma'):
            command = "ffmpeg -i {} {}{}.wav".format(os.path.join(root, f), output_dir, f[:-4])
            subprocess.call(command, shell=True)