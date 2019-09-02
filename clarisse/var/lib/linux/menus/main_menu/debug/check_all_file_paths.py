import os.path

app = ix.application
menu = app.get_main_menu()

error_count = 0

def check_file_exists(filename, accept_empty):
    path = filename
    if path == "" and accept_empty:
        return True
    if not os.path.isfile(path):
        return False
    directory, filename = os.path.split(path)
    return filename in os.listdir(directory)


list = ix.application.get_main_menu().get_all_commands(True)
for i in range(list.get_count()):
    item = menu.get_item(list[i])

    if item.is_command() or item.is_menu():
        # check action file of command
        if item.get_type() == ix.api.AppMainMenuItem.TYPE_COMMAND_WITH_FILE:
            if not check_file_exists(item.get_action_file_fullpath(), False):
                ix.log_warning('The "Action" file of item menu "' + item.get_path() + '" is not found ("' + item.get_action_file_fullpath() + '").' )
                error_count += 1

        # check action show file of command
        action_files_show = item.get_action_files_show_fullpath()
        for i in range(action_files_show.get_count()):
            if not check_file_exists(action_files_show[i], True):
                ix.log_warning('The "Action Show" file of item menu "' + item.get_path() + '" is not found ("' + action_files_show[i] + '").' )
                error_count += 1

        # check icon path
        if not check_file_exists(item.get_icon_fullpath(), True):
            ix.log_warning('The icon of item menu "' + item.get_path() + '" is not found ("' + item.get_icon_fullpath() + '").' )
            error_count += 1

ix.log_warning("Check all action files of Main Menu: " + str(error_count) + " error found.")
