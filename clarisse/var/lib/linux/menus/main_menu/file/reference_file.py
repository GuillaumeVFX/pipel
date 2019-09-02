ix.enable_command_history()

app = ix.application

working_context = app.get_working_context()
if (not working_context.is_editable()) and working_context.is_content_locked() and working_context.is_remote() :
    ix.log_error("Cannot reference project in a locked context.\n")
else:
    title = "Reference Files..."
    # filters
    filters = "Known Files"
    extensions = ix.api.CoreStringArray()
    ix.api.OfFileReferenceContextEngine.get_file_format_extensions(extensions)
    filters += "\t*.{"
    for i in range(extensions.get_count()):
        filters += extensions[i]
        if i < (extensions.get_count() - 1):
            filters += ","
    filters += "}"

    filenames = ix.api.GuiWidget.open_files(app, "", title, filters)

    if filenames.get_count() > 0:
        clarisse_win = app.get_event_window()
        clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
        app.disable()
        ix.reference_file(working_context, filenames)
        for i in range(filenames.get_count()):
            filename = filenames[i]
            app.add_recent_file(filename, "reference")
        app.enable()
        clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

ix.disable_command_history()