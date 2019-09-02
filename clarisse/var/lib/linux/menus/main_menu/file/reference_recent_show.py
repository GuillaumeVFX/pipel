from os.path import basename

menu = ix.application.get_main_menu()
menu.remove_all_commands("File>Reference>Recent>")

item = menu.get_item("File>Reference>Recent>")
if item != None:
    working_directory = item.get_working_directory()

recent_location = ix.application.get_recent_files("reference")
for i in range(recent_location.get_count()):
    filename = basename(recent_location[i])
    file_path = working_directory + '/reference_recent_action.py'

    cur_recent_location = recent_location[i]
    cur_recent_location = cur_recent_location.replace('\\', '\\\\')
    cur_recent_location = cur_recent_location.replace('\'', '\\\'')
    cur_recent_location = cur_recent_location.replace('\"', '\\\\"')
    
    command = "variables = {'reference_path': '" + cur_recent_location + "'}\n"
    command += "execfile('" + file_path + "', variables)"

    item_path = "File>Reference>Recent>" + str(i+1) + "    " + filename
    menu.add_command_as_script("ScriptingPython", item_path, command, "", recent_location[i])


menu.add_command("File>Reference>Recent>separator")
menu.add_command("File>Reference>Recent>Clear Recent", "./reference_clear_recent.py")