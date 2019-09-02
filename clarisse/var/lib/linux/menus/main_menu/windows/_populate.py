app = ix.application
menu = app.get_main_menu()

item = menu.add_command("Windows>")

menu.add_show_callback("Windows>", "./_show.py")

menu.add_command("Windows>New Clarisse...", "./new_clarisse.py")

# populate widgets list
menu.run_file("./_populate_widgets.py")

menu.add_command("Windows>separator")

menu.add_command("Windows>Active Windows>", "./active_windows.py")
menu.add_show_callback("Windows>Active Windows>", "./active_windows_show.py")

menu.add_command("Windows>separator")

menu.add_command("Windows>Hide/Show Subwindows", "./show_subwindows_tab.py", "`")

menu.add_command("Windows>separator")

item = menu.add_command("Windows>Close Current", "./close_current.py")
icon = ix.api.GuiResource.viewport_close()
if icon != None:
    item.set_icon(icon)
