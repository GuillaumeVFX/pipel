app = ix.application

if app.message_box("Do you really want to reset shelf toolbar to default?", "Isotropix Clarisse: Warning", ix.api.AppDialog.no(), ix.api.AppDialog.STYLE_YES_NO).is_yes():
    app.reset_default_shelf()