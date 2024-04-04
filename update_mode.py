import time
import subprocess
import os
from update.update_app import update_app
from update.update_pip_requirements import update_requirements

from modules.load_configure import *

if echo == "True":
    from modules.echo import *

dir = os.getcwd()

while True:

    print("You in update mode, choose the update options: \n")
    print("1) Update app \n")
    print("2) Update/fix pip requirements \n")

    mode = int(input("Enter options for update, 1 or 2: "))


    if mode == 1:
        update_app()
    elif mode == 2:
        update_requirements()
