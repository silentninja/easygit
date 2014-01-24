import os, sys, sublime, sublime_plugin, subprocess
from .functions import get_git

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def plugin_loaded():
    """The ST3 entry point for plugins."""
    git = get_git()
    if not git:
        sublime.error_message('Git is not installed on your computer, we need it!')
        return
    status = subprocess.call([git, 'status'], startupinfo=startupinfo)
    if status is not 0:
        sublime.error_message('This folder is not a git repository! Make it one and try again')
        return
    print("Everything ok")

