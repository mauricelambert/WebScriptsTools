from WebScriptsTools import __all__
from WebScriptsTools import *
from sys import exit

namespace = {}
namespace.update(locals())
namespace.update(globals())

for function in __all__:
    if function != "main":
        print(function, namespace[function]())

exit(0)