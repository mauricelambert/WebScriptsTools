from WebScriptsTools import __all__
from WebScriptsTools import *
from os.path import join
from os import environ

import WebScriptsTools

namespace = {}
namespace.update(locals())
namespace.update(globals())

__all__.remove("main")
__all__.remove("module2to3")

environ["WEBSCRIPTS_PATH"] = "/"
environ["SCRIPT_CONFIG"] = '{"name": "script"}'
environ["LOG_PATH"] = "/"
environ["USER"] = "{}"


class Mock:
    configuration = None


class Mock2:
    class loader:
        def exec_module(test):
            assert test == "upload"


def mock_spec_from_file_location(uploads, path):
    assert uploads == "uploads"
    assert path.endswith(
        join(
            "scripts",
            "uploads",
            "modules",
            "uploads_management.py",
        )
    )
    return Mock2()


def mock_module_from_spec(spec):
    assert isinstance(spec, Mock2)
    return "upload"


WebScriptsTools.spec_from_file_location = mock_spec_from_file_location
WebScriptsTools.module_from_spec = mock_module_from_spec


class Module:
    @module2to3
    def method(
        self,
        environ,
        user,
        configuration,
        filename,
        commande,
        inputs,
        csrf_token: str = None,
    ):
        return configuration

    @module2to3
    def function(
        environ,
        user,
        configuration,
        filename,
        commande,
        inputs,
        csrf_token: str = None,
    ):
        return configuration


server = Mock()
module = Module()

assert Module.function("test", "test", server, "test", "test", "test") is None
assert module.method("test", "test", server, "test", "test", "test") is None

for function in __all__:
    print(function, namespace[function]())


def tests():
    try:
        a
    except Exception as e:
        raise NameError("test") from e


tests()  # exit with code 127 (cause: NameError in test())
