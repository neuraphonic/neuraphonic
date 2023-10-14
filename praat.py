import parselmouth

from parselmouth.praat import call

def getFeatures(audio_path: str, f0min, f0max):
    sound = parselmouth.Sound(audio_path)
    features = {}
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    features["hnr"] = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    features["jitter"] = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    features["jitter_abs"] = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    features["jitter_rap"] = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    features["jitter_ppq5"] = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    features["jitter_ddp"] = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    features["shimmer"] = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    features["shimmer_db"] = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    features["shimmer_apq3"] = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    features["shimmer_apq5"] = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    features["shimmer_apq11"] = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    features["shimmer_dda"] = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    

    return features

feat = getFeatures("audio_samples/test_set_subject_2.wav", 75, 200)
print(feat)
