import ix
app = ix.application

ix.enable_command_history()

working_context = app.get_working_context()
if (not working_context.is_editable()) and working_context.is_content_locked() and working_context.is_remote() :
    ix.log_error("Cannot reference project in a locked context.\n")
elif reference_path != "":
    clarisse_win = app.get_event_window()
    filenames = ix.api.CoreStringVector()
    filenames.add(reference_path)
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    ix.reference_file(working_context, filenames)
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

ix.disable_command_history()