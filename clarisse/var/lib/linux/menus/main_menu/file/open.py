app = ix.application

# Propose to save the project if it's modified
reponse, filename = ix.check_need_save()
if reponse.is_yes():
    app.save_project(filename)

if not reponse.is_cancelled():
    recent_location = app.get_current_project_filename()
    if (recent_location == "" and app.get_recent_files("project").get_count() > 0):
        recent_location = app.get_recent_files("project")[0]
    extensions = app.get_project_extension_name()
    str_ext = "{"
    for i in range(extensions.get_count()):
        str_ext += extensions[i]
        if (i+1) < extensions.get_count():
            str_ext += ","
    str_ext += "}"
    filename = ix.api.GuiWidget.open_file(app, recent_location, "Open Project File...", "Known Files\t*." + str_ext)
    if filename != "":
        clarisse_win = app.get_event_window()
        old_cursor = clarisse_win.get_mouse_cursor()
        clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
        app.disable()
        app.load_project(filename)
        app.enable()
        clarisse_win.set_mouse_cursor(old_cursor)
