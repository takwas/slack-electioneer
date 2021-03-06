# -*- coding: utf-8 -*-
"""
    votebot.parser
    ~~~~~~~~~~~~~~

    Parser for messages sent to bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""
# local imports
import utils
import commands
from actions import Response


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
        try:
            msg = msg.strip()
        except AttributeError:
            msg = ''
        msg = msg +' '

        # Use the delimiter to know if this is a message to try to parse.
        if msg[0] == self.cmd_delimiter:
            # search for the first whitespace in the message to extract
            # the command part of it
            cmd_width = msg.find(' ')
            cmd = msg[1:cmd_width]

            if utils.is_valid_cmd(cmd):
                try:
                    return commands.cmds.get(cmd).execute(bot=self.bot, msg=msg[cmd_width:].strip(), **kwargs)
                except AttributeError:
                    pass
            # elif self.bot.waiting:
            #     if msg.startswith(':names'):
            #         bot.save_candidates(msg.split(':names')[1].strip())
            
            return Response("Invalid command!. Type ':help' for help")
