ix.enable_command_history()

app = ix.application

title = "Import Image Files..."
filters = ix.api.ImageIOFileFormat.get_extension_file_filters_for_open_file()
filenames = ix.api.GuiWidget.open_files(app, app.get_current_project_filename(), title, filters)

if filenames.get_count() > 0:
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    ix.import_map_files(filenames, "TextureMapFile", "_map")
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

ix.disable_command_history()