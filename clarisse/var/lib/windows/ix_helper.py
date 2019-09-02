
import os

# ensure the paths are correctly setup so that ix library will find its dependencies
os.environ["PATH"] += "{env_sep}{path}{env_sep}{path}{path_sep}..".format(
    path=os.path.dirname(os.path.abspath(__file__)),
    env_sep=os.pathsep,
    path_sep=os.path.sep
)

import ix as __api__
import clarisse_helper as __clarisse_helper__
ix = __clarisse_helper__
ix.application = None
__clarisse_helper__.api = __api__

def create_application(module_path):
    if ix.application == None:
        ix.application = ix.api.ApplicationHelper.create_application(module_path)
        import __cmds__
        ix.cmds = __cmds__
        ix.cmds.ix.api = __api__
    else:
        print 'An application has been already created!'
        raise RuntimeError()
