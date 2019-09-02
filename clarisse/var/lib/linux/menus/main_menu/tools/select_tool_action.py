import ix
app = ix.application

full_name = "project://" + object_class_name

tool_selected = app.get_factory().get_object(full_name)
if tool_selected != None:
    app.get_selection().set_all_slots_selection("tools", tool_selected)