app = ix.application
menu = app.get_main_menu()

windows_menu = menu.get_item("Windows>")

# Items Shortcut
dico_shortcut = {'Search': 'F3'}

classes = app.get_factory().get_classes().get_classes("Widget")
first_item_category = False

# alpha sort on classes
ui_name_sort = []
classes_sort = []
for i in range(classes.get_count()):
    ui_name_sort.append(classes[i].get_ui_name())
ui_name_sort = sorted(ui_name_sort)

for i in range(classes.get_count()):
    for j in range(classes.get_count()):
        if ui_name_sort[i] == classes[j].get_ui_name():
            classes_sort.append(classes[j])
            break

tools_item_added = []
for i_category in range(len(classes_sort)+1):
    if i_category < len(classes_sort):
        category = classes_sort[i_category].get_category()
        first_item_category = True
        if category == "":
            continue
    else:
        category = ""

    for i in range(len(classes_sort)):
        current_class = classes_sort[i]
        ui_name = current_class.get_ui_name()
        if current_class.is_ui_creatable() == False or (ui_name in tools_item_added) or category != current_class.get_category():
            continue

        # create a category
        if first_item_category:
            menu.add_command("Windows>{" + category + "}", "", "")
            first_item_category = False

        if ui_name in dico_shortcut.keys():
            shortcut = dico_shortcut[ui_name]
        else:
            shortcut = ""

        # add the item
        file_path = windows_menu.get_working_directory() + '/select_widget_action.py'

        command = "variables = {"
        command += "'class_object_default_name': '" + current_class.get_object_default_name() + "', "
        command += "'class_name': '" + current_class.get_name() + "', "
        command += "'class_ui_name': '" + current_class.get_ui_name() + "'"
        command += "}\n"
        command += "execfile('" + file_path + "', variables)"
        item = menu.add_command_as_script("ScriptingPython", "Windows>" + ui_name + "...", command, shortcut)
        item.set_icon(current_class)

        item.set_custom_data(current_class.get_object_default_name())
        tools_item_added.append(ui_name)
