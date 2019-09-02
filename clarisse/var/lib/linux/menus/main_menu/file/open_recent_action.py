import ix
app = ix.application

# Propose to save the project if it's modified
reponse, filename = ix.check_need_save()
if reponse.is_yes():
    app.save_project(filename)

if not reponse.is_cancelled():
    if project_path != "":
        clarisse_win = app.get_event_window()
        old_cursor = clarisse_win.get_mouse_cursor()
        clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
        app.disable()
        app.load_project(project_path)
        app.enable()
        clarisse_win.set_mouse_cursor(old_cursor)