

import os, sublime, sublime_plugin
from .functions import get_git
from .functions import git





class AddThenCommitThenPushCommand(sublime_plugin.TextCommand):
    # exectue(git
    #if spawn(git, ["status"]) == "Not a git repository"
    #   echo("this is not a yet a git repository, please make it one and try again")
    #else:
    #   spawn(git, ["status"])
    def run(self, edit):
        gitexe = get_git()
        if not gitexe:
            sublime.error_message('Git is not installed on your computer, we need it!')
            return
        if git('status') is not 0:
            sublime.error_message('This folder is not a git repository! Make it one and try again')
            return

        def on_done(str):
            current_file = sublime.active_window().active_view().file_name()
            if not current_file:
                sublime.error_message('This is not a valid file. Forgot to save it?')
                return
            current_dir = os.path.dirname(current_file)
            os.chdir(current_dir)
            exit_code = git('add', current_file)
            if exit_code is not 0:
                sublime.error_message("Problem adding files, do it manually!")
                return
            exit_code |= git('commit', '-m', str)
            if exit_code is not 0:
                sublime.error_message("Problem commiting files, do it manually!")
                return
            exit_code |= git('push')
            if exit_code is not 0:
                sublime.error_message("Problem pushing files, do it manually!")
                return


        sublime.active_window().show_input_panel(
            "Write a short description of your recent changes (the commit message)",
            "",
            on_done,
            lambda: 0,
            lambda: 0
        )  

