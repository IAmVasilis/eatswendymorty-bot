
from colorama import Fore

import colorama


class log:
    def __init__(self):
        colorama.init()

    @staticmethod
    def print(caller: str, text: str):
        print(f"{Fore.WHITE}[{Fore.CYAN}{caller}{Fore.WHITE}] {text}")
