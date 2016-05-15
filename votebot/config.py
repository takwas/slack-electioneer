# -*- coding: utf-8 -*-
"""
    votebot.config
    ~~~~~~~~~~~~~~

    Configuration for the bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""

# template text for building string
# representations for config classes
running_mode = 'App running in {mode} mode.'


# Base configuration class that
# will be extended
class Config:

    # standard library imports
    import os
    import textwrap

    TOKEN = os.getenv('SLACK_TOKEN', None)
    CMD_DELIMITER = ':'
    NICK_SUFFIX = ':'
    # Nicks of users who have control over a bot
    BOT_ADMINS = {
        'insaida': 'U0NA6G39N',
        'ichux': 'U0NAZ4CRL',
        'aishab': 'U0NE07PMJ',
        'acetakwas': 'U0NAKE0TT',
    }
    SOURCE_URL = 'https://github.com/takwas/pyung-slack-votebot'
    ABOUT = textwrap.dedent(
                        """
                        I'm just a bot. What do I know? ¯\_(ツ)_/¯
                        Name: Votebot
                        Profession: Electioneer
                        Author: @acetakwas
                        Source: {source_url}
                        """.format(source_url=SOURCE_URL)
                        )
    
    


# Configuration used during
# the development of our bot
class DevConfig(Config):

    NICKNAME = 'sawkat'
    #DEFAULT_CHANNELS = ('#bot-test', )

    def __repr__(self):
        return running_mode.format(mode='development')


# Configuration for testing the functionalities
# of our bot
class TestConfig(Config):

    NICKNAME = 'sawkat'
    #DEFAULT_CHANNELS = ('#bot-test', )

    def __repr__(self):
        return running_mode.format(mode='testing')


# Main configuration for when our bot is deployed on a server
class DeployConfig(Config):

    NICKNAME = 'votebot'  # The nick of the bot.
    #DEFAULT_CHANNELS = ('#bot-test', )

    def __repr__(self):
        return running_mode.format(mode='deploy')


config_modes = {
    'default': DevConfig,
    'dev': DevConfig,
    'deploy': DeployConfig,
    'test': TestConfig
}
