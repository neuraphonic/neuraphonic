import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from joblib import dump, load
from filters.praat import Praat

def regressor(df):
    # Regressor to predict motor_UPDRS
    label = df['motor_UPDRS']
    features = df.drop(columns=["motor_UPDRS", "total_UPDRS", "subject#", "test_time"])

    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))

def classifier(df):
    label = df['status']
    features = df.drop(columns=["status", "DFA", "PPE", "RPDE"]) # IMPORTANT - praat does not have DFA, PPE, RPDE yet so we drop them for now
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))
    dump(model, "models/randomforest.joblib")

def classify_using_saved_model(audio_sample, is_cloud=True):
    model = load("models/randomforest.joblib")
    praat = Praat()
    features = praat.getFeatures(audio_sample, 75, 200)
    if is_cloud:
        praat.generateSpectrogram(audio_sample, "/tmp/")
    else:
        praat.generateSpectrogram(audio_sample)
    df = pd.DataFrame([features])
    return model.predict(df)

def test_multiple_classifiers(df):
    log_reg_params = [{"C":0.01}, {"C":0.1}, {"C":1}, {"C":10}]
    dec_tree_params = [{"criterion": "gini"}, {"criterion": "entropy"}]
    rand_for_params = [{"criterion": "gini"}, {"criterion": "entropy"}]
    kneighbors_params = [{"n_neighbors":3}, {"n_neighbors":5}]
    naive_bayes_params = [{}]
    svc_params = [{"C":0.01}, {"C":0.1}, {"C":1}, {"C":10}]
    modelclasses = [
        ["log regression", LogisticRegression, log_reg_params],
        ["decision tree", DecisionTreeClassifier, dec_tree_params],
        ["random forest", RandomForestClassifier, rand_for_params],
        ["k neighbors", KNeighborsClassifier, kneighbors_params],
        ["naive bayes", GaussianNB, naive_bayes_params],
        ["support vector machines", SVC, svc_params]
    ]
    insights = []
    label = df['status']
    features = df.drop(columns=["status"])

    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2)
    for modelname, Model, params_list in modelclasses:
        for params in params_list:
            model = Model(**params)
            model.fit(x_train, y_train)
            score = model.score(x_test, y_test)      
            insights.append((modelname, model, params, score))

    insights.sort(key=lambda x:x[-1], reverse=True)
    for modelname, model, params, score in insights:
        print(modelname, params, score)

df1 = pd.read_csv("data/parkinsons_timeseries.csv")
df2 = pd.read_csv("data/healthy_and_unhealthy.csv")
df3 = pd.read_csv("data/healthy.csv")
df4 = pd.read_csv("data/unhealthy.csv")

df3.rename(columns={"Unnamed: 0":"status"}, inplace=True)
df4.rename(columns={"Unnamed: 0":"status"}, inplace=True)
df3["status"] = 0
df4["status"] = 1

df1["motor_UPDRS"] = df1["motor_UPDRS"].apply(lambda x: 1 if x > 12 else 0)
df1.rename(columns={"motor_UPDRS": "status"}, inplace=True)
df2.rename(columns={"MDVP:Jitter(%)":"Jitter(%)", "MDVP:Jitter(Abs)":"Jitter(Abs)", "MDVP:RAP":"Jitter:RAP", "MDVP:PPQ":"Jitter:PPQ5",
                    "MDVP:Shimmer":"Shimmer", "MDVP:Shimmer(dB)":"Shimmer(dB)", "MDVP:APQ":"Shimmer:APQ11", }, inplace=True)

df3.rename(columns={"MDVP:Jitter(%)":"Jitter(%)", "MDVP:Jitter(Abs)":"Jitter(Abs)", "MDVP:RAP":"Jitter:RAP", "MDVP:PPQ":"Jitter:PPQ5",
                    "MDVP:Shimmer":"Shimmer", "MDVP:Shimmer(dB)":"Shimmer(dB)", "MDVP:APQ":"Shimmer:APQ11", }, inplace=True)

df4.rename(columns={"MDVP:Jitter(%)":"Jitter(%)", "MDVP:Jitter(Abs)":"Jitter(Abs)", "MDVP:RAP":"Jitter:RAP", "MDVP:PPQ":"Jitter:PPQ5",
                    "MDVP:Shimmer":"Shimmer", "MDVP:Shimmer(dB)":"Shimmer(dB)", "MDVP:APQ":"Shimmer:APQ11", }, inplace=True)

df2.drop(columns=["name", "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "spread1", "spread2", "D2", "NHR"], inplace=True)
df1.drop(columns=["total_UPDRS", "subject#", "test_time", "age", "sex", "NHR"], inplace=True)

df = pd.concat([df1, df2, df3, df4])

