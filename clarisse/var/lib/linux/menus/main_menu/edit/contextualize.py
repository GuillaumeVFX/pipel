ix.enable_command_history()

app = ix.application
ix.api.SdkHelpers.contextualize_items(app)

ix.disable_command_history()