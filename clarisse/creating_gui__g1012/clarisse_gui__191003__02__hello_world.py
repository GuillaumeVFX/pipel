window = ix.api.GuiWindow(ix.application, 0, 0, 640, 480)
label = ix.api.GuiLabel(window, 0, 0, 640, 480, "Hello World")
label.set_justification(ix.api.GuiWidget.JUSTIFY_CENTER)
window.show()
while window.is_shown(): ix.application.check_for_events()