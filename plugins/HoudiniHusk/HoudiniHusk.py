#!/usr/bin/env python3

from __future__ import absolute_import

import re

from Deadline.Plugins import DeadlinePlugin, PluginType
from Deadline.Scripting import RepositoryUtils
from six.moves import range


def GetDeadlinePlugin():
    return HoudiniHuskPlugin()
    
def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()
    
class HoudiniHuskPlugin (DeadlinePlugin):
    completedFrames = 0
    ropType = ""
    
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
        self.GetPluginInfoEntry
        houdiniVersion = self.GetPluginInfoEntry("HoudiniVersion",).replace( ".", "_" )
        return self.GetRenderExecutable( "Houdini" + houdiniVersion + "_Husk_Executable", "Houdini " + houdiniVersion)
        
    def RenderArgument(self):
        arguments = self.GetPluginInfoEntryWithDefault("Arguments", "").strip()
        # Path Mappings
        arguments = RepositoryUtils.CheckPathMapping(arguments)
        # Frame Range
        frame_start = self.GetStartFrame()
        frame_end = self.GetEndFrame()
        frame_count = max(0, frame_end - frame_start) + 1
        frame_increment = 1 # Deadline doesn't support this

        self.frame_start = frame_start
        self.frame_end = frame_end
        self.frame_increment = frame_increment
        self.frame_current = frame_start
        # Instead of adding frame args, we expect them to be part of the arguments already.
        # We do this so that pre/post scripts receive the correct frame data too.
        """
        frame_args = "--frame {frame_start}"\
                     "--frame-count {frame_count}"\
                     "--frame-inc {frame_increment}"\
                     "".format(frame_start=frame_start,
                               frame_count=frame_count,
                               frame_increment=frame_increment)
        arguments.append(frame_args)
        """
        arguments = re.sub( r"<(?i)FRAME>", str(frame_start), arguments)
        arguments = re.sub( r"<(?i)FRAME_COUNT>", str(frame_count), arguments)
        arguments = re.sub( r"<(?i)FRAME_INCREMENT>", str(frame_increment), arguments)
        arguments = re.sub( r"<(?i)QUOTE>", "\"", arguments)
        return arguments
    
    def PreRenderTasks(self):
        self.SetProgress(0)
        self.LogInfo("Starting Houdini Husk Job")

    def PostRenderTasks(self):
        self.SetProgress(100)
        self.LogInfo("Finished Houdini Husk Job")
        
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
        
    def HandleStdoutDoneRender(self):
        self.SetStatusMessage("Finished Render")
        self.SetProgress(100)

    def HandleProgress( self ):
        progress = float( self.GetRegexMatch(1) )
        self.SetProgress( progress )