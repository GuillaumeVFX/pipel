app = ix.application
menu = app.get_main_menu()

menu.enable_command("File>Revert", app.get_current_project_filename() != "")

menu.enable_command("File>Open Recent>", app.get_recent_files("project").get_count() > 0)

menu.enable_command("File>Reference>Recent>", app.get_recent_files("reference").get_count() > 0)

# enabling/disabling Import submenu if the working context is not content locked
working_context = app.get_working_context()
menu.enable_command("File>Import>", working_context.is_editable() and not working_context.is_user_locked() and not working_context.is_content_locked())

menu.enable_command("File>Export>Geometry...", ix.selection.get_objects().get_count() > 0)

menu.enable_command("File>Export>Context As Project...", ix.selection.get_contexts().get_count() == 1)

menu.enable_command("File>Export>Context As Project With Dependencies...", ix.selection.get_contexts().get_count() == 1)
