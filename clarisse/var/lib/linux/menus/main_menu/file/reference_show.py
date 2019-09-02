app = ix.application
menu = app.get_main_menu()

# enabling/disabling Import submenu if the working context is not content locked
working_context = app.get_working_context()
enable_actions = working_context.is_editable() and not working_context.is_user_locked() and not working_context.is_content_locked() and not working_context.is_remote()

menu.enable_command("File>Reference>File...", enable_actions)

menu.enable_command("File>Reference>Make Local...", False)
menu.enable_command("File>Reference>Export Context...", False)

item_count = app.get_selection().get_count()
for i_item in range(0, item_count):
    item = app.get_selection().get_item(i_item)
    if item.is_context():
        ctx = item.to_context()
        if ctx.is_reference():
            if not ctx.is_remote():
                menu.enable_command("File>Reference>Make Local...", ctx.get_engine().supports_localize())
                menu.enable_command("File>Reference>Export Context...", True)
                break
        elif ctx.is_cap_delete():
            menu.enable_command("File>Reference>Export Context...", True)
