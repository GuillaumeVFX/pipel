ix.enable_command_history()

app = ix.application
clarisse_win = app.get_event_window()
ix.application.open_edit_color_manager_window(clarisse_win)

ix.disable_command_history()
