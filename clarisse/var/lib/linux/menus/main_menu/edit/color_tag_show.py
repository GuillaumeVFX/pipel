ix.enable_command_history()

app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()

menu.remove_all_commands("Edit>Color Tag>")
app.fill_colortag_main_menu(clarisse_win, "Edit>Color Tag>")

ix.disable_command_history()