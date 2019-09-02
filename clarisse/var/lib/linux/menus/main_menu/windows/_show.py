app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()

sub_win_count = app.get_sub_windows_count(clarisse_win)

menu.enable_command("Windows>Active Windows>", sub_win_count > 0)
menu.enable_command("Windows>Hide/Show Subwindows", sub_win_count > 0)


clarisse_win_count = app.get_clarisse_window_count()
menu.enable_command("Windows>Close Current", clarisse_win_count > 1)
