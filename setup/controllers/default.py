from setup import app
from flask import render_template, flash, redirect, url_for

@app.route("/")
def index():
    return render_template("index.html")