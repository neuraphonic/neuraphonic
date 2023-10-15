from praat import Praat
from wma_to_wav import main

import os

main()

praat = Praat()

directory = 'data_store/unhealthy_audio'

i = 0

for filename in os.listdir(directory):
    i = i + 1
    print(i)
    if (i > 25):
        break
    f = os.path.join(directory, filename)
    try:
        praat.generateSpectrogram(f)
    except:
        continue