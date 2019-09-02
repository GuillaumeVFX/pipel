app = ix.application
menu = app.get_main_menu()
clarisse_win = app.get_event_window()

# remove all items
menu.remove_all_commands("Create>")

app.fill_create_main_menu(clarisse_win, "Create>")

working_context = app.get_working_context();
enabled = working_context.is_editable() and not working_context.is_user_locked() and not working_context.is_content_locked() and not working_context.is_remote()

command_list = menu.get_sub_commands("Create>", False, True)
for i in range(command_list.get_count()):
    menu.enable_command(command_list[i], enabled)