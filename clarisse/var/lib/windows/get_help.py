import sys
import inspect
from collections import namedtuple

DefaultArgSpec = namedtuple('DefaultArgSpec', 'has_default default_value')

def _get_default_arg(args, defaults, arg_index):

    if not defaults:
        return DefaultArgSpec(False, None)

    args_with_no_defaults = len(args) - len(defaults)

    if arg_index < args_with_no_defaults:
        return DefaultArgSpec(False, None)
    else:
        value = defaults[arg_index - args_with_no_defaults]
        if (type(value) is str):
            value = '"%s"' % value
        return DefaultArgSpec(True, value)

def get_method_sig(method):
    argspec = inspect.getargspec(method)
    arg_index=0
    args = []
    for arg in argspec.args:
        default_arg = _get_default_arg(argspec.args, argspec.defaults, arg_index)
        if default_arg.has_default:
            args.append("%s=%s" % (arg, default_arg.default_value))
        else:
            args.append(arg)
        arg_index += 1
    return "%s(%s)" % (method.__name__, ", ".join(args))

if __name__ == "__main__":
    lng = ix.api.ModuleLanguage.get_language(ix.application, 'Python')
    cmd = lng.get_help()
    help = ""
    try:
        if cmd != "" and cmd.startswith("ix"):
            modules = cmd.split(".")
            for part in modules:
                if modules.index(part) == 0:
                    attr = sys.modules[part]
                else:
                    attr = getattr(attr, part)
            method_sig = get_method_sig(attr)

            if attr.__doc__:
                # if the doc have more one line, put the signature before the doc
                if (attr.__doc__.count("\n") >= 1):
                    help += method_sig
                    help += "\n"
                help += attr.__doc__
            else:
                help += method_sig
    except:
        pass
    lng.set_help(help)
    ix.api.ModuleLanguage.get_language(ix.application, 'Python')
