import argparse
from prettytable import PrettyTable
from termcolor import colored
from modules.sysinfo import OSInfo
from modules.netconfig import CIS_NetworkConfigurations
from modules.netconfig import CIS_FirewallConfigurations
from modules.lognaudit import CIS_LoggingAndAuditingConfigurations
from modules.sysfileaudit import CIS_SystemFileConfigurations

banner = "\n"\
"              ___  _  ___          _________         .    .\n"\
"             /  _\\| |/ __|        (..       \_    ,  |\  /|\n"\
"            |  |_ | |\__ \\         \       O  \  /|  \ \/ /\n"\
"             \___||_||___/          \______    \/ |   \  /\n"\
"       __ _  _   _  ____   _  _____    vvvv\    \ |   /  |\n"\
"      / _` || | | ||  _ \\ | ||_   _|   \^^^^  ==   \_/   |\n"\
"     | (_| || |_| || |_) )| |  | |      `\_   ===    \.  |\n"\
"      \\__,_|\\_____/|____/ |_|  |_|      / /\_   \ /      |\n"\
"                                        |/   \_  \|     /\n"\
"            Tran Thanh Vinh                    \_______/\n"\
"\n"\
"  An auditing tool for Linux system, follow the CIS Benchmark\n"

parser = argparse.ArgumentParser(prog='CIS Audit Shark', 
                                usage='python3 run.py', 
                                epilog='python3 run.py', 
                                description='An auditing tool for Linux system, follow the CIS Benchmark. This program should be run as root.')

def main():
    print(banner)

    systemInfo = OSInfo()
    systemInfo.showOSInfo()

    total_passed = 0
    total_rules = 0

    networkConfigAudit = CIS_NetworkConfigurations('./rules/network.json', 'Auditing network configurations')
    firewallConfigAudit = CIS_FirewallConfigurations('./rules/firewall.json', 'Auditing firewall configurations')
    lognauditConfigAudit = CIS_LoggingAndAuditingConfigurations('./rules/lognaudit.json', 'Auditing logging and auditing configurations')
    sysfileConfigAudit = CIS_SystemFileConfigurations('./rules/sysfile.json', 'Auditing system file configurations')

    # Audit System File configurations
    sysfileConfigAudit.audit()
    print()
    total_passed += sysfileConfigAudit.getPassed()
    total_rules += sysfileConfigAudit.getTotal()

    # Audit Network configurations
    networkConfigAudit.audit()
    print()
    total_passed += networkConfigAudit.getPassed()
    total_rules += networkConfigAudit.getTotal()

    # Audit Firewall configurations
    firewallConfigAudit.audit()
    print()
    total_passed += firewallConfigAudit.getPassed()
    total_rules += firewallConfigAudit.getTotal()

    # Audit Logging and Auditing configurations
    lognauditConfigAudit.audit()
    print()
    total_passed += lognauditConfigAudit.getPassed()
    total_rules += lognauditConfigAudit.getTotal()

    # Result
    totalPercentPassed = float("{:.2f}".format(total_passed / total_rules * 100))
    resultTable = PrettyTable([colored("Passed", "green"), colored("Failed", "red"), colored("Error", "yellow"), "Total"])
    resultTable.add_row([colored(str(total_passed) + '(' + str(totalPercentPassed) + '%)', "green"), colored(str(total_rules - total_passed) + '(' + str(100 - totalPercentPassed) + '%)', "red"), colored("0", "yellow"), total_rules])
    print(colored("========== RESULT ==========", "blue"))
    print(resultTable)
    print("\n")
    print(colored("========== Audit System File configurations ==========", "blue"))
    sysfileConfigAudit.run()
    print(colored("========== Audit Network configurations ==========", "blue"))
    networkConfigAudit.run()
    print(colored("========== Audit Firewall configurations ==========", "blue"))
    firewallConfigAudit.run()
    print(colored("========== Audit Logging and Auditing configurations ==========", "blue"))
    lognauditConfigAudit.run()

if __name__ == "__main__":
    main()