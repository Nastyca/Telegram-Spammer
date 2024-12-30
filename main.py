import os
import json
import time
import ctypes
import random
import requests

from pystyle import *
from sys import stdout
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor

#-

def cls():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear') 

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config_json = load_config('config.json')

liste = open("proxies.txt", "r").read().splitlines()

cls()

#-

e = Fore.RESET
b = Fore.WHITE
g = Fore.GREEN
r = Fore.RED

#-

nombre = 0
valides = 0
invalides = 0
batch_size = 3000

Write.Print(f"""
 _______   _                                   _____                                           
|__   __| | |                                 / ____|                                          
   | | ___| | ___  __ _ _ __ __ _ _ __ ___   | (___  _ __   __ _ _ __ ___  _ __ ___   ___ _ __ 
   | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \   \___ \| '_ \ / _` | '_ ` _ \| '_ ` _ \ / _ \ '__|
   | |  __/ |  __/ (_| | | | (_| | | | | | |  ____) | |_) | (_| | | | | | | | | | | |  __/ |   
   |_|\___|_|\___|\__, |_|  \__,_|_| |_| |_| |_____/| .__/ \__,_|_| |_| |_|_| |_| |_|\___|_|   
                   __/ |                            | |                                        
                  |___/                             |_|                                        \n""", Colors.blue_to_purple, interval=0)

#-

nombre_ = int(input(f"{Fore.LIGHTMAGENTA_EX}Nombre ->{e} "))
threads = int(input(f"\n{Fore.LIGHTMAGENTA_EX}Threads ->{e} "))

type_ = input(f"""
{b}PROXIES
{Fore.BLUE}[1] HTTP/HTTPS
[2] SOCKS5

{Fore.LIGHTMAGENTA_EX}Choisissez ->{e} """)

if type_ == "1":
    type = "http"
elif type_ == "2":
    type = "socks5"
else:
    print(f"\n{r}[-] Mauvais choix !")
    time.sleep(3)
    quit()

print(f"")

#-

url = config_json["url"]
chat_id = config_json["chat_id"]
text = config_json["text"]

#-

headers = {"Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*"}

def spam_(nombre):
    global valides, invalides

    nombre += 1

    proxy = random.choice(liste)
    proxies = {"http": f"{type}://{proxy}", "https": f"{type}://{proxy}"}
    
    try:

        requete = requests.post(url, headers=headers, data=f"chat_id={chat_id}&text={text}", proxies=proxies, timeout=5)
        if 'true' in requete.text:
            with open("data/messages.json", "a", encoding="latin-1", errors="ignore") as f:
                json.dump(json.loads(requete.text), f, ensure_ascii=False)
                f.write(",\n")

            valides += 1
            stdout.write(f"\r{g}[{b}Nombre : {valides}{g}] {b}> {g}[{b}Chat ID : {chat_id}{g}] {b}> {g}[{b}Message : {text}{g}]{e}")
            stdout.flush()
        else:
            invalides += 1
            stdout.write(f"\r{r}[{b}Nombre : {valides}{r}] {b}> {r}[{b}Chat ID : {chat_id}{r}] {b}> {r}[{b}Message : {text}{r}]{e}")
            stdout.flush()

        ctypes.windll.kernel32.SetConsoleTitleW(f"Nombre : {nombre} | Valides : {valides} | Invalides : {invalides}")

    except:
        pass

def spam(start, end, step, threads):
    for batch_start in range(start, end + 1, step):
        batch_end = min(batch_start + step - 1, end)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(spam_, range(batch_start, batch_end + 1))

spam(1, nombre_, batch_size, threads)

print(f"\n\n{g}[+] Données enregistrées avec succès dans 'data/messages.json'{e}")
