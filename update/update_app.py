import subprocess
import os

def update_app():
    subprocess.run(["git", "pull"], shell=True)