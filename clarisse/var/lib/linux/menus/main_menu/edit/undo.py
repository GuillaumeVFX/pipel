ix.enable_command_history()

app = ix.application
if app.get_command_manager().is_undoable():
    app.get_command_manager().undo()
    ix.log_info("Undo()")

ix.disable_command_history()