app = ix.application
filename = app.get_current_project_filename()
if filename != "":
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    app.save_project_snapshot(filename)
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)
else:
    app.get_main_menu().exec_command("File>Save As...")
