from flask import Flask
import fwaccess

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "You need to know the url"

@app.route("/youtubeoff")
def hello_world1():
    fwaccess.addAllDomainOverrides()
    return "youtube off"

@app.route("/youtubeon")
def hello_world2():
    fwaccess.delAllDomainOverrides()
    return "youtube on"

