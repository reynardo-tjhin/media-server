import os
import platform
from flask import Flask, render_template, Response, send_from_directory

# --- Configurations ---
if (platform.system() == "Windows"):
    MEDIA_DIR = "C:\\Users\\reych\\Downloads"
elif (platform.system() == "Linux"):
    MEDIA_DIR="/home/reynardo-tjhin/media/movies"

# --- Flask App Initialization
app = Flask(__name__)


# --- Main Entry Point ---
if (__name__ == "__main__"):
    # '0.0.0.0' makes the server accessible from any device on your network
    # 'debug=True' gives you helpful error messages and auto-reloads the server when you save the file.
    # Don't use in production!
    app.run(host='0.0.0.0', port=5000, debug=True)