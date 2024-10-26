from flask import Flask

app = Flask(__name__)
app.secret_key= "12345"
from setup.controllers import default