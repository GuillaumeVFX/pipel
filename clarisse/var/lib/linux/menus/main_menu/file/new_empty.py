# Propose to save the project if it's modified
reponse, filename = ix.check_need_save()
if reponse.is_yes():
    ix.application.save_project(filename)

if not reponse.is_cancelled():
    # create an empty project
    ix.application.new_project()
    # clear and reset all Clarisse windows
    ix.application.reset_windows_layout()