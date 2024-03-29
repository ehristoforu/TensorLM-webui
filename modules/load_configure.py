from dotenv import load_dotenv
import os

load_dotenv("configure.txt")

global tlm_version
tlm_version = os.getenv("tlm_version")

global theme
theme = os.getenv("theme")

global echo
echo = os.getenv("echo")

global footer
footer = os.getenv("footer")