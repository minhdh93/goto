#!/usr/bin/env python
# coding: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import, unicode_literals, print_function
from builtins import dict, str  # redefine dict and str to be py3-like in py2.
# http://johnbachman.net/building-a-python-23-compatible-unicode-sandwich.html

import os
import sys
import codecs
from functools import reduce

from .settings import GOTOPATH
from .gotomagic import text
from .gotomagic.magic import GotoMagic
from .gotomagic.utils import healthcheck, print_utf8, fix_python2
from .commands import command_map, default
from .plugins import plugin_map

commands_and_plugins = command_map.copy()
commands_and_plugins.update(plugin_map)

def main():

    fix_python2()
    make_sure_we_print_in_utf8()

    exit_if_unhealthy()
    exit_with_usage_if_needed()

    project = sys.argv[1]
    magic = GotoMagic(project)
    argv = sys.argv[2:]

    command, argv = parse_command(argv)
    args = list(filter(lambda word: not word.startswith('-'), argv))
    options = list(filter(lambda word: word.startswith('-'), argv))

    if not command and len(args) == 0:
        output = usage()
        print_utf8(output)
        exit(0)

    output, err = run_command(magic, command, args, options)

    if output:
        print_utf8(output)

    if err:
        print_utf8(err.message)
        exit(1)

    exit(0)


def parse_command(argv):
    global commands_and_plugins

    for arg in argv:
        if arg in commands_and_plugins.keys() or arg in ['help', '--help', '-h', '/?']:
            command = arg
            argv.remove(arg)
            return command, argv

    return None, argv


def run_command(magic, command, args, options):
    global commands_and_plugins

    if command in ['help', '--help', '-h', '/?']:
        return usage(), None

    if command:
        return commands_and_plugins[command].run(magic, command, args, options)
    else:
        return default.run(magic, None, args, options)


def exit_if_unhealthy():
    err = healthcheck()
    if err:
        print_utf8(err.message)
        exit(1)


def exit_with_usage_if_needed():
    if len(sys.argv) < 3:
        output = usage()
        print_utf8(output)
        exit(0)


def make_sure_we_print_in_utf8():
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7


def usage():
    global command_map, plugin_map
    """
    Get information about usage
    """

    header = """
Goto - the magic traveler, how may I help you?

Wondering how to change project?
    project help                  Consult my brother in command

Basic usage
    goto <magicword>      Go to shortcut
    goto [<magicword>...] Go to many shortcuts
"""

    def map_to_text(title, command_map):
        commands_help = set([x for x in command_map.values()])
        commands_help = list(map(lambda x: x.help(), commands_help))
        commands_help = sorted(commands_help)
        commands_help = sorted(commands_help, key=lambda x: x.startswith('-'), reverse=False)
        commands_help = reduce(lambda x,y: x + "    goto {}\n".format(y), commands_help, "\n{}\n".format(title))
        return commands_help

    return "{}{}{}".format(header, map_to_text('Commands', command_map), map_to_text('Plugins', plugin_map))

if __name__ == '__main__':
    main()
