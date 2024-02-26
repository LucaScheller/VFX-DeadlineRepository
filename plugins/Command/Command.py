#!/usr/bin/env python3

from __future__ import absolute_import

import os
import re

from Deadline.Plugins import DeadlinePlugin, PluginType
from Deadline.Scripting import RepositoryUtils
from six.moves import range


def GetDeadlinePlugin():
    return CommandPlugin()
    
def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()
    
class CommandPlugin(DeadlinePlugin):
    completedFrames = 0
    
    def __init__( self ):
        import sys
        if sys.version_info.major == 3:
            super().__init__()
        # Internals
        self.frame_start = None
        self.frame_end = None
        self.frame_increment = None
        self.frame_current = None
        # Process
        self.InitializeProcessCallback += self.InitializeProcess
        # Command
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        # Pre/Post Task
        self.PreRenderTasksCallback += self.PreRenderTasks
        self.PostRenderTasksCallback += self.PostRenderTasks
    
    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback
        
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
        del self.PreRenderTasksCallback
        del self.PostRenderTasksCallback
    
    def InitializeProcess( self ):
        # Settings
        self.PluginType = PluginType.Simple
        self.SingleFramesOnly = False
        self.StdoutHandling = True
        self.PopupHandling = False

        return

        # Stdout Handlers
        self.AddStdoutHandlerCallback( ".*Progress: (\d+)%.*" ).HandleCallback += self.HandleProgress
        self.AddStdoutHandlerCallback( "(Couldn't find renderer.*)" ).HandleCallback += self.HandleStdoutRenderer
        self.AddStdoutHandlerCallback( "(Error: Unknown option:.*)" ).HandleCallback += self.HandleStdoutUnknown
        self.AddStdoutHandlerCallback( "(Error: .*)" ).HandleCallback += self.HandleStdoutError
        self.AddStdoutHandlerCallback(r"(ERROR\s*\|.*)").HandleCallback += self.HandleStdoutError
        self.AddStdoutHandlerCallback(r"\[Error\].*").HandleCallback += self.HandleStdoutError
        self.AddStdoutHandlerCallback( ".*(No licenses could be found to run this application).*" ).HandleCallback += self.HandleStdoutLicense
        self.AddStdoutHandlerCallback( ".*ALF_PROGRESS ([0-9]+)%.*" ).HandleCallback += self.HandleStdoutFrameProgress
        self.AddStdoutHandlerCallback( ".*Render Time:.*" ).HandleCallback += self.HandleStdoutFrameComplete
        self.AddStdoutHandlerCallback( ".*Finished Rendering.*" ).HandleCallback += self.HandleStdoutDoneRender
        self.AddStdoutHandlerCallback( ".*ROP type: (.*)" ).HandleCallback += self.SetRopType
        self.AddStdoutHandlerCallback( ".*?(\d+)% done.*" ).HandleCallback += self.HandleStdoutFrameProgress
        self.AddStdoutHandlerCallback( "\[render progress\] ---[ ]+(\d+) percent" ).HandleCallback += self.HandleStdoutFrameProgress
        self.AddStdoutHandlerCallback( "(License error: No license found)").HandleCallback += self.HandleStdoutLicense
        self.AddStdoutHandlerCallback( "RMAN_PROGRESS *([0-9]+)%" ).HandleCallback += self.HandleStdoutFrameProgress

    def RenderExecutable( self ):
        # This will be replaced via our JobPreLoad.py
        return os.path.join(os.path.dirname(__file__), "mock_executable")
        
    def RenderArgument(self):
        command = self.GetPluginInfoEntryWithDefault("Command", "").strip()
        # Path Mappings
        command = RepositoryUtils.CheckPathMapping(command)
        # Frame Range
        frame_start = self.GetStartFrame()
        frame_end = self.GetEndFrame()
        frame_count = max(0, frame_end - frame_start) + 1
        frame_increment = 1

        self.frame_start = frame_start
        self.frame_end = frame_end
        self.frame_increment = frame_increment
        self.frame_current = frame_start

        command = re.sub( r"<(?i)FRAME_START>", str(frame_start), command)
        command = re.sub( r"<(?i)FRAME_END>", str(frame_end), command)
        command = re.sub( r"<(?i)FRAME_COUNT>", str(frame_count), command)
        command = re.sub( r"<(?i)FRAME_INCREMENT>", str(frame_increment), command)
        command = re.sub( r"<(?i)QUOTE>", "\"", command)
        return command
    
    def PreRenderTasks(self):
        self.SetProgress(0)
        self.LogInfo("Starting Command Job")

    def PostRenderTasks(self):
        self.SetProgress(100)
        self.LogInfo("Finished Command Job")
        
    def HandleStdoutRenderer(self):
        self.FailRender(self.GetRegexMatch(1))
    
    def HandleStdoutError(self):
        self.FailRender(self.GetRegexMatch(1))

    def HandleStdoutLicense(self):
        self.FailRender(self.GetRegexMatch(1))
        
    def HandleStdoutUnknown(self):
        self.FailRender( "Bad command line: " + self.RenderArgument() + "\nHoudini Error: " + self.GetRegexMatch(1) )
    
    def HandleStdoutFrameProgress(self):
        completedFrameProgress = float(self.completedFrames) * 100.0
        currentFrameProgress = float(self.GetRegexMatch(1))
        overallProgress = (completedFrameProgress + currentFrameProgress) / float(frameCount)
        self.SetProgress(overallProgress)
        self.SetStatusMessage( "Progress: " + str(overallProgress) + " %" )
                

        overallProgress = float(self.GetRegexMatch(1))
        self.SetProgress(overallProgress)
        self.SetStatusMessage( "Progress: " + str(overallProgress) + " %" )
        
    def HandleStdoutFrameComplete(self):
        self.frame_current = self.GetRegexMatch(1)

    def HandleProgress( self ):
        progress = float( self.GetRegexMatch(1) )
        self.SetProgress( progress )