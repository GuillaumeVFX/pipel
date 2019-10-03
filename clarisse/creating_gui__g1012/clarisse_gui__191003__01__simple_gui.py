window = ix.api.GuiWindow(ix.application, 0, 0, 640, 480)
window.show()
while window.is_shown(): ix.application.check_for_events()