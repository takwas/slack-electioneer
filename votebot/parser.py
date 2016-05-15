# -*- coding: utf-8 -*-
"""
    votebot.parser
    ~~~~~~~~~~~~~~

    Parser for messages sent to bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""


class ArgsParser(object):
    """
    This object will handle parsing of messages received by a bot.

    Typical messages include a command, followed by arguments.
    """

    def __init__(self, bot, cmd_delimiter=None):
        """
        Constructs a parser object taking in the delimiter to use in
        identifying the command part of the received message.
        """
        self.cmd_delimiter = cmd_delimiter if cmd_delimiter is not None \
            else bot.config.CMD_DELIMITER
        self.bot = bot

    def parse_msg(self, msg, **kwargs):
        """
        This method does the actual parsing, and it accepts as a
        parameter, the message to parse.
        """
        # strip message of leading and trailing whitespace chars
        msg = msg.strip()
        msg = msg +' '

        # Use the delimiter to know if this is a message to try to parse.
        if msg[0] == self.cmd_delimiter:
            # search for the first whitespace in the message to extract
            # the command part of it
            cmd_width = msg.find(' ')
            cmd = msg[1:cmd_width]

            from utils import is_valid_cmd

            if is_valid_cmd(cmd):
                from commands import cmds
                try:
                    return cmds.get(cmd).callback(bot=self.bot, msg=msg[cmd_width:].strip(), **kwargs)
                except AttributeError:
                    pass
            
            from actions import Response
            return Response("Invalid command!. Type ':help' for help")

    # def parse_msg_cmd(self, msg):
    #     msg = msg.strip()
    #     pass

    # def parse_msg_args(self, msg):
    #     msg = msg.strip()
    #     cmd_width = msg.find(' ')

    #     while True:
    #         cmd_width = msg[cmd_width:].find(' ')
    #         #if cmd_width
    #     pass
