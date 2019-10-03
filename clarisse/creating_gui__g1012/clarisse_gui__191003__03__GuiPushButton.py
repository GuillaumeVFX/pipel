class MyButton(ix.api.GuiPushButton):
    def __init__(self, parent, x, y, w, h, label):
        ix.api.GuiPushButton.__init__(self, parent, x, y, w, h, label)
        self.connect(self, 'EVT_ID_PUSH_BUTTON_CLICK', self.on_click)

    def on_click(self, sender, evtid):
        self.set_label('Pressed')

window = ix.api.GuiWindow(ix.application, 0, 0, 640, 480)
button = MyButton(window, 0, 0, 128, 22, "Press Me!")
window.show()
while window.is_shown(): ix.application.check_for_events()