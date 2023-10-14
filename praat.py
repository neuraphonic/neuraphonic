import parselmouth

from parselmouth.praat import call

class Praat:
    def getFeatures(self, audio_path: str, f0min, f0max):
        sound = parselmouth.Sound(audio_path)
        features = {}
        harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
        features["Jitter(%)"] = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        features["Jitter(Abs)"] = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        features["Jitter:RAP"] = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        features["Jitter:PPQ5"] = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
        features["Jitter:DDP"] = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
        features["Shimmer"] = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["Shimmer(dB)"] = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["Shimmer:APQ3"] = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["Shimmer:APQ5"] = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["Shimmer:APQ11"] = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["Shimmer:DDA"] = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        features["HNR"] = call(harmonicity, "Get mean", 0, 0)

        return features

# praat = Praat()
# feat = praat.getFeatures("files/file_example_WAV_1MG.wav", 75, 200)
# print(feat)
