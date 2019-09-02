ix.enable_command_history()

app = ix.application
ix.api.SdkHelpers.remove_offsets_items_selected(app)

ix.disable_command_history()
