
import sublime
import subprocess
import sublime_plugin
from .functions import get_git



class AddThenCommitThenPushCommand(sublime_plugin.TextCommand):
    # exectue(git
    #if spawn(git, ["status"]) == "Not a git repository"
    #   echo("this is not a yet a git repository, please make it one and try again")
    #else:
    #   spawn(git, ["status"])
    subprocess.call([get_git(), 'status'])
    pass
