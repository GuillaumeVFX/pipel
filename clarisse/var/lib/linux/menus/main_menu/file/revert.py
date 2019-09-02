app = ix.application

# Propose to save the project if it's modified
reponse, filename = ix.check_need_save()
if reponse.is_yes():
    app.save_project(filename)

if not reponse.is_cancelled():
        filename = app.get_current_project_filename()
        if filename != "":
            clarisse_win = app.get_event_window()
            old_cursor = clarisse_win.get_mouse_cursor()
            clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
            app.disable()
            app.load_project(filename)
            app.enable()
            clarisse_win.set_mouse_cursor(old_cursor)
