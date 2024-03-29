import time
import subprocess
import os

from modules.load_configure import *

if echo =="True":
    from art import *
    print(text2art('''TensorLM''', font="small"))
    print("Our license: https://www.apache.org/licenses/LICENSE-2.0.txt")
    print("")
    time.sleep(3)

dir = os.getcwd()

while True:

    print("You in update mode, choose the update options: \n")
    print("1) Update app \n")
    print("2) Update/fix pip requirements \n")

    mode = int(input("Enter options for update, 1 or 2: "))


    if mode == 1:
        subprocess.run([f"{dir}/update/update_app.bat"], shell=True)
    elif mode == 2:
        subprocess.run([f"{dir}/update/update_pip_requirements.bat"], shell=True)
