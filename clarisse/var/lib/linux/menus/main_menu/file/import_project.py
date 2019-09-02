ix.enable_command_history()

app = ix.application

title = "Import Project Files..."

# build project filters
extensions = app.get_project_extension_name()
str_ext = "{"
for i in range(extensions.get_count()):
    str_ext += extensions[i]
    if (i+1) < extensions.get_count():
        str_ext += ","
str_ext += "}"
filters = "Known Files\t*." + str_ext

filenames = ix.api.GuiWidget.open_files(app, app.get_current_project_filename(), title, filters)
if filenames.get_count() > 0:
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    for i in range(filenames.get_count()):
        ix.import_project(filenames[i])
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

ix.disable_command_history()