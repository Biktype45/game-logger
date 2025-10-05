import os

def print_banner():
    os.system("")  # enable ANSI colors on Windows PowerShell
    cyan = "\033[96m"
    magenta = "\033[95m"
    green = "\033[92m"
    reset = "\033[0m"

    print()
    print(cyan + "-" * 44)
    print(magenta + " Game Logger Backend Started")
    print(green + " Auto-Enrich Enabled  |  Excel Sync Active")
    print(cyan + "-" * 44 + reset)
    print()
