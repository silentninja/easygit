

import os
import sublime
import sublime_plugin
from .functions import git, git_output, call_git
from subprocess import CalledProcessError

ERROR_NOT_INSTALLED = 'Git is not installed on your computer, we need it!'
ERROR_NOT_A_REPO = 'This folder is not a git repository! Make it one and try again'
ERROR_NOT_VALID_VIEW = 'This is not a valid file. Forgot to save it?'
ERROR_ADD = "Problem adding files, do it manually!"
ERROR_COMMIT = "Problem commiting files, do it manually!"
ERROR_PUSH = "Problem pushing files, do it manually!"


class AddThenCommitThenPushCommand(sublime_plugin.TextCommand):
    # exectue(git
    # if spawn(git, ["status"]) == "Not a git repository"
    #   echo("this is not a yet a git repository, please make it one and try again")
    # else:
    #   spawn(git, ["status"])

    def run(self, args, targeted):
        current_view = sublime.active_window().active_view()
        current_file = current_view.file_name()
        current_dir = os.path.dirname(current_file)

        os.chdir(current_dir)

        if not call_git():
            return sublime.error_message(ERROR_NOT_INSTALLED)
        try:
            git('status')
        except Exception as e:
            return sublime.error_message(ERROR_NOT_A_REPO)

        def on_done(str):

            if not current_file:
                return sublime.error_message(ERROR_NOT_VALID_VIEW)

            if targeted == "file":
                target = current_file
            elif targeted == 'all':
                target = '-A'
            else:
                target = "."
            if current_view.is_dirty():
                current_view.run_command('save')

            # if git_output('status').find('nothing to commit') != -1:
            #     return sublime.message_dialog("Everything up to date!")

            # git('reset', 'HEAD', target)
            try:
                git('add', target)
                git('commit', '-m', str)
                git('push')
                return sublime.message_dialog("Easy-Git Success!")
            except CalledProcessError as e:
                sublime.error_message("Error when performing: " + ' '.join(
                    e.cmd) + "\n Error Message: " + e.output.decode("utf-8"))

        sublime.active_window().show_input_panel(
            "Write a short description of your recent changes (the commit message)",
            "",
            on_done,
            lambda: 0,
            lambda: 0
        )
