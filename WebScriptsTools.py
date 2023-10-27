#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements tools for WebScripts Scripts
#    Copyright (C) 2022, 2023  Maurice Lambert

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

__version__ = "0.1.0"
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
WebScriptsTools  Copyright (C) 2022, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = [
    "get_webscripts_data_path",
    "get_upload_module",
    "get_upload_script",
    "set_excepthook",
    "get_log_file",
    "module2to3",
    "get_user",
    "main",
]

from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType, MethodType, FunctionType
from os.path import join, splitext, basename
from contextlib import redirect_stdout
from collections.abc import Callable
from typing import Dict, Union, Any
from sys import exit, stderr, argv
from os import environ, makedirs
from types import TracebackType
from json import loads, dumps
from functools import wraps
from sys import excepthook  # save default excepthook function
from typing import List
import sys


environ_get: Callable = environ.get


def get_upload_module() -> ModuleType:
    """
    This function returns the WebScripts upload module.
    """

    upload_path = join(
        environ_get("WEBSCRIPTS_PATH"),
        "scripts",
        "uploads",
        "modules",
        "uploads_management.py",
    )
    spec = spec_from_file_location("uploads", upload_path)
    upload = module_from_spec(spec)
    spec.loader.exec_module(upload)

    return upload


def get_webscripts_data_path() -> str:
    """
    This function returns the path to the data directory.
    """

    return environ["WEBSCRIPTS_DATA_PATH"]


def get_log_file() -> str:
    """
    This function returns the log path
    for WebScripts scripts.
    """

    logpath = environ["WEBSCRIPTS_LOGS_PATH"].split("|", 1)[0]
    script = loads(environ["SCRIPT_CONFIG"])
    name = script.get("name")
    category = environ_get("category", "nocategory")

    directory = join(logpath, "scripts", category)
    file = join(directory, f"{splitext(name)[0]}.log")

    makedirs(directory, exist_ok=True)

    return file


def get_log_files() -> str:
    """
    This function returns the log files paths
    used by WebScripts.
    """

    return environ["WEBSCRIPTS_LOGS_FILES"].split("|")


def get_log_directories() -> List[str]:
    """
    This function returns the log directories
    used by WebScripts.
    """

    return environ["WEBSCRIPTS_LOGS_PATH"].split("|")


def get_documentation_directories() -> List[str]:
    """
    This function returns the documentation directories
    used by WebScripts.
    """

    return environ["WEBSCRIPTS_DOCUMENTATION_PATH"].split(":")


def get_webscripts_modules() -> List[str]:
    """
    This function returns the modules files paths
    used by WebScripts.
    """

    return environ["WEBSCRIPTS_MODULES"].split(":")


def get_user() -> Dict[str, str]:
    """
    This function returns the WebScripts user.
    """

    return loads(environ_get("USER"))


def print_exception(
    exception_class: type, exception: Exception, traceback: TracebackType
) -> None:
    """
    This function prints exception and exit without prints sensible
    informations about the system and the code (file path, code, ect...).
    """

    try:
        function = getattr(exception, "function_name", None)
        text = repr(exception) + (
            f" from:{function!r}" if function is not None else ""
        )

        with redirect_stdout(stderr):
            cause: Exception = exception.__cause__
            while cause:
                function = getattr(cause, "function_name", None)
                text = (
                    f"{cause!r}"
                    f"{f' from:{function!r}' if function is not None else ''}"
                    f"[{text}]"
                )
                cause = cause.__cause__

            filename = basename(traceback.tb_frame.f_code.co_filename)
            print(f"{filename!r}:{traceback.tb_lineno!r} -> {text}")

    finally:
        exit(getattr(exception, "exit_code", 127))


def set_excepthook() -> None:
    """
    This function sets sys.excepthook to secure
    sensible informations on python errors.
    """

    sys.excepthook = print_exception


def get_upload_script() -> str:
    """
    This function prints the upload script path.
    """

    return join(
        environ_get("WEBSCRIPTS_PATH"),
        "scripts",
        "uploads",
        "upload_file.py",
    )


def module2to3(callable_: Union[FunctionType, MethodType]) -> FunctionType:
    """
    This decorator make compatibility between the module
    functions of version 2 and version 3 of WebScripts.
    """

    @wraps(callable_)
    def function(*args, **kwargs) -> Any:
        """
        This decorator make compatibility between the module
        functions of version 2 and version 3 of WebScripts.
        """

        environ, user, server, filename, command, inputs = args
        return callable_(
            environ,
            user,
            server.configuration,
            filename,
            command,
            inputs,
            **kwargs,
        )

    @wraps(callable_)
    def method(*args, **kwargs) -> Any:
        """
        This decorator make compatibility between the module
        functions of version 2 and version 3 of WebScripts.
        """

        self, environ, user, server, filename, command, inputs = args
        return callable_(
            self,
            environ,
            user,
            server.configuration,
            filename,
            command,
            inputs,
            **kwargs,
        )

    arg_length = callable_.__code__.co_argcount

    if arg_length == 7:
        return function
    elif arg_length == 8:
        return method


def main() -> int:
    """
    This function execute scripts
    tools from the command line.
    """

    functions = (
        "get_log_file",
        "get_log_files",
        "get_upload_script",
        "get_log_directories",
        "get_webscripts_modules",
        "get_webscripts_data_path",
        "get_documentation_directories",
    )

    if len(argv) != 2 or argv[1] not in functions:
        print(
            f"USAGES: {argv[0]} <tool>\n"
            "\tAvailable tools are:\n\t - " + "\n\t - ".join(functions)
        )
        return 1

    data = globals()[argv[1]]()
    if isinstance(data, list):
        data = dumps(data)

    print(data)
    return 0


if __name__ == "__main__":
    # print(copyright)
    exit(main())
