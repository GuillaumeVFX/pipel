menu = ix.application.get_main_menu()

menu.add_command("Image>Edit Channel Layers...", "./edit_channel_layers.py", "ctrl+l")
menu.add_command("Image>Edit File Format/Color Space Mapping...", "./edit_color_space.py", "")
menu.add_command("Image>separator")
menu.add_command("Image>Color Manager...", "./edit_color_manager.py", "ctrl+j")

