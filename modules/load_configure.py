from dotenv import load_dotenv
import os

load_dotenv("configure.txt")

# System #

global tlm_version
tlm_version = os.getenv("tlm_version")

global openai_key
openai_key = os.getenv("openai_key")

global echo
echo = os.getenv("echo")

global share_server_protocol
share_server_protocol = os.getenv("share_server_protocol")


# UI #

global theme
theme = os.getenv("theme")

global chat_style
chat_style = os.getenv("chat_style")

global footer
footer = os.getenv("footer")

global show_api
show_api = os.getenv("show_api")