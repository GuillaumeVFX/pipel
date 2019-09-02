app = ix.application
menu = app.get_main_menu()

enable = app.is_enable_motion_key_options()
menu.enable_command("Animate>Set Motion Key...", enable)
menu.enable_command("Animate>Delete Motion Key...", enable)


scene_objects_selected = False
item_count = app.get_selection().get_count()
for i in range(item_count):
    item = app.get_selection().get_item(i)
    if item.is_object():
        obj = item.to_object()
        if obj.get_module().is_kindof(ix.api.ModuleSceneObject.class_info()):
            scene_objects_selected = True;
            break

menu.enable_command("Animate>Center Pivot To BBox", scene_objects_selected)
menu.enable_command("Animate>Center Pivot To Ground", scene_objects_selected)
menu.enable_command("Animate>Reset Pivots", scene_objects_selected)
menu.enable_command("Animate>Conform Pivots", scene_objects_selected)
menu.enable_command("Animate>Remove Offsets", scene_objects_selected)
menu.enable_command("Animate>Record Offsets", scene_objects_selected)
menu.enable_command("Animate>Reset Transforms", scene_objects_selected)
