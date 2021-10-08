from threading import Thread

from flask import Flask

app = Flask("")


@app.route("/")
def home():
    return """
        LinerlyBot is now on matrix.org! Simply invite @linerlybot-matrix:matrix.org into your (unencrypted) room.\n\nNote that the Matrix version is still in development, as the libraries needed by the bot can change. Will plan to use matrix-nio.
    """


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()