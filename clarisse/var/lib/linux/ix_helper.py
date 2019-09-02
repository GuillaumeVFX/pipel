
import os
import ix as __api__
import clarisse_helper as __clarisse_helper__
ix = __clarisse_helper__
ix.application = None
__clarisse_helper__.api = __api__

def create_application(module_path):
    if ix.application == None:

        # create a list with all environment variables
        environ_vec = ix.api.CoreStringVector()
        for key in os.environ.keys():
            environ_vec.add(key + '=' + os.getenv(key))

        ix.application = ix.api.ApplicationHelper.create_application(module_path, environ_vec)
        import __cmds__
        ix.cmds = __cmds__
        ix.cmds.ix.api = __api__
    else:
        print 'An application has been already created!'
        raise RuntimeError()
