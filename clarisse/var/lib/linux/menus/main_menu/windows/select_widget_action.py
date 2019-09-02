import ix
app = ix.application

#object = app.get_factory().add_object(class_object_default_name, class_name)

clarisse_win = app.get_event_window()
x = ix.api.Gui.get_mouse_screen_position_x()
y = ix.api.Gui.get_mouse_screen_position_y()

app.open_new_floating_widget_window(clarisse_win, class_name, "", x-25, y-30, 512, 384)
