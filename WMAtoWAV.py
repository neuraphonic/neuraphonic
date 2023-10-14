import os
from pydub import AudioSegment

input_path = "compressed_audio/"
output_path = "neuraphonic/raw_audio/"

os.chdir(input_path)

wma_files = os.listdir()

for input_file in wma_files:
    name, extension = os.path.splitext(input_file)
    if extension == ".wma":
        wma_source = AudioSegment.from_file(input_file, format="wma")
        wav_file = name + extension
        output = output_path + wav_file
        wma_source.export(output, format="wav")