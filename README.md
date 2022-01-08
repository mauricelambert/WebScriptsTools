![WebScripts Logo](https://mauricelambert.github.io/info/python/code/WebScripts/small_logo.png "WebScripts logo")

# WebScriptsTools

## Description

This package implements tools for WebScripts Scripts.

## Requirements

This package require:

 - python3
 - python3 Standard Library

## Installation

```bash
pip install WebScriptsTools
```

## Usages

### Command line

#### Module

```bash
# These command lines should be launch in a WebScripts Scripts Environment !

python3 -m WebScriptsTools
python3 -m WebScriptsTools get_log_file
python3 -m WebScriptsTools get_webscripts_data_path
```

If you run these command lines outside the WebScripts scripting environment, you get this error:
```text
TypeError: the JSON object must be str, bytes or bytearray, not NoneType
```

Example of usage in a script bash:
```bash
logfile=$(python3 -m WebScriptsTools get_log_file)
echo "DEBUG: Get log file from WebScriptsTools" > "${logfile}"
cat "$(python3 -m WebScriptsTools get_webscripts_data_path)/datafile.txt"
echo "INFO: print data using WebScripts data directory" > "${logfile}"
```

### Python script

```python
# To use this module you should be in a WebScripts Scripts Environment

from WebScriptsTools import *

# Get the upload module, to read, delete or write a shared file
upload = get_upload_module()
upload.get_file("my_webscripts_shared_file.txt")

# Use the data path to change databases
with open(f"{get_webscripts_data_path()}/datafile.txt") as datafile:
    print(datafile.read())

# Get the log file to configure your logger or read your logs
logs = open(get_log_file())
log = logs.readline()
while log:
    print(log)
    log = logs.readline()

# Get the user to check permission or get informations like ID or name
user = get_user()
print(f"You are named '{user['name']}' here !")
```

## Links

 - [Github Page](https://github.com/mauricelambert/WebScriptsTools/)
 - [Documentation](https://mauricelambert.github.io/info/python/code/WebScriptsTools.html)
 - [Pypi package](https://pypi.org/project/WebScriptsTools/)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
