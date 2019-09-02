app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()

menu.remove_all_commands("Debug>")
ix.application.fill_debug_main_menu(clarisse_win , "Debug>")
menu.add_command("Debug>separator")
menu.add_command("Debug>Check all files path of Main Menu", "./check_all_file_paths.py")
