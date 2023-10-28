import os

from flask import Flask

app = Flask(__name__)

api_keys = []

for key, value in os.environ.items():
    if key.upper().startswith("DOCXTMPL_API_KEY_FILE"):
        with open(value, "r") as f:
            api_keys.append(f.readline().strip())
    if key.upper().startswith("DOCXTMPL_API_KEY"):
        api_keys.append(value)
