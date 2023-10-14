import flask
import os

import wma_to_wav

UPLOAD_FOLDER = "./compressed_audio"
ALLOWED_EXTENSIONS = {"wav", "wma"}

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    value = '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return(value)

@app.route("/")
def home_page():
    return flask.render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
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
    wma_to_wav.main()
    return "complete"

@app.route("/show_results")
def show_results():
    return flask.render_template("results.html")