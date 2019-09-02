menu = ix.application.get_main_menu()

menu.add_command("Layout>")
menu.add_show_callback("Layout>", "./_show.py")

menu.add_command("Layout>Presets>")
menu.add_show_callback("Layout>", "./presets_show.py")
menu.add_command("Layout>Presets>separator")
menu.add_command("Layout>Presets>Store...", "./presets_store.py")
menu.add_command("Layout>Presets>Manage...", "./presets_manage.py")

menu.add_command("Layout>separator")

item = menu.add_command("Layout>Freeze", "./freeze.py")
item.set_checkable(True)

menu.add_command("Layout>separator")

menu.add_command("Layout>Shelf Toolbar>Show/Hide", "./shelf_toolbar_show_hide.py")
menu.add_command("Layout>Shelf Toolbar>Reset To Default", "./shelf_toolbar_reset_to_default.py")

menu.add_command("Layout>separator")

menu.add_command("Layout>Clear All Viewports", "./clear_all_viewports.py")
