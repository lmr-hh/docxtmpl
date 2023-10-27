import os

from flask import Flask

app = Flask(__name__)

auth_token = os.getenv("AUTH_TOKEN")
