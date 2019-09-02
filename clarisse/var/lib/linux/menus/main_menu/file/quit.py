app = ix.application

# Propose to save the project if it's modified
reponse, filename = ix.check_need_save()

if reponse.is_yes():
    app.save_project(filename)

if not reponse.is_cancelled():
    app.quit()