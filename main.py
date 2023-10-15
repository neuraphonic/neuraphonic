import flask
import os

import filters.wma_to_wav as wma_to_wav

from models.randomForest import classify_using_saved_model
from models.ensemble import classify
from twilio.twiml.voice_response import VoiceResponse

UPLOAD_FOLDER_WMA = "./compressed_audio"
UPLOAD_FOLDER_WAV = "./audio_samples"
UPLOAD_FOLDER_CLOUD = "/tmp/"
ALLOWED_EXTENSIONS = {"wav", "wma"}


filename = None
result = None

app = flask.Flask(__name__, static_folder="static")
if os.environ.get("ENV") == "dev":
    IS_CLOUD = False
else:
    IS_CLOUD = True


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
            if IS_CLOUD:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_CLOUD
            elif filename.endswith(".wma"):
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_WMA
            else:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_WAV
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return flask.redirect(flask.url_for("loading"))
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
    audio_path = os.path.join(app.config["UPLOAD_FOLDER"], raw_filename)
    print(audio_path)
    result = classify(audio_path, IS_CLOUD)
    return "complete"

@app.route("/show_results")
def show_results():
    try:
        global result
        if (result == 1):
            result = "Your voice pattern shows features that may be indicative of Parkinson's Disease. You may want to consider consulting a doctor for further diagnosis."
        else:
            result = "Your voice pattern does not show features that may be indicative of Parkinson's Disease. Ensure that you talk to your doctor to gather a complete medical picture."
        return flask.render_template("results.html", value=result)
    except:
        return "Something went wrong in processing the file. Please try again."

@app.route("/execute_pipeline_phone", methods=["POST"])
def execute_pipeline_phone():
    print("Successfully recorded voice")
    print(flask.request.args.get("RecordingUrl"))
    resp = VoiceResponse()
    resp.say("ajeeg")
    return "ajeeg"


@app.route("/phone_call", methods=["POST"])
def phone_call():
    
    resp = VoiceResponse()
    resp.say("Please record your voice")
    resp.record(
        recording_status_callback="/execute_pipeline_phone",
        recording_status_callback_method="POST",
        recording_status_callback_event="completed",
        action="/execute_pipeline_phone",
        finish_on_key="#",
        play_beep=True,
        max_length=5
    )

    resp.say("thank you for recording your voice")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
