import os
import csv
from datetime import datetime
# from werkzeug.utils import secure_filename

from flask import Flask, redirect, url_for, request, render_template, send_from_directory

import sqlite3
from flask import g
import json



app = Flask(__name__, static_folder="static")
localDomain = "http://localhost:5000"
publicDomain = "http://www.gtxr.club"
DOMAIN = localDomain

localPath = ""
publicPath = "/home/GTXR/mysite/"
PATH = localPath

extension = ""

@app.route("/")
def openHome():
    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'r') as file:
        data = json.load(file)
    data = dict(data)
    return render_template("index.html", text="Hello World", nodes = data, domain=DOMAIN)


# @app.route(f"{extension}/admin/SH", methods=["POST", "GET"])
# def admin():
#     json_file = PATH + f"static/user_data/tracking.json"
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#     date = datetime.datetime.now().strftime('%Y-%m-%d')
#     week_before = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=7)
#     return render_template('admin.html', data=data, current_date= date ,
#                            week_before= week_before.strftime('%Y-%m-%d')  ,domain=DOMAIN)


if __name__ == "__main__":
    app.debug = True
    app.run()
