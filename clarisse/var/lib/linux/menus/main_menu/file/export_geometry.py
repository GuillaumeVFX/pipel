app = ix.application

title = "Export Geometry File..."
filters = "Wavefront Object Files\t*.obj"
filename = ix.api.GuiWidget.save_file(app, "", title, filters)

if filename != "":
    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    ix.export_geometries(filename, ix.selection.get_objects())
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)
