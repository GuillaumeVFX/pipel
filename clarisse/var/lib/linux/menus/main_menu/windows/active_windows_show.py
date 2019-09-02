app = ix.application
menu = app.get_main_menu()
menu.remove_all_commands("Windows>Active Windows>")

working_directory = menu.get_item("Windows>Active Windows>").get_working_directory()

clarisse_win = app.get_event_window()
sub_win_count = app.get_sub_windows_count(clarisse_win)
for i in range(sub_win_count):
    title = "Windows>Active Windows>" + str(i+1) + ". " + app.get_sub_windows(clarisse_win, i).get_title() + "..."

    file_path = working_directory + '/active_windows_action.py'

    command = "variables = {'sub_win_index': '" + str(i) + "'}\n"
    command += "execfile('" + file_path + "', variables)"

    menu.add_command_as_script("ScriptingPython", title, command, "", "")
