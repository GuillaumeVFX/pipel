app = ix.application
menu = app.get_main_menu()

menu.enable_command("Edit>Undo", app.get_command_manager().is_undoable())
menu.enable_command("Edit>Redo", app.get_command_manager().is_redoable())

has_selection = app.get_selection().get_count() != 0
menu.enable_command("Edit>Cut", has_selection)
menu.enable_command("Edit>Copy", has_selection)
menu.enable_command("Edit>Instantiate", has_selection)
menu.enable_command("Edit>Delete", has_selection)
menu.enable_command("Edit>Rename...", has_selection)
menu.enable_command("Edit>Group", has_selection)
menu.enable_command("Edit>Combine", has_selection)
menu.enable_command("Edit>Contextualize", has_selection)
menu.enable_command("Edit>Create Shading Layer>", has_selection)
menu.enable_command("Edit>Hide", has_selection)
menu.enable_command("Edit>Show", has_selection)
menu.enable_command("Edit>Disable", has_selection)
menu.enable_command("Edit>Enable", has_selection)
menu.enable_command("Edit>Color Tag>", has_selection)

menu.enable_command("Edit>Isolate>Isolate More", has_selection)
menu.enable_command("Edit>Isolate>Isolate Less", has_selection)

# Select All
flags = ix.api.CoreBitFieldHelper( ix.api.OfItem.FLAG_NONE, ix.api.OfItem.FLAG_NONE, ix.api.CoreBitFieldHelper.MODE_DISABLE, ix.api.CoreBitFieldHelper.MODE_DISABLE )

allow_select_all = True
working_context = ix.application.get_working_context()
if working_context.get_context_count(flags) == 0:
    project_items = ix.api.OfObjectArray()
    working_context.get_objects("ProjectItem", project_items, flags)
    if project_items.get_count() == 0:
        allow_select_all = False
menu.enable_command("Edit>Select All", allow_select_all)

menu.enable_command("Edit>Deselect All", ix.selection.get_count() > 0)

# Enable/Disable flags
allow_revert_overrides = False
allow_disable = False
allow_enable = False
for i in range(ix.selection.get_count()):
    if ix.selection[i].is_disabled():
        allow_enable = True
    else:
        allow_disable = True
    if ix.selection[i].is_overriden() or ix.selection[i].is_remote():
        allow_revert_overrides = True

menu.enable_command("Edit>Enable", allow_enable)
menu.enable_command("Edit>Disable", allow_disable)

# Revert Overrides flags
menu.enable_command("Edit>Revert Overrides", allow_revert_overrides)

