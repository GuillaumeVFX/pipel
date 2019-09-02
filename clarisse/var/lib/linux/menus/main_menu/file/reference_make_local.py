app = ix.application

context_items = ix.api.CoreStringVector()

for i in range(app.get_selection().get_count()):
    item = app.get_selection().get_item(i)
    if item.is_context():
        context_items.add(item.get_full_name())
    else:
        ix.log_warning("Make Local: cannot localize '%s', only contexts can be localized." % (item.get_name()))

if context_items.is_empty() == False:
    ix.enable_command_history()

    clarisse_win = app.get_event_window()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    app.disable()
    ix.reference_make_local(context_items)
    app.enable()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_DEFAULT)

    ix.disable_command_history()
