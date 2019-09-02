ix.enable_command_history()

app = ix.application
clarisse_win = app.get_event_window()
app.open_rename_item_window(clarisse_win)

ix.disable_command_history()