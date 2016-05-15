#!/usr/bin/env python
"""
    run
    ~~~

    Setup config and run application.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
# standard library imports
import os

# local imports
from votebot import create_votebot, config as conf

# Get running mode configuration from envvar or use default mode
config_mode = os.getenv('VOTEBOT_CONFIG_MODE', None)
if config_mode is None or config_mode not in ('dev', 'deploy', 'test'):
    print 'Value of environment variable: `VOTEBOT_CONFIG_MODE` not found or invalid!'
    print 'Using default configuration mode...'

config = conf.config_modes.get(config_mode)

# Get slack bot token from envvar
token = config.TOKEN
if token is None:
    print 'Environment variable: `SLACK_TOKEN` not found!'
    print 'Terminating...'
    sys.exit(1)


if __name__ == '__main__':
    print 'Votebot running...'
    
    votebot = create_votebot(config)
    votebot.listen()