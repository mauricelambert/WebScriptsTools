from os import getcwd, name
from os.path import join
from json import dump
from sys import exit

with open("config_TestWebScriptsTools.json", "w") as file:
    dump(
        {
            "scripts": {"TestWebScriptsTools": "config"},
            "config": {
                "launcher": "python3" if name != "nt" else "python",
                "category": "Tests",
                "path": join(getcwd(), "test.py"),
            },
        },
        file,
    )

print(
    "Move the config_TestWebScriptsTools.json file to a "
    "WebScripts configuration path.\nPlease remove it after"
    " testing, this script configuration is not secure and"
    " not hardened, and this script prints information about"
    " your platform, WebScripts server, and configuration."
)
exit(0)
