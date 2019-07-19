# coding: utf-8
from __future__ import unicode_literals

import subprocess
from ..gotomagic.text import GotoError, GotoWarning


def vscode(magic, command, args, options):
    """
    Launch Visual Studio Code in the code folder
    """

    try:
        code = magic['code']
    except KeyError:
        return None, GotoWarning("no_magicword_named_code")

    try:
        subprocess.check_call('code "%s"' % code, shell=True)
    except subprocess.CalledProcessError:
        return None, GotoError("vscode_launch_failed")

    return None, None
