menu = ix.application.get_main_menu()

menu.add_command("Edit>")
menu.add_show_callback("Edit>", "./_show.py")

menu.add_command("Edit>Undo", "./undo.py", "ctrl+z", "Undo last action")
menu.add_command("Edit>Redo", "./redo.py", "ctrl+shift+z", "Redo last action")

menu.add_command("Edit>separator")

menu.add_command("Edit>Cut", "./cut.py", "ctrl+x", "Cut current selection and copy it to the clipboard")
menu.add_command("Edit>Copy", "./copy.py", "ctrl+c", "Copy current selection to the clipboard")
menu.add_command("Edit>Copy With Dependencies", "./copy_with_dependencies.py", "ctrl+shift+d", "Copy current selection to the clipboard, including external dependencies")
menu.add_command("Edit>Paste", "./paste.py", "ctrl+v", "Paste the content of the clipboard")
menu.add_command("Edit>Instantiate", "./instantiate.py", "ctrl+i", "Create instances from the selection")

menu.add_command("Edit>separator")

menu.add_command("Edit>Revert Overrides", "./revert_overrides.py")

menu.add_command("Edit>separator")

menu.add_command("Edit>Select All", "./select_all.py", "ctrl+a", "Select all the content of the current context")
menu.add_command("Edit>Deselect All", "./deselect_all.py","", "Deselect all items")
menu.add_command("Edit>Unload Resources", "./unload_resources.py","", "Unload all resources from memory")
# Select
menu.add_command("Edit>Select>Instances", "./select_instances.py", "ctrl+pgdown", "Select all instances from the selected sources")
menu.add_command("Edit>Select>Instances Recursively", "./select_instances_recursively.py", "", "Select all instances recursively")
menu.add_command("Edit>Select>Sources", "./select_sources.py", "ctrl+pgup", "Select all sources from the selected instances")
menu.add_command("Edit>Select>Sources Recursively", "./select_sources_recursively.py","","Select all sources recursively")
menu.add_command("Edit>Select>separator")
menu.add_command("Edit>Select>Outputs", "./select_outputs.py", "alt+pgdown", "Select items on which the selection is connected to")
menu.add_command("Edit>Select>Outputs Recursively", "./select_outputs_recursively.py", "", "Select outputs recursively")
menu.add_command("Edit>Select>Inputs", "./select_inputs.py", "alt+pgup", "Select items that are connected to the selection")
menu.add_command("Edit>Select>Inputs Recursively", "./select_inputs_recursively.py", "", "Select inputs recursively")
menu.add_command("Edit>Select>separator")
menu.add_command("Edit>Select>All Dependencies", "./select_all_dependencies.py", "shift+alt+a", "Select both input and output connections from the selected items")
menu.add_command("Edit>Select>separator")
menu.add_command("Edit>Select>Previous Selection", "./set_previous_selection.py", "bkspace", "Go back to the selection history")
menu.add_command("Edit>Select>Next Selection", "./set_next_selection.py", "shift+bkspace", "Go forward to the selection history")

menu.add_command("Edit>separator")

menu.add_command("Edit>Delete", "./delete.py", "del", "Delete Selected Object")
menu.add_command("Edit>Permanently Delete", "./trash.py", "shift+del", "Permanently Delete Selected Object")
menu.add_command("Edit>Rename...", "./rename.py", "f2", "Rename Selected Object")

menu.add_command("Edit>separator")

menu.add_command("Edit>Group", "./group.py", "", "Group selected objects")
menu.add_command("Edit>Combine", "./combine.py", "", "Combine selected objects")
menu.add_command("Edit>Contextualize", "./contextualize.py", "", "Move the selection in a newly created context")

menu.add_command("Edit>separator")

menu.add_command("Edit>Create Shading Layer>Use Full Names", "./create_sl_use_full_name.py", "", "Create a new shading layer from selected objects using absolute names")
menu.add_command("Edit>Create Shading Layer>Use Relative Names", "./create_sl_use_relative_name.py", "", "Create a new shading layer from selected objects using relative names")
menu.add_command("Edit>Create Shading Layer>Use Kinematics", "./create_sl_use_kinematics.py", "", "Create a new shading layer from selected objects using kinematics names")
menu.add_command("Edit>Create Shading Layer>Use Shading Groups Names", "./create_sl_use_shading_groups_name.py", "", "Create a new shading layer from selected objects using shading group names")

menu.add_command("Edit>separator")

menu.add_command("Edit>Hide", "./hide.py", "ctrl+h", "Hide selection from the 3D View")
menu.add_command("Edit>Show", "./show.py", "shift+h", "Unhide selection from the 3D View")

menu.add_command("Edit>Isolate>Isolate", "./isolate.py", "shift+i", "Isolate selection in the 3D View")
menu.add_command("Edit>Isolate>Isolate More", "./isolate_more.py", "", "Add selection to isolated items")
menu.add_command("Edit>Isolate>Isolate Less", "./isolate_less.py", "", "Remove selection from isolated items")
menu.add_command("Edit>Isolate>Isolate Swap", "./isolate_swap.py", "", "Swap currently isolated items with the ones that are not")

menu.add_command("Edit>separator")


menu.add_command("Edit>Disable", "./disable.py", "ctrl+d", "Disable currently selected items")
menu.add_command("Edit>Enable", "./enable.py", "shift+d", "Enable currently selected items")
menu.add_command("Edit>Color Tag>")
menu.add_show_callback("Edit>Color Tag>", "./color_tag_show.py")

menu.add_command("Edit>separator")

menu.add_command("Edit>Preferences...", "./preferences.py", "ctrl+k", "Edit Clarisse Preferences")
