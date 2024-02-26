#!/usr/bin/env python3
import shlex
from Deadline.Plugins import *
import logging

def AlterCommandLine(executable, arguments, workingDirectory):
    """Our executable only holds a dummy command. This callback
    remaps the first argument to be the executable.
    Args:
        executable (str): The executable
        arguments (str): The arguments
        workingDirectory (str): The working directory
    Returns:
        executable (str): The executable
        arguments (str): The arguments
        workingDirectory (str): The working directory
    """

    deadlinePlugin_accessor.LogInfo("Run Command: '{}'".format(arguments))
    elements = shlex.split(arguments)
    executable = elements[0]
    arguments = shlex.join(elements[1:])
    return (executable, arguments, workingDirectory)


deadlinePlugin_accessor = None

def __main__(deadlinePlugin):
    global deadlinePlugin_accessor
    deadlinePlugin_accessor = deadlinePlugin

    # Setup JobPreLoad
    deadlinePlugin.ModifyCommandLineCallback += AlterCommandLine