import collections
app = ix.application
menu = app.get_main_menu()


menu.add_command("Tools>")
menu.add_show_callback("Tools>", "./_show.py")

tools_menu = menu.get_item("Tools>")
menu.remove_all_commands(tools_menu.get_path())

# Items Shortcut
dico_shortcut = {'Select': 'q', 'Translate Item': 'w', 'Rotate Item': 'e', 'Scale Item': 'r', 'Transform Item': 't'}

classes = app.get_factory().get_classes().get_classes("Tool")

# reorder by UI Weight
classes_sort = {}
for i in range(classes.get_count()):
    classes_sort[classes[i]] = classes[i].get_ui_weight()
classes_sort = collections.OrderedDict(sorted(classes_sort.items(), key=lambda x: x[1], reverse=True))

# create a radio button group
m_radio_group_tools = None

first_item_category = False
tools_item_added = []
category = ""

working_directory = tools_menu.get_working_directory()

for i_category in range(len(classes_sort)):
    if i_category < len(classes_sort):
        category = classes_sort.keys()[i_category].get_category()
        first_item_category = True
        if category == "":
            continue
    else:
        category = ""

    for i in range(len(classes_sort)):
        current_class = classes_sort.keys()[i]
        ui_name = current_class.get_ui_name()
        if current_class.is_abstract() or current_class.is_under_licensed() or (ui_name in tools_item_added) or category != current_class.get_category():
            continue

        # create a category
        if first_item_category:
            menu.add_command("Tools>{" + category + "}", "", "")
            first_item_category = False

        if ui_name in dico_shortcut.keys():
            shortcut = dico_shortcut[ui_name]
        else:
            shortcut = ""

        # add the item
        file_path = working_directory + '/select_tool_action.py'
        command = "variables = {'object_class_name': '" + current_class.get_object_default_name() + "'}\n"
        command += "execfile('" + file_path + "', variables)"
        item = menu.add_command_as_script("ScriptingPython", "Tools>" + ui_name, command, shortcut)

        item.set_radio_group("tools_buttons")

        # add class icon
        item.set_icon(current_class)

        item.set_custom_data(current_class.get_object_default_name())
        tools_item_added.append(ui_name)
