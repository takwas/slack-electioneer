# -*- coding: utf-8 -*-
"""
    votebot.commands
    ~~~~~~~~~~~~~~~~

    Commands recognisable by bot.

    :author: Tosin Damilare James Animashaun (acetakwas@gmail.com)
    :copyright: (c) 2016 by acetakwas
    :license: see LICENSE for details.
"""

# standard library imports
import textwrap

# local imports
import actions


class Command(object):
    """
    This provides a wrapper object for a command. Each command that can
    be executed on the bot has it's own set of properties which are
    contained in this class.
    """

    def __init__(self, cmd, callback, help_text):

        # The command text for this command
        self.cmd = cmd

        # The callback function to execute when this command is run
        self.callback = callback

        # A text containing help information on how to use this command
        self.help_text = help_text

    def __repr__(self):
        return 'Command: <{cmd}>'.format(cmd=self.cmd)

    def execute(self, **kwargs):
        """
        Execute this command by running the callback function created
        with it. Return the result of the function afterwards.
        """
        return self.callback(**kwargs)


# A mapping of commands to their respective Command objects
#
# Currently included commands:
#     :help :about :inbox :link :log :masters :paste :ctrl
#     :whatdidimiss :resource :submit
cmds = {
    'help' : Command(cmd='help', callback=actions.do_help,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:help
                                    Show general help.

                                U2:\t:help <command>
                                    Show help for <command>. Use <U1> for a
                                    list of valid commands.
                            """
                            )
                            ),
    'about' : Command(cmd='about', callback=actions.do_about,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:about
                                    Show 'about' information for this bot.
                            """
                            )
                            ),
    'clear' : Command(cmd='clear', callback=actions.do_clear,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:clear
                                    Clear all messages in this channel.

                                U2:\t:clear <username1>[, <username2>...]
                                    Clear all messages from usernames in list of usernames in this channel.

                                U3:\t:clear log
                                    Clear all log messages from bot in this channel.
                            """
                            )
                            ),
    'initiate' : Command(cmd='initiate', callback=actions.do_initiate,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:initiate
                                    Prepare this channel for an election.
                            """
                            )
                            ),
    'setup' : Command(cmd='setup', callback=actions.do_setup,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:setup
                                    Do clean refresh of all data.
                            """
                            )
                            ),
    'session-start' : Command(cmd='session-start', callback=actions.do_session_start,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:session-start
                                    Start elections.
                            """
                            )
                            ),
    'session-stop' : Command(cmd='session-stop', callback=actions.do_session_stop,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:session-stop
                                    End elections.
                            """
                            )
                            ),
    'admins' : Command(cmd='admins', callback=actions.do_admins,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:admins
                                    Show the admins who can control this bot.
                            """
                            )
                            ),
    'say' : Command(cmd='say', callback=actions.do_say,
                        help_text=textwrap.dedent(
                            """
                            >>> *Usage:*

                                U1:\t:say
                                    Show help for this command.
                                U2:\t:say chan=<channel> <msg>
                                    Make the bot say <msg> in <channel>.
                            """
                            )
                            )
}


# def execute(cmd, **kwargs):
#     """
#     Executes the callback function for the given `cmd`.
#     """
#     cmd_obj = cmds.get(cmd, None)

#     if cmd_obj is not None:
#         return cmd_obj.callback(**kwargs)