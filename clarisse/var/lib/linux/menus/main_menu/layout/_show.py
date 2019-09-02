app = ix.application
menu = app.get_main_menu()

clarisse_win = app.get_event_window()
if (clarisse_win != None):
    item = menu.get_item("Layout>Freeze")
    item.set_checked(app.is_freeze_layout(clarisse_win))