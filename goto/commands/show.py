# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning


def show(magic, command, args, options):
    """
    Show magicword.
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='show')

    word = args[0]
    magic.show_shortcut(word)

    return None, None
