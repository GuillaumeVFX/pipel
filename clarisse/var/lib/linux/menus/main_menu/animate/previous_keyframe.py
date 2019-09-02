ix.enable_command_history()

app = ix.application
app.get_builtin_commands().goto_previous_keyframe()

ix.disable_command_history()
