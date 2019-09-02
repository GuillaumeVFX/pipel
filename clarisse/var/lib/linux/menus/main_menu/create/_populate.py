menu = ix.application.get_main_menu()

menu.add_command("Create>")
menu.add_show_callback("Create>", "./_show.py")
# execute the file "_show.py" when the main menu UI will displayed. (adding shortcuts of Create menu)
menu.add_show_callback(".", "./_show.py")
