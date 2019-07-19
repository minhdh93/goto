# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning

def add(magic, command, args, options):
    """
    Add magicword
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword_and_uri", command='add')

    if (len(args) == 1):
        return None, GotoWarning("missing_uri",
                                 magicword=args[0],
                                 command='add')

    magicword = args[0]
    uri = args[1]

    magic.add_shortcut(magicword, uri)
    magic.save()

    return 'Added magic word {}'.format(magicword), None
