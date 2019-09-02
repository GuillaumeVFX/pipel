app = ix.application
menu = app.get_main_menu()
list = menu.get_sub_commands("Tools>", False)
try:
    item = app.get_selection().get_item("tools", 0)

    name_selection = item.get_name()
    for name_item in list:
        item = menu.get_item(name_item)
        object_name = item.get_custom_data()
        # separator
        if object_name == "":
            continue
        # select the current selected tool
        if name_selection == item.get_custom_data():
            item.set_checked(True)
            break
except:
    None
        