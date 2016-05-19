# -*- coding: utf-8 -*-
"""
    votebot.config
    ~~~~~~~~~~~~~~

    Configuration for the bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
# standard library imports
import os
import textwrap

# template text for building string
# representations for config classes
running_mode = 'App running in {mode} mode.'


# Base configuration class that
# will be extended
class Config:



    ADMIN_TOKEN = os.getenv('VOTEBOT_ADMIN_TOKEN', None)
    CMD_DELIMITER = ':'
    NICK_SUFFIX = ':'
    #CACHE_EXPIRY = 60 * 10 # 10 minutes
    # Nicks of users who have control over a bot
    BOT_ADMINS = {
        'tmdoubleu': 'U0U39CR8Q',
        'insaida': 'U0NA6G39N',
        'ichux': 'U0NAZ4CRL',
        'aishab': 'U0NE07PMJ',
        'acetakwas': 'U0NAKE0TT'
    }
    VOTE_SYMBOL = 'white_check_mark'
    SOURCE_URL = 'https://github.com/takwas/votebot'
    ABOUT = textwrap.dedent(
                        """
                        I'm just a bot. What do I know? ¯\_(ツ)_/¯
                        Name: Votebot
                        Profession: Electioneer
                        Author: @acetakwas
                        Source: {source_url}
                        """.format(source_url=SOURCE_URL)
                        )
    ELECTION_START_TIME = None
    ELECTION_END_TIME = None


# Configuration used during
# the development of our bot
class DevConfig(Config):

    DEBUG = True
    TOKEN = os.getenv('VOTEBOT_TOKEN_DEV', None)
    BOT_NAME = 'sawkat'
    STATS = {
        'C179BGHMY': {
            'office': 'test',
            'topic': 'Bot-Dev Testing Channel',
            'purpose': 'Test bots as you develop them.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {}
        }
    }
    DATABASE_URL = 'sqlite:///votebot_dev_data.sqlite'

    def __repr__(self):
        return running_mode.format(mode='development')


# Configuration for testing the functionalities
# of our bot
class TestConfig(Config):

    TESTING = True
    TOKEN = os.getenv('VOTEBOT_TOKEN_TEST', None)
    BOT_NAME = 'sawkat'
    STATS = {
        #'C195MMLKU': {
        'C19RDTTSQ': {
            'office': 'Test Office',
            'topic': 'Vote System Testing Channel',
            'purpose': 'Pre-election testing.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {
                'U0NAKE0TT' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NA6G39N' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAZ4CRL' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
            }
        },
        'C195MMLKU': {
            'office': 'Test Office 2',
            'topic': 'Vote System Testing Channel',
            'purpose': 'Pre-election testing.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {
                'U0NAKE0TT' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NA6G39N' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAZ4CRL' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
            }
        }
    }
    DATABASE_URL = 'sqlite:///votebot_test_data.sqlite'

    def __repr__(self):
        return running_mode.format(mode='testing')


# Main configuration for when our bot is deployed on a server
class DeployConfig(Config):

    DEPLOY = True
    TOKEN = os.getenv('VOTEBOT_TOKEN', None)
    BOT_NAME = 'votebot'  # The nick of the bot.
    STATS = {
        'C17JQ5RRT': {
            'office': 'Chairperson',
            'topic': 'Chairperson Voting Channel',
            'purpose': 'Conduct chairperson election.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {
                'U0UEMDE04' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAZ4CRL' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NE07PMJ' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                }
            }
        },
        'C17H9HHU3': {
            'office': 'Secretary',
            'topic': 'Secretary Voting Channel',
            'purpose': 'Conduct secretary election.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {
                'U0U39CR8Q' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAZ4CRL' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0TLPG83T' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NE07PMJ' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAKE0TT' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                }
            }
        },
        'C17JQQH0F': {
            'office': 'Treasurer',
            'topic': 'Treasurer Voting Channel',
            'purpose': 'Conduct treasurer election.',
            'live_ts': '',
            'log_ts': '',
            'election_status_ts': '',
            'election_status': False,
            'candidates': {
                'U0U39CR8Q' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NA6G39N' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0Q2DQCEA' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NE07PMJ' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
                'U0NAKE0TT' :  {
                    'post_ts' : '',
                    'votes_count' : 0
                },
            }
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
