import ix
app = ix.application
menu = app.get_main_menu()

clarisse_win = app.get_event_window()

sub_win_count = app.get_sub_windows_count(clarisse_win)
if sub_win_count > 0:
    window = app.get_sub_windows(clarisse_win, int(sub_win_index))
    if window != None:
        if window.is_shown():
            if window.is_minimized():
                window.show()
            else:
                window.set_mute(True)
                window.hide()
                window.set_mute(False)
                window.show()
        else:
            window.show()