# -*- coding: utf-8 -*-
"""
votebot
~~~~~~~

A slack bot used for conducting elections.

:author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
:copyright: (c) 2016 by acetakwas
:license: see LICENSE for details.
"""


def create_votebot(config):
    """
    Factory function for creating a bot object. Uses `config` to
    determine appropriate settings and mode for the bot and application.
    """

    # local imports
    from bot import VoteBot
    

    # create factory protocol and application
    bot = VoteBot(config=config)
    return bot
