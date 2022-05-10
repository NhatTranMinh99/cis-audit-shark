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

class CIS_Audit:
    def __init__(self, rulefile, description):
        self.rulefile = rulefile
        self.description = "[-] " + description
        self.total = 0;
        self.passed = 0;
        self.error = 0;
        self.result = []
        self.command = []
        self.output = []
        self.recommendation = []

        data = json.load(open(self.rulefile))
        for rule in data['rules']:
            self.result.append({rule.get('name'): "false"})
            self.command.append(rule.get('cmd'))
            self.output.append(rule.get('output'))
            self.recommendation.append({rule.get('name'): rule.get('recommendation')})
            self.total += 1

    def audit(self):
        # passwd = "1"
        # command = subprocess.Popen(shlex.split("echo " + passwd + " | sudo -S cat /etc/shadow"), stdout=subprocess.PIPE)
        prev_index = -1
        progress_bar = tqdm(range(len(self.command)), desc=self.description, ncols=100)
        for i in progress_bar:
            check = 1
            rule_list = self.command[i]
            output_list = self.output[i]
            for rule in rule_list:
                command = subprocess.Popen(shlex.split(rule), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                if (command.stdout.read().decode("utf-8").strip() != output_list[rule_list.index(rule)]):
                    check = 0
                    break
            if (check == 1 and i > prev_index):
                self.result[i] = "true"
                self.passed += 1
            prev_index = i
            time.sleep(0.1)
        # for rule_list in self.command:
        #     check = 1
        #     output_list = self.output[self.command.index(rule_list)]
        #     for rule in rule_list:
        #         command = subprocess.Popen(shlex.split(rule), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        #         if (command.stdout.read().decode("utf-8").strip() != output_list[rule_list.index(rule)]):
        #             check = 0
        #             break
        #     if (check == 1 and self.command.index(rule_list) > prev_index):
        #         self.network_result[self.command.index(rule_list)] = "true"
        #         self.passed += 1
        #     prev_index = self.command.index(rule_list)

    def print_result(self):
        percentPassed = float("{:.2f}".format(self.passed / self.total * 100))
        resultTable = PrettyTable([colored("Passed", "green"), colored("Failed", "red"), colored("Error", "yellow"), "Total"])
        resultTable.add_row([colored(str(self.passed) + '(' + str(percentPassed) + '%)', "green"), colored(str(self.total - self.passed) + '(' + str(100 - percentPassed) + '%)', "red"), colored(self.error, "yellow"), self.total])
        print(resultTable)
        print()

    def print_recommendation(self):
        print("Recommendation for failed rules:")
        for rule in self.result:
            if (rule != "true"):
                prefix = '  - '
                preferredWidth = 100
                wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth, subsequent_indent=' '*len(prefix))
                message = str(self.recommendation[self.result.index(rule)]).replace("{}\'", "")
                message = re.sub("[{}']+", "", message)
                print(wrapper.fill(message))
        print("\n")
    
    def run(self):
        self.print_result()
        self.print_recommendation()

    def getPassed(self):
        return self.passed 

    def getTotal(self):
        return self.total
