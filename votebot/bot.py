# -*- coding: utf-8 -*-
"""
    votebot.votebot
    ~~~~~~~~~~~~~~~

    Bot (Slack client) module.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
from slackclient import SlackClient

from commands import cmds
from parser import ArgsParser
import utils

class VoteBot(SlackClient):

    # Create bot instance
    def __init__(self, config):
        SlackClient.__init__(self, config.TOKEN)
        self.config = config
        self.nickname = self.config.NICKNAME
        self.masters = self.config.BOT_ADMINS
        self.sourceURL = self.config.SOURCE_URL
        self.about = self.config.ABOUT
        self.parser = ArgsParser(bot=self)


    # Make bot connect and listen for events
    def listen(self):
        if self.rtm_connect():
            print 'Votebot connected! Listening...'
        else:
            print 'Votebot failed to connect!'
        while True:
            for message in self.rtm_read():
                # do something with message
                print message
                parse_msg(message)


def privmsg(self, user, channel, msg):
        """
        This will get called when the bot receives a message.

        :param user: absolute ID of user who sent the message. A typical
                    ID would look like this: sawkat!~sawkat@100.110.120.6
        :param channel: channel where the message was sent. The `channel`
                        is a channel if the message was sent in a
                        channel. The `channel` is the bot's nick if the
                        message

                        was sent as a private message
        :param msg: the message string that was sent
        """
        # Get nick of message sender
        user = user.split('!', 1)[0]

        user_is_admin = user in self.masters

        # Is this a private message to me?
        if channel == self.nickname:
            room = user
            response = self.parser.parse_msg(msg, sender=user)
        # Or is this a message directed at me from a channel?
        elif msg.startswith(self.nickname):
            room = channel
            # remove the nick and parse the message
            response = self.parser.parse_msg(msg[msg.find(' ')+1:], sender=user)

        # Process a response if allowed to talk
        if not self.stealth:
            msg = ''
            for line in response.get_response():
                msg += line+'\n'

            if response.is_general:
                if response.channel is not None:
                    self.msg_channel(response.channel, msg)
            elif room == user or (room == channel and response.is_private):
                self.msg_user(user, msg)
            elif room == channel and not response.is_private:
                self.msg_user_in_channel(channel, user, msg)


def parse_msg(msg):
    pass