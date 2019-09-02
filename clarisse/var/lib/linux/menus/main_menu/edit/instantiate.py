ix.enable_command_history()

items = ix.api.SdkHelpers.instantiate_items_selected(ix.application)

ix.selection.select(items)

ix.disable_command_history()