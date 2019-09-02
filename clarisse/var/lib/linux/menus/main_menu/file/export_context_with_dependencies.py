app = ix.application

if app.get_selection().get_count() > 0:
    item = app.get_selection().get_item(0)
    if item.is_context():
        context_selected = item.to_context()
        if context_selected != 0:
            title = "Export Context As Project With Dependencies..."
            filters = "Clarisse Project\t*.project"
            filename = ix.api.GuiWidget.save_file(app, "", title, filters)

            if filename != "":
                clarisse_win = app.get_event_window()
                clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
                app.disable()
                ix.export_context_as_project_with_dependencies(context_selected, filename)
                app.enable()
                clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)
else:
    ix.log_warning("Export Context As Project With Dependencies error: Works only with a context.")

