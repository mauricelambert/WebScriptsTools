#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements tools for WebScripts Scripts
#    Copyright (C) 2022  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package implements tools for WebScripts Scripts.
"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements tools for WebScripts Scripts.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/WebScriptsTools"

copyright = """
WebScriptsTools  Copyright (C) 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["get_webscripts_data_path", "get_upload_module", "get_log_file", "get_user", "main"]

from importlib.util import spec_from_file_location, module_from_spec
from collections.abc import Callable
from sys import exit, stderr, argv
from os.path import join, splitext
from os import environ, makedirs
from types import ModuleType
from typing import Dict
from json import loads


environ_get: Callable = environ.get


def get_upload_module() -> ModuleType:

    """
    This function returns the WebScripts upload module.
    """

    upload_path = join(environ_get("WEBSCRIPTS_PATH"), "scripts", "uploads", "modules", "uploads_management.py")
    spec = spec_from_file_location("uploads", upload_path)
    upload = module_from_spec(spec)
    spec.loader.exec_module(upload)

    return upload


def get_webscripts_data_path() -> str:

    """
    This function returns the path to the data directory.
    """

    return join(environ_get("WEBSCRIPTS_PATH"), "data")

def get_log_file() -> str:

    """
    This function returns the log path
    for WebScripts scripts.
    """

    logpath = environ_get("LOG_PATH")
    script = loads(environ_get("SCRIPT_CONFIG"))
    name = script.get("name")
    category = environ_get("category", "nocategory")

    directory = join(logpath, "scripts", category)
    file = join(f"{splitext(name)[0]}.log")

    makedirs(directory, exist_ok=True)

    return file


def get_user() -> Dict[str, str]:

    """
    This function returns the WebScripts user.
    """

    return loads(environ_get("USER"))


def main() -> int:

    """
    This function execute scripts
    tools from the command line.
    """

    functions = ("get_log_file", "get_webscripts_data_path")

    if len(argv) != 2 or argv[1] not in functions:
        print(
            f"USAGES: {argv[0]} <tool>\n"
            "\tAvailable tools are:\n\t - " +
            "\n\t - ".join(
                functions
            )
        )
        return 1

    print(globals()[argv[1]]())
    return 0

if __name__ == "__main__":
    # print(copyright)
    exit(main())
