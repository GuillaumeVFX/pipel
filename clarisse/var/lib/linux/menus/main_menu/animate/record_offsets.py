ix.enable_command_history()

app = ix.application
ix.api.SdkHelpers.record_offsets_items_selected(app)

ix.disable_command_history()
