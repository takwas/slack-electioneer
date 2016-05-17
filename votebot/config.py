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


    TOKEN = os.getenv('VOTEBOT_TOKEN', None)
    ADMIN_TOKEN = os.getenv('VOTEBOT_ADMIN_TOKEN', None)
    CMD_DELIMITER = ':'
    NICK_SUFFIX = ':'
    CACHE_EXPIRY = 60 * 10 # 10 minutes
    # Nicks of users who have control over a bot
    BOT_ADMINS = {
        'insaida': 'U0NA6G39N',
        'ichux': 'U0NAZ4CRL',
        'aishab': 'U0NE07PMJ',
        'acetakwas': 'U0NAKE0TT',
    }
    VOTE_SYMBOL = 'white_check_mark'
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

    BOT_NAME = 'sawkat'
    STATS = {
        'C179BGHMY': {
            'office': 'test',
            'topic': 'Bot-Dev Testing Channel',
            'purpose': 'Test bots as you develop them.',
            'candidates': {}
        }
    }
    DATABASE_URL = 'sqlite:///votebot_dev_data.sqlite'

    def __repr__(self):
        return running_mode.format(mode='development')


# Configuration for testing the functionalities
# of our bot
class TestConfig(Config):

    BOT_NAME = 'sawkat'
    STATS = {
        'C195MMLKU': {
            'office': 'test',
            'topic': 'Vote System Testing Channel',
            'purpose': 'Pre-election testing.',
            'candidates': {}
        }
    }
    DATABASE_URL = 'sqlite:///votebot_test_data.sqlite'

    def __repr__(self):
        return running_mode.format(mode='testing')


# Main configuration for when our bot is deployed on a server
class DeployConfig(Config):

    BOT_NAME = 'votebot'  # The nick of the bot.
    STATS = {
        'C17JQ5RRT': {
            'office': 'Chairperson',
            'topic': 'Chairperson Voting Channel',
            'purpose': 'Conduct chairperson election.',
            'candidates': {}
        },
        'C17H9HHU3': {
            'office': 'Secretary',
            'topic': 'Secretary Voting Channel',
            'purpose': 'Conduct secretary election.',
            'candidates': {}
        },
        'C17JQQH0F': {
            'office': 'Treasurer',
            'topic': 'Treasurer Voting Channel',
            'purpose': 'Conduct treasurer election.',
            'candidates': {}
        }
    }
    DATABASE_URL = 'sqlite:///votebot_data.sqlite'

    def __repr__(self):
        return running_mode.format(mode='deploy')


config_modes = {
    'default': DevConfig,
    'dev': DevConfig,
    'deploy': DeployConfig,
    'test': TestConfig
}
