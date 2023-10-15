import models.ensemble as ensemble
import filters.praat as praat

import os

# get values from data_store/healthy_audio
directory = 'data_store/healthy_audio'
correct = 0
incorrect = 0

# get values from data_store/unhealthy_audio
directory = 'data_store/unhealthy_audio'

i = 0

for filename in os.listdir(directory):
    if (i == 20):
        break
    f = os.path.join(directory, filename)
    try:
        output = ensemble.classify(f)
        if output == 1:
            correct += 1
        else:
            incorrect += 1
    except:
        continue
    i += 1

print(correct / (correct + incorrect))