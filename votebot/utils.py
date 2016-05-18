# -*- coding: utf-8 -*-
"""
    votebot.utils
    ~~~~~~~~~~~~~

    A bunch of utility functions for the program.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
# local imports
import commands
#from commands import cmds


# Verifies the name format for a channel
# Prepends it with a "#", if it doesn't
# already start with one
# def verify_channel(channel):
#     if channel:
#         if not channel.startswith('#'):
#             channel = '#' + channel
#     else:
#         pass

#     return channel

#reload_links('../links.json')


def is_valid_cmd(cmd):
    return commands.cmds.has_key(cmd)
