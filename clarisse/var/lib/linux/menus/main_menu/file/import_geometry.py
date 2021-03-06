ix.enable_command_history()

app = ix.application

title = "Import Geometry Files..."
filter = "Known Files\t*.{lwo,obj}\nLightWave Object Files\t*.lwo\nWavefront Object Files\t*.obj"
filenames = ix.api.GuiWidget.open_files(app, app.get_current_project_filename(), title, filter)

if filenames.get_count() > 0:
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    ix.import_geometries(filenames)
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

ix.disable_command_history()
