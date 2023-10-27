import os

from flask import Flask

app = Flask(__name__)

if os.getenv("AUTH_TOKEN_FILE"):
    with open(os.getenv("AUTH_TOKEN_FILE"), "r") as f:
        auth_token = f.readline()
if os.getenv("AUTH_TOKEN"):
    auth_token = os.getenv("AUTH_TOKEN")

print(f"Token: {auth_token}")
