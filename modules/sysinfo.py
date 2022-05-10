import distro
import platform
from termcolor import colored

class OSInfo:
    def __init__(self):
        self.system = platform.system()
        self.distro = distro.id()
        self.release = distro.version()

    def showOSInfo(self):
        print(colored("========== OS Info ==========", "blue"))
        print(colored("OS:          ", "red") + self.system)
        print(colored("Distro:      ", "red") + self.distro)
        print(colored("Release:     ", "red") + self.release)
        print()