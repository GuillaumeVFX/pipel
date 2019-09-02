ix.enable_command_history()

app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()
ix.application.open_preferences_window(clarisse_win)

ix.disable_command_history()