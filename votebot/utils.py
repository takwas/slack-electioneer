# -*- coding: utf-8 -*-
"""
    votebot.utils
    ~~~~~~~~~~~~~

    A bunch of utility functions for the program.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""

import config

# Verifies the name format for a channel
# Prepends it with a "#", if it doesn't
# already start with one
def verify_channel(channel):
    if channel:
        if not channel.startswith('#'):
            channel = '#' + channel
    else:
        pass

    return channel

# returns a list of valid link names
def get_link_names(links_data):
    links_list = []
    for key, value in links_data.iteritems():
        links_list.append(key)

    return links_list

# To reload  data from the json file
def reload_links(filename):
    # standard library imports
    import json

    with open(filename) as f:
        links_data = json.load(f)

    return links_data

#reload_links('../links.json')
def is_valid_cmd(cmd):
    from commands import cmds

    return cmds.has_key(cmd)

#def get_help_string(param_count=0):

#    for i in range(param_count):
