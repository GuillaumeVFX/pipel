import os

app = ix.application
prev_filename = app.get_current_project_filename()
project_ext = app.get_project_extension_name()[0]

if project_ext == "ple" :
    if prev_filename != "":
        _, ext = os.path.splitext(prev_filename)
        if ext != ("." + project_ext):
            prev_filename = ""

filename = ix.api.GuiWidget.save_file(app, prev_filename, "Save Project File...", "Project Files\t*." + project_ext)

if filename != "" :
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()

    _, ext = os.path.splitext(filename)
    if ext != "." + project_ext:
        filename += "." + project_ext

    app.save_project(filename)
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)
