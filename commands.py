

import os, sublime, sublime_plugin
from .functions import git

ERROR_NOT_INSTALLED = 'Git is not installed on your computer, we need it!'
ERROR_NOT_A_REPO = 'This folder is not a git repository! Make it one and try again'
ERROR_NOT_VALID_VIEW = 'This is not a valid file. Forgot to save it?'
ERROR_ADD = "Problem adding files, do it manually!"
ERROR_COMMIT = "Problem commiting files, do it manually!"
ERROR_PUSH = "Problem pushing files, do it manually!"


class AddThenCommitThenPushCommand(sublime_plugin.TextCommand):
    # exectue(git
    #if spawn(git, ["status"]) == "Not a git repository"
    #   echo("this is not a yet a git repository, please make it one and try again")
    #else:
    #   spawn(git, ["status"])
    def run(self, args, targeted):

        if not git():
            return sublime.error_message( ERROR_NOT_INSTALLED )

        if git('status') is not 0:
            return sublime.error_message( ERROR_NOT_A_REPO )

        def on_done(str):
            
            current_file = sublime.active_window().active_view().file_name()
            current_dir = os.path.dirname(current_file)

            if not current_file:
                return sublime.error_message( ERROR_NOT_VALID_VIEW )

            if targeted == "file":
                target = current_file
            else:
                target = "*"

            os.chdir(current_dir)
            
            if git('add', target) is not 0:
                return sublime.error_message( ERROR_ADD )
                
            if git('commit', '-m', str) is not 0:
                return sublime.error_message( ERROR_COMMIT )
            
            if git('push') is not 0:
                return sublime.error_message( ERROR_PUSH )

        sublime.active_window().show_input_panel(
            "Write a short description of your recent changes (the commit message)",
            "",
            on_done,
            lambda: 0,
            lambda: 0
        )  

