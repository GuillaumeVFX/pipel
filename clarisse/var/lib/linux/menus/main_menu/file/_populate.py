app = ix.application
menu = app.get_main_menu()

menu.add_command("File>")
menu.add_show_callback("File>", "./_show.py")

# new
menu.add_command("File>New>Scene", "./new_scene.py", "ctrl+n")
menu.add_command("File>New>Empty", "./new_empty.py", "ctrl+shift+n")

# open
item = menu.add_command("File>Open...", "./open.py", "ctrl+o")
item.set_icon(ix.api.GuiResource.open())
if app.is_advanced_features_enabled():
    item = menu.add_command("File>Open As Revision...", "./open_as_revision.py")
menu.add_command("File>Open Recent>")
menu.add_show_callback("File>", "./open_recent_show.py")
menu.add_command("File>Revert", "./revert.py")

# save
item = menu.add_command("File>Save", "./save.py", "ctrl+s")
item.set_icon(ix.api.GuiResource.save())
menu.add_command("File>Save As...", "./save_as.py", "shift+ctrl+s")
menu.add_command("File>Save Snapshot", "./save_snapshot.py", "shift+alt+s")

menu.add_command("File>separator")

# import
classes = app.get_factory().get_classes()
item = menu.add_command("File>Import>Geometry...", "./import_geometry.py")
item.set_icon(classes.get("Geometry"))
item = menu.add_command("File>Import>Volume...", "./import_volume.py")
item.set_icon(classes.get("GeometryVolume"))
item = menu.add_command("File>Import>Image...", "./import_image.py")
item.set_icon(classes.get("Image"))
item = menu.add_command("File>Import>Texture...>")
item.set_icon(classes.get("Texture"))
item = menu.add_command("File>Import>Texture...>Map File...", "./import_texture_map_file.py")
item.set_icon(classes.get("TextureMapFile"))
item = menu.add_command("File>Import>Texture...>Streaming Map File...", "./import_texture_streaming_map_file.py")
item.set_icon(classes.get("TextureMapFile"))
item = menu.add_command("File>Import>Project...", "./import_project.py")
item.set_icon(ix.api.GuiResource.save())

# export
item = menu.add_command("File>Export>Geometry...", "./export_geometry.py")
item.set_icon(classes.get("Geometry"))
item = menu.add_command("File>Export>Context As Project...", "./export_context_as_project.py")
item.set_icon(ix.api.GuiResource.save())
item = menu.add_command("File>Export>Context As Alembic...", "./export_alembic.py")
item.set_icon("./export_alembic.png")
item = menu.add_command("File>Export>Context As Project With Dependencies...", "./export_context_with_dependencies.py")
item.set_icon(ix.api.GuiResource.save())

# reference
item = menu.add_command("File>Reference>File...", "./reference_file.py")
menu.add_command("File>Reference>Recent>")
menu.add_show_callback("File>Reference>", "./reference_recent_show.py")
item.set_icon(ix.api.GuiResource.save())
if app.is_advanced_features_enabled():
    item = menu.add_command("File>Reference>Load All", "./reference_load_all.py")
    item.set_icon(ix.api.GuiResource.save())
menu.add_command("File>Reference>Make Local...", "./reference_make_local.py")
menu.add_command("File>Reference>Export Context...", "./reference_export_context.py")


menu.add_show_callback("File>Reference>", "./reference_show.py")

menu.add_command("File>separator")

menu.add_command("File>Reload Resources", "./reload_resources.py", "ctrl+shift+r")
menu.add_command("File>Resync Resources", "./resync_resources.py")

menu.add_command("File>separator")

menu.add_command("File>Quit", "./quit.py", "ctrl+q")

