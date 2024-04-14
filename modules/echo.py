from art import *
import os
import time
import psutil

from modules.load_configure import *

print("")
print(text2art('''TensorLM''', font="small"))
print("Our license: https://www.gnu.org/licenses/gpl-3.0.txt")
time.sleep(2.5)
print(" ")

print(f"Version: {tlm_version}")
print("")
print(f"Share server protocol: {share_server_protocol}")
print(f"Show API: {show_api}")
print(f"Theme: {theme}")
print(f"Chat style: {chat_style}")
print("")
print('System memory:', psutil.virtual_memory())
print('System swap memory:', psutil.swap_memory())
print("")
for _ in range(3):
    info = psutil.cpu_percent(interval=1)
    print('CPU percent (interval=1, percpu=False):', info)

print()
for _ in range(3):
    info = psutil.cpu_percent(interval=1, percpu=True)
    print('CPU percent (interval=1, percpu=True):', info)

print()
print('Logical CPUs:', psutil.cpu_count())

print("")