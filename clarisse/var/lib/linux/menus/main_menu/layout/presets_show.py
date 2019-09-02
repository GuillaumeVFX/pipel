app = ix.application
menu = app.get_main_menu()

menu.remove_all_commands("Layout>Presets>")
item = menu.get_item("Layout>Presets>")
if item != None:
	working_directory = item.get_working_directory()

# populate layouts
list = app.get_viewport_layout_names()
for i in range(list.get_count()):
    file_path = working_directory + '/presets_action.py'
    command = "variables = {"
    command += "'layout_name': '" + list[i] + "'}\n"
    command += "execfile('" + file_path + "', variables)"
    menu.add_command_as_script("ScriptingPython", "Layout>Presets>" + list[i], command, "")

menu.add_command("Layout>Presets>separator", "", "")
menu.add_command("Layout>Presets>Store...", "./presets_store.py", "")
menu.add_command("Layout>Presets>Manage...", "./presets_manage.py", "")