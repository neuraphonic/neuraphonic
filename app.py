import flask
import os

import wma_to_wav

from testModel import classify_using_saved_model

UPLOAD_FOLDER_WMA = "./compressed_audio"
UPLOAD_FOLDER_WAV = "./audio_samples"
ALLOWED_EXTENSIONS = {"wav", "wma"}

filename = None
result = None

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_WAV

def allowed_file(filename):
    value = '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return(value)

@app.route("/")
def home_page():
    return flask.render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    global filename
    if flask.request.method == "POST":
        if "file" not in flask.request.files:
            print("No File")
            return flask.redirect(flask.url_for("failure"))
        file = flask.request.files["file"]
        if file.filename == "":
            print("Empty File")
            return flask.redirect(flask.url_for("failure"))
        if file and allowed_file(file.filename):
            filename = file.filename
            if filename.endswith(".wma"):
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_WMA
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_WAV
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return flask.redirect(flask.url_for("success"))
        else:
            return flask.redirect(flask.url_for("failure"))
    return flask.render_template(flask.url_for("failure"))

@app.route("/uploaded", methods=["GET"])
def success():
    return flask.render_template("uploaded.html")

@app.route("/failure", methods=["GET"])
def failure():
    return flask.render_template("failure.html")

@app.route("/loading")
def loading():
    return flask.render_template("loading.html")

@app.route("/execute_pipeline")
def execute_pipeline():
    global filename
    global result
    raw_filename = filename[:-4] + str(".wav")
    if filename.endswith(".wma"):
        wma_to_wav.main()
    audio_path = audio_path="./audio_samples/" + raw_filename
    result = classify_using_saved_model(audio_path)
    return "complete"

@app.route("/show_results")
def show_results():
    global result
    if (result[0] == 1):
        result = "Your voice pattern shows features that may be indicative of Parkinson's Disease. You may want to consider consulting a doctor for further diagnosis."
    else:
        result = "Your voice pattern does not show features that may be indicative of Parkinson's Disease. Ensure that you talk to your doctor to gather a complete medical picture."
    return flask.render_template("results.html", value=result)