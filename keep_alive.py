from flask import Flask
from threading import Thread
import os

app = Flask("")


@app.route("/")
def main():
    return "im alive"


def run():
    app.run(port=os.environ.get("PORT", 5000))


def keep_alive():
    server = Thread(target=run)
    server.start()
