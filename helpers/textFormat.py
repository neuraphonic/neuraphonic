import pandas as pd
import os
import filters.praat as praat

# code to run through all files in data_store/healthy_audio and turn them into a csv file with Praat

praat = praat.Praat()

directory = 'data_store/unhealthy_audio'

i = 0

features = []

for filename in os.listdir(directory):
    i = i + 1
    print(i)
    f = os.path.join(directory, filename)
    try:
        features.append(praat.getFeatures(f))
    except:
        continue

df = pd.DataFrame(features)
df.to_csv('data_store/unhealthy.csv')
