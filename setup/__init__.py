from flask import Flask

app = Flask(__name__)

from setup.controllers import default