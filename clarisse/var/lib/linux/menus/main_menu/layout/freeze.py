app = ix.application
clarisse_win = app.get_event_window()

app.freeze_layout(clarisse_win, not app.is_freeze_layout(clarisse_win))