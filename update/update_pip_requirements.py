import subprocess
import os

def update_requirements():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True)