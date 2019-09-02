ix.enable_command_history()

app = ix.application
if app.get_command_manager().is_redoable():
    app.get_command_manager().redo()
    ix.log_info("Redo()")

ix.disable_command_history()