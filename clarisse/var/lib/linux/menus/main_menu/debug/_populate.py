menu = ix.application.get_main_menu()

if ix.application.is_vendor_license_enabled():
    menu.add_command("Debug>")
    menu.add_show_callback("Debug>", "./_show.py")