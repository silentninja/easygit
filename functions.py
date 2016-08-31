import subprocess
from binascii import b2a_uu
import os


def which(program):

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def get_git():
    if hasattr(get_git, "_cache") is False:
        setattr(get_git, "_cache", which("git.exe") or which("git"))
    return getattr(get_git, "_cache")


def git(*commands):
    kwargs = get_subprocess_kwargs()
    subprocess.check_output(
        [get_git()] + list(commands), stderr=subprocess.STDOUT, **kwargs).decode("utf-8")


def call_git(*commands):
    kwargs = get_subprocess_kwargs()
    return subprocess.call([get_git()] + list(commands), **kwargs)


def git_output(*commands):
    try:
        kwargs = get_subprocess_kwargs()
        result = subprocess.check_output(
            [get_git()] + list(commands), **kwargs)
        result = b2a_uu(result)
    except:
        result = ""
    return result


def get_subprocess_kwargs():
    kwargs = {}
    if os.name == 'nt':
        errorlog = open(os.devnull, 'w')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs["stderr"] = errorlog
        kwargs["startupinfo"] = startupinfo
    return kwargs
