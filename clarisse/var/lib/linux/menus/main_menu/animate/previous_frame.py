ix.enable_command_history()

app = ix.application
current_frame = app.get_factory().get_time().get_current_frame()
app.get_builtin_commands().set_current_frame(current_frame - 1, current_frame)

ix.disable_command_history()
