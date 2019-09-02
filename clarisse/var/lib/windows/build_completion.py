from datetime import datetime
import inspect

def get_attrs(foo, fullpath, last_name, completion, memo=None):

    if memo is None:
        memo = {}
        last_name = ''
    attrs = dir(foo)
    for a in attrs:
        if a == last_name or a == "ix":
            continue
        new_fullpath = fullpath + "." + a
        value = getattr(foo, a)
        if value != None and (isinstance(value, dict) or isinstance(value, list) or str(type(value)) == "<type 'dictproxy'>" or str(type(value)) == "<type 'SwigPyObject'>" or str(type(value)) == "<type 'builtin_function_or_method'>"):
            continue
        if memo.get(value) != None:
            continue
        else:
            memo[value] = True
            if value != None and not a.startswith("_") and a != "denominator":
                try:
                    completion.add(new_fullpath)
                    get_attrs(value, new_fullpath, a, completion, memo)
                except Exception, err:
                    None
                    #print "Exception '" + str(err) + "'\t  '" + new_fullpath + "'\t  '" + str(type(value)) + "'"

if __name__ == "__main__":
    lng = ix.api.ModuleLanguage.get_language(ix.application, "Python")
    completion = ix.api.CoreStringVector()

    get_attrs(ix, "ix", None, completion)

    lng.set_completion(completion)
    lng.add_completion(lng.get_keywords());
    lng.add_completion(lng.get_reserved_keywords());
    lng.set_rebuild_completion(False)

    ix.log_info("Building Python Completion done (" + str(completion.get_count()) + " entries) - Experimental Feature")