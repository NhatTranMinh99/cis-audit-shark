import subprocess
from unittest import result
from prettytable import PrettyTable
from termcolor import colored
import json
import shlex
from tqdm import tqdm
import time
import textwrap
import re
from modules.cisaudit import CIS_Audit

class CIS_SystemFileConfigurations(CIS_Audit):
    pass
