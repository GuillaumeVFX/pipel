#
# status: Working :)
MODULE_PATH = "./lib/clarisse_net.py"
MODULE_NAME = "clarisse_net"
import importlib
import sys

spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
clarisse_net = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = clarisse_net
spec.loader.exec_module(clarisse_net)
import clarisse_net as ix

rclarisse = ix.ClarisseNet('gaf',55000)

# rclarisse.connect('',55000)

rclarisse.run('print "REMOTE Hello World!"')


rclarisse.run('print "This is great I can send stuff to my clarisse :) wow that is too much"')

