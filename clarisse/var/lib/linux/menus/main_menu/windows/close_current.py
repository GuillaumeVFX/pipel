app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()

app.close_current_clarisse_window(clarisse_win)
