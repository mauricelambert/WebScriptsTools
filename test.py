from WebScriptsTools import __all__
from WebScriptsTools import *
from sys import exit

namespace = {}
namespace.update(locals())
namespace.update(globals())

for function in __all__:
    if function != "main":
        print(function, namespace[function]())


def test():
    try:
        a
    except Exception as e:
        raise NameError("test") from e


test()  # exit with code 127 (cause: NameError in test())
