from __future__ import absolute_import
import imp
import os
import re
import sys
import threading
import time
import six

from collections import Counter, OrderedDict
from six.moves import range
from typing import Any, Optional, List, Union
if six.PY3:
    from importlib import reload  # python 3 doesn't have the built-in 'reload'

from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent

from System import *
from System.Collections.Specialized import StringCollection
from System.IO import Path, StreamWriter, File, Directory
from System.Text import Encoding
from System.Text.RegularExpressions import Regex

from Deadline.Scripting import RepositoryUtils, FrameUtils, ClientUtils, PathUtils
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog
from ThinkboxUI.Controls.Scripting.ButtonControl import ButtonControl

# For Integration UI
imp.load_source( 'IntegrationUI', RepositoryUtils.GetRepositoryFilePath( "submission/Integration/Main/IntegrationUI.py", True ) )
import IntegrationUI

# For VrsceneUtils
vraySubmissionPath = RepositoryUtils.GetRepositoryPath( "submission/VRay/Main", True)
if vraySubmissionPath not in sys.path:
    sys.path.append( vraySubmissionPath )

if 'VrsceneUtils' not in sys.modules:
    import VrsceneUtils
else:
    # Reload in case the repository file was modified
    reload( VrsceneUtils )

# For TileRendering
tileRenderingSubmissionPath = RepositoryUtils.GetRepositoryPath( "submission/TileRendering/Main", True )
if tileRenderingSubmissionPath not in sys.path:
    sys.path.append( tileRenderingSubmissionPath  )

if 'TileRendering' not in sys.modules:
    import TileRendering
else:
    # Reload in case the repository file was modified
    reload( TileRendering )

########################################################################
## Globals
########################################################################
scriptDialog = None  # type: DeadlineScriptDialog
settings = None
integration_dialog = None  # type: ignore
ProjectManagementOptions = ["Shotgun","FTrack"]
DraftRequested = True
renderEngineOptions = ["V-Ray", "V-Ray RT", "V-Ray RT(OpenCL)", "V-Ray RT(CUDA)", "V-Ray RT(RTX)"]

# Due to the method order resolution, we only need to do this to implement an OrderedCounter
class OrderedCounter( Counter, OrderedDict ):
    pass

########################################################################
## Main Function Called By Deadline
########################################################################
def __main__( *args ):
    # type: (*Any) -> None
    global scriptDialog
    global settings
    global ProjectManagementOptions
    global DraftRequested
    global integration_dialog
    
    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle( "Submit V-Ray Job To Deadline" )
    scriptDialog.SetIcon( scriptDialog.GetIcon( 'Vray' ) )
    
    scriptDialog.AddTabControl("Tabs", 0, 0)
    
    scriptDialog.AddTabPage("Job Options")
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator1", "SeparatorControl", "Job Description", 0, 0, colSpan=2 )
    
    scriptDialog.AddControlToGrid( "NameLabel", "LabelControl", "Job Name", 1, 0, "The name of your job. This is optional, and if left blank, it will default to 'Untitled'.", False )
    scriptDialog.AddControlToGrid( "NameBox", "TextControl", "Untitled", 1, 1 )

    scriptDialog.AddControlToGrid( "CommentLabel", "LabelControl", "Comment", 2, 0, "A simple description of your job. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "CommentBox", "TextControl", "", 2, 1 )

    scriptDialog.AddControlToGrid( "DepartmentLabel", "LabelControl", "Department", 3, 0, "The department you belong to. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "DepartmentBox", "TextControl", "", 3, 1 )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator2", "SeparatorControl", "Job Options", 0, 0, colSpan=3 )

    scriptDialog.AddControlToGrid( "PoolLabel", "LabelControl", "Pool", 1, 0, "The pool that your job will be submitted to.", False )
    scriptDialog.AddControlToGrid( "PoolBox", "PoolComboControl", "none", 1, 1 )

    scriptDialog.AddControlToGrid( "SecondaryPoolLabel", "LabelControl", "Secondary Pool", 2, 0, "The secondary pool lets you specify a Pool to use if the primary Pool does not have any available Workers.", False )
    scriptDialog.AddControlToGrid( "SecondaryPoolBox", "SecondaryPoolComboControl", "", 2, 1 )

    scriptDialog.AddControlToGrid( "GroupLabel", "LabelControl", "Group", 3, 0, "The group that your job will be submitted to.", False )
    scriptDialog.AddControlToGrid( "GroupBox", "GroupComboControl", "none", 3, 1 )

    scriptDialog.AddControlToGrid( "PriorityLabel", "LabelControl", "Priority", 4, 0, "A job can have a numeric priority ranging from 0 to 100, where 0 is the lowest priority and 100 is the highest priority.", False )
    scriptDialog.AddRangeControlToGrid( "PriorityBox", "RangeControl", RepositoryUtils.GetMaximumPriority() // 2, 0, RepositoryUtils.GetMaximumPriority(), 0, 1, 4, 1 )

    scriptDialog.AddControlToGrid( "TaskTimeoutLabel", "LabelControl", "Task Timeout", 5, 0, "The number of minutes a Worker has to render a task for this job before it requeues it. Specify 0 for no limit.", False )
    scriptDialog.AddRangeControlToGrid( "TaskTimeoutBox", "RangeControl", 0, 0, 1000000, 0, 1, 5, 1 )
    scriptDialog.AddSelectionControlToGrid( "AutoTimeoutBox", "CheckBoxControl", False, "Enable Auto Task Timeout", 5, 2, "If the Auto Task Timeout is properly configured in the Repository Options, then enabling this will allow a task timeout to be automatically calculated based on the render times of previous frames for the job." )

    scriptDialog.AddControlToGrid( "ConcurrentTasksLabel", "LabelControl", "Concurrent Tasks", 6, 0, "The number of tasks that can render concurrently on a single Worker. This is useful if the rendering application only uses one thread to render and your Workers have multiple CPUs.", False )
    scriptDialog.AddRangeControlToGrid( "ConcurrentTasksBox", "RangeControl", 1, 1, 16, 0, 1, 6, 1 )
    scriptDialog.AddSelectionControlToGrid( "LimitConcurrentTasksBox", "CheckBoxControl", True, "Limit Tasks To Worker's Task Limit", 6, 2, "If you limit the tasks to a Worker's task limit, then by default, the Worker won't dequeue more tasks then it has CPUs. This task limit can be overridden for individual Workers by an administrator." )

    scriptDialog.AddControlToGrid( "MachineLimitLabel", "LabelControl", "Machine Limit", 7, 0, "", False )
    scriptDialog.AddRangeControlToGrid( "MachineLimitBox", "RangeControl", 0, 0, 1000000, 0, 1, 7, 1 )
    scriptDialog.AddSelectionControlToGrid( "IsBlacklistBox", "CheckBoxControl", False, "Machine List Is A Deny List", 7, 2, "" )

    scriptDialog.AddControlToGrid( "MachineListLabel", "LabelControl", "Machine List", 8, 0, "Use the Machine Limit to specify the maximum number of machines that can render your job at one time. Specify 0 for no limit.", False )
    scriptDialog.AddControlToGrid( "MachineListBox", "MachineListControl", "", 8, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "LimitGroupLabel", "LabelControl", "Limits", 9, 0, "The Limits that your job requires.", False )
    scriptDialog.AddControlToGrid( "LimitGroupBox", "LimitGroupControl", "", 9, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "DependencyLabel", "LabelControl", "Dependencies", 10, 0, "Specify existing jobs that this job will be dependent on. This job will not start until the specified dependencies finish rendering.", False )
    scriptDialog.AddControlToGrid( "DependencyBox", "DependencyControl", "", 10, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "OnJobCompleteLabel", "LabelControl", "On Job Complete", 11, 0, "If desired, you can automatically archive or delete the job when it completes.", False )
    scriptDialog.AddControlToGrid( "OnJobCompleteBox", "OnJobCompleteControl", "Nothing", 11, 1 )
    scriptDialog.AddSelectionControlToGrid( "SubmitSuspendedBox", "CheckBoxControl", False, "Submit Job As Suspended", 11, 2, "If enabled, the job will submit in the suspended state. This is useful if you don't want the job to start rendering right away. Just resume it from the Monitor when you want it to render." )
    scriptDialog.EndGrid()
    scriptDialog.EndTabPage()

    scriptDialog.AddTabPage("V-Ray Options")

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator3", "SeparatorControl", "Options", 0, 0, colSpan=4 )

    scriptDialog.AddControlToGrid( "SceneLabel", "LabelControl", "V-Ray File", 1, 0, "The V-Ray file (*.vrscene) to be rendered. If you are submitting a sequence of vrscene files (one file per frame), you only need to select one vrscene file from the sequence.", False )
    sceneBox = scriptDialog.AddSelectionControlToGrid( "SceneBox", "MultiFileBrowserControl", "", "V-Ray Files (*.vrscene);;All Files (*)", 1, 1, colSpan=3 )
    sceneBox.ValueModified.connect(SceneBoxChanged)

    scriptDialog.AddControlToGrid("OutputLabel","LabelControl","Output File (Optional)", 2, 0, "Optionally override the output file name. Required for tile rendering. Any hash (\"#\") characters will be substituted with the frame number using the format specified in the .vrscene file.", False)
    outputBox = scriptDialog.AddSelectionControlToGrid("OutputBox","FileSaverControl","","Bitmap (*.bmp);;OpenEXR (*.exr);;High Dynamic Range (*.hdr);;JPEG (*.jpg);;Portable Network Graphics (*.png);;TGA (*.tga);;V-Ray Image (*.vrimg)", 2, 1, colSpan=3)
    outputBox.ValueModified.connect(OutputBoxChanged)

    scriptDialog.AddControlToGrid( "FramesLabel", "LabelControl", "Frame List", 3, 0, "The list of frames to render.", False )
    scriptDialog.AddControlToGrid( "FramesBox", "TextControl", "", 3, 1 )
    separateFilesBox = scriptDialog.AddSelectionControlToGrid("SeparateFilesBox","CheckBoxControl",False,"Separate Input vrscene Files Per Frame", 3, 2, "Select this option if you are submitting a sequence of vrscene files (one file per frame).", colSpan=2)
    separateFilesBox.ValueModified.connect(SeparateFilesChanged)

    scriptDialog.AddControlToGrid( "ChunkSizeLabel", "LabelControl", "Frames Per Task", 4, 0, "This is the number of frames that will be rendered at a time for each job task.", False )
    scriptDialog.AddRangeControlToGrid( "ChunkSizeBox", "RangeControl", 1, 1, 1000000, 0, 1, 4, 1 )
    scriptDialog.AddControlToGrid("ThreadsLabel", "LabelControl", "Threads", 4, 2, "The number of threads to use for rendering. Specify 0 to use the optimal number of threads.", False)
    scriptDialog.AddRangeControlToGrid("ThreadsBox","RangeControl",0,0,256,0,1, 4, 3)

    scriptDialog.AddControlToGrid("CommandLineLabel","LabelControl","Command Line Args", 5, 0, "Specify additional command line arguments you would like to pass to the V-Ray renderer.", False)
    scriptDialog.AddControlToGrid("CommandLineBox","TextControl","", 5, 1, colSpan=3 )
    
    scriptDialog.AddSelectionControlToGrid("RenderableOnAWSCheck","CheckBoxControl",False,"Renderable on AWS", 6, 0, "If enabled, the *.vrscene file will be parsed to retrieve the output file path and render resolution.", False)
    
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator12", "SeparatorControl", "RT Engine Options", 0, 0, colSpan = 4 )

    scriptDialog.AddControlToGrid( "rtEngineLabel", "LabelControl", "Render Engine", 1, 0, "Select which V-Ray render engine to use.", False, colSpan = 2 )
    renderEngine = scriptDialog.AddComboControlToGrid( "rtEngineBox", "ComboControl", "V-Ray", renderEngineOptions, 1, 1 )
    renderEngine.ValueModified.connect( RenderEngineChanged )

    scriptDialog.AddControlToGrid( "rtTimeoutLabel", "LabelControl", "Frame Timeout", 1, 2, "Specify a timeout value for a frame in minutes when using the RT engine (0.0 is default - no timeout).", False, colSpan = 2 )
    scriptDialog.AddRangeControlToGrid( "rtTimeoutBox", "RangeControl", 0.0, 0.0, 999999, 2, 0.1, 1, 3 )
    
    scriptDialog.AddControlToGrid( "rtNoiseLabel", "LabelControl", "Noise Threshold", 2, 0, "Specify a noise threshold when using the RT engine (default is 0.001).", False, colSpan = 2 )
    scriptDialog.AddRangeControlToGrid( "rtNoiseBox", "RangeControl", 0.001, 0.001, 999999, 3, 0.001, 2, 1 )

    scriptDialog.AddControlToGrid( "rtSampleLabel", "LabelControl", "Sample Level", 2, 2, "Specify maximum paths per pixel when using the RT engine (default is 0 - no limit).", False, colSpan = 2 )
    scriptDialog.AddRangeControlToGrid( "rtSampleBox", "RangeControl", 0, 0, 999999, 0, 1, 2, 3 )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator11", "SeparatorControl", "V-Ray Frame Buffer", 0, 0, colSpan = 4 )

    displayWindow = scriptDialog.AddSelectionControlToGrid("DisplayVFBBox","CheckBoxControl",False,"Display VFB", 1, 0, "Enable this option to display the V-Ray Frame Buffer while rendering.")
    displayWindow.ValueModified.connect( DisplayWindowChanged )

    scriptDialog.AddSelectionControlToGrid("AutocloseVFBBox","CheckBoxControl",False,"Autoclose VFB", 1, 1, "Enable this option to autoclose the V-Ray Frame Buffer once rendering has completed.")

    scriptDialog.AddControlToGrid( "sRGBLabel", "LabelControl", "sRGB Setting", 1, 2, "Select the initial setting for the sRGB option in the V-Ray Frame Buffer", False, colSpan = 2 )
    scriptDialog.AddComboControlToGrid( "sRGBBox", "ComboControl", "On", ["On", "Off"] , 1, 3 )
    scriptDialog.EndGrid()
    
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator4", "SeparatorControl", "Vrimg2Exr Options", 0, 0, colSpan=2 )

    scriptDialog.AddSelectionControlToGrid("Vrimg2ExrBox","CheckBoxControl",False,"Convert vrimg Files To exr With Dependent Job", 1, 0, "Enable this option to submit a dependent job that converts the vrimg output files to exr files. This feature requires parsing the .vrscene file(s) which can take significant time depending on the scene and network speed (for remote .vrscene files)")
    scriptDialog.AddSelectionControlToGrid("DeleteVrimgBox","CheckBoxControl",False,"Delete Input vrimg Files After Conversion", 1, 1, "Enable this option to delete the input vrimg file after the conversion has finished.")
    scriptDialog.EndGrid()
    scriptDialog.EndTabPage()

    scriptDialog.AddTabPage("Tile Rendering")
    
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator9", "SeparatorControl", "Resolution Override", 0, 0, colSpan=4 )

    resolutionOverrideBox = scriptDialog.AddSelectionControlToGrid("ResolutionOverrideCheck","CheckBoxControl",True,"Override Resolution", 1, 0, "Enable to override image resolution.", colSpan=4)
    resolutionOverrideBox.ValueModified.connect(ResolutionOverrideChanged)

    scriptDialog.AddControlToGrid( "WidthOverrideLabel", "LabelControl", "Width", 2, 0, "Width of Image in pixels." )
    scriptDialog.AddRangeControlToGrid( "WidthOverrideBox", "RangeControl", 100, 1, 1000000, 0, 1, 2, 1 )

    scriptDialog.AddControlToGrid( "HeightOverrideLabel", "LabelControl", "Height", 2, 2, "Height of Image in pixels." )
    scriptDialog.AddRangeControlToGrid( "HeightOverrideBox", "RangeControl", 100, 1, 1000000, 0, 1, 2, 3 )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator10", "SeparatorControl", "Tile Rendering", 0, 0, colSpan=4 )

    scriptDialog.AddControlToGrid( "TileRenderWarningLabel", "LabelControl", "Tile Rendering is unavailable when rendering a .vrimg file.", 1, 0, "", colSpan=4 )

    enableTilesBox = scriptDialog.AddSelectionControlToGrid("EnableTilesCheck","CheckBoxControl",False,"Enable Tile Rendering", 2, 0, "Enable to tile render the output. This feature requires parsing the .vrscene file(s) which can take significant time depending on the scene and network speed (for remote .vrscene files)", False, colSpan=2)
    enableTilesBox.ValueModified.connect(TilesChanged)
    
    scriptDialog.AddControlToGrid( "XTilesLabel", "LabelControl", "Tiles in X", 3, 0, "The number of tiles in the X direction.", False )
    scriptDialog.AddRangeControlToGrid( "XTilesBox", "RangeControl", 2, 1, 100, 0, 1, 3, 1 )
    scriptDialog.AddControlToGrid( "YTilesLabel", "LabelControl", "Tiles in Y", 3, 2, "The number of tiles in the Y direction.", False )
    scriptDialog.AddRangeControlToGrid( "YTilesBox", "RangeControl", 2, 1, 100, 0, 1, 3, 3 )
    
    singleFrameEnabledBox = scriptDialog.AddSelectionControlToGrid("SingleFrameEnabledCheck","CheckBoxControl",False,"Single Frame Tile Job Enabled", 4, 0, "Enable to submit all tiles in a single job.", False,1,2)
    singleFrameEnabledBox.ValueModified.connect(SingleFrameChanged)
    scriptDialog.AddControlToGrid( "SingleJobFrameLabel", "LabelControl", "Single Job Frame", 4, 2, "Which Frame to Render if Single Frame is enabled.", False )
    scriptDialog.AddRangeControlToGrid( "SingleJobFrameBox", "RangeControl", 1, 0, 100000, 0, 1, 4, 3 )
    
    SubmitDependentBox = scriptDialog.AddSelectionControlToGrid( "SubmitDependentCheck", "CheckBoxControl", True, "Submit Dependent Assembly Job", 5, 0, "If enabled, a dependent assembly job will be submitted.", False, 1, 2 )
    SubmitDependentBox.ValueModified.connect(SubmitDependentChanged)
    scriptDialog.AddSelectionControlToGrid( "CleanupTilesCheck", "CheckBoxControl", True, "Cleanup Tiles After Assembly", 5, 2, "If enabled, all tiles will be cleaned up by the assembly job.", False, 1, 2 )
    
    scriptDialog.AddSelectionControlToGrid( "ErrorOnMissingCheck", "CheckBoxControl", True, "Error on Missing Tiles", 6, 0, "If enabled, the assembly job will fail if any tiles are missing.", False, 1, 2 )
    scriptDialog.AddSelectionControlToGrid( "ErrorOnMissingBackgroundCheck", "CheckBoxControl", False, "Error on Missing Background", 6, 2, "If enabled, the assembly will fail if the background is missing.", False, 1, 2 )
    
    scriptDialog.AddControlToGrid("AssembleOverLabel","LabelControl","Assemble Over", 7, 0, "What the tiles should be assembled over.", False)
    assembleBox = scriptDialog.AddComboControlToGrid("AssembleOverBox","ComboControl","Blank Image",("Blank Image","Previous Output","Selected Image"), 7, 1)
    assembleBox.ValueModified.connect(AssembleOverChanged)
    
    scriptDialog.AddControlToGrid("BackgroundLabel","LabelControl","Background Image File", 8, 0, "The Background image to assemble over.", False)
    scriptDialog.AddSelectionControlToGrid("BackgroundBox","FileSaverControl","", "Bitmap (*.bmp);;JPG (*.jpg);;PNG (*.png);;Targa (*.tga);;TIFF (*.tif);;All Files (*)", 8, 1, colSpan=3)
        
    scriptDialog.EndGrid()
    scriptDialog.EndTabPage()
    
    integration_dialog = IntegrationUI.IntegrationDialog()
    integration_dialog.AddIntegrationTabs( scriptDialog, "VrayMonitor", DraftRequested, ProjectManagementOptions, failOnNoTabs=False )
    
    scriptDialog.EndTabControl()
    
    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "HSpacer1", 0, 0 )
    submitButton = scriptDialog.AddControlToGrid( "SubmitButton", "ButtonControl", "Submit", 0, 1, expand=False )
    submitButton.ValueModified.connect(SubmitButtonPressed)
    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 2, expand=False )
    # Make sure all the project management connections are closed properly
    closeButton.ValueModified.connect(integration_dialog.CloseProjectManagementConnections)
    closeButton.ValueModified.connect(scriptDialog.closeEvent)
    scriptDialog.EndGrid()
    
    #Application Box must be listed before version box or else the application changed event will change the version
    settings = ( "DepartmentBox","CategoryBox","PoolBox","SecondaryPoolBox","GroupBox","PriorityBox","MachineLimitBox","IsBlacklistBox","MachineListBox","LimitGroupBox","SceneBox","FramesBox","ChunkSizeBox","ThreadsBox","WidthBox","HeightBox","OutputBox","DisplayWindowBox","AutocloseBox","displaySRGBBox","rtEngineBox","rtTimeoutBox","rtNoiseBox","rtSampleBox", "ResolutionOverrideCheck", "WidthOverrideBox", "HeightOverrideBox", "RenderableOnAWSCheck" )
    scriptDialog.LoadSettings( GetSettingsFilename(), settings )
    scriptDialog.EnabledStickySaving( settings, GetSettingsFilename() )
    
    OutputBoxChanged( None )
    SceneBoxChanged( None )
    SeparateFilesChanged( None )
    RenderEngineChanged( None )
    DisplayWindowChanged( None )
    ResolutionOverrideChanged( None )
    
    scriptDialog.ShowDialog( False )

def SceneBoxChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    
    sceneFiles = scriptDialog.GetValue( "SceneBox" )
    sceneFiles = sceneFiles.split( ";" )

    if len( sceneFiles ) > 1:
        scriptDialog.SetEnabled( "EnableTilesCheck", False )
        scriptDialog.SetEnabled( "OutputBox", False )
        scriptDialog.SetEnabled( "SeparateFilesBox", False )

        scriptDialog.SetValue( "OutputBox", "" )
        scriptDialog.SetValue( "EnableTilesCheck", False )
        scriptDialog.SetValue( "SeparateFilesBox",False )
    else:
        scriptDialog.SetEnabled( "EnableTilesCheck", True )
        scriptDialog.SetEnabled( "OutputBox", True )
        scriptDialog.SetEnabled( "SeparateFilesBox", True )

        results = ParseVRayFileName( sceneFiles[0] )

        if( results is not None ):
            scriptDialog.SetValue( "FramesBox", results[0] )
            scriptDialog.SetValue( "SeparateFilesBox", not results[1] )
        else:
            scriptDialog.SetValue( "FramesBox", "" )
            scriptDialog.SetValue( "SeparateFilesBox", False )

def SeparateFilesChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    
    scriptDialog.SetEnabled( "ChunkSizeBox",not scriptDialog.GetValue( "SeparateFilesBox" ) )

def OutputBoxChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    
    enabled = False
    
    outputFile = scriptDialog.GetValue( "OutputBox" ).strip()
    if outputFile != "":
        extension = Path.GetExtension( outputFile ).lower()
        enabled = (extension == ".vrimg")

    
    scriptDialog.SetEnabled( "Vrimg2ExrBox", enabled )
    scriptDialog.SetEnabled( "DeleteVrimgBox", enabled )
    ResolutionOverrideChanged()

def RenderEngineChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog

    renderEngine = scriptDialog.GetValue( "rtEngineBox" )

    scriptDialog.SetEnabled( "rtTimeoutBox", not( renderEngine == "V-Ray" ) )
    scriptDialog.SetEnabled( "rtTimeoutLabel", not( renderEngine == "V-Ray" ) )
    scriptDialog.SetEnabled( "rtNoiseBox", not( renderEngine == "V-Ray" ) )
    scriptDialog.SetEnabled( "rtNoiseLabel", not( renderEngine == "V-Ray" ) )
    scriptDialog.SetEnabled( "rtSampleBox", not( renderEngine == "V-Ray" ) )
    scriptDialog.SetEnabled( "rtSampleLabel", not( renderEngine == "V-Ray" ) )

def DisplayWindowChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog

    displayWindow = scriptDialog.GetValue( "DisplayVFBBox" )

    scriptDialog.SetEnabled( "AutocloseVFBBox", displayWindow )
    scriptDialog.SetEnabled( "sRGBBox", displayWindow )
    scriptDialog.SetEnabled( "sRGBLabel", displayWindow )

def ResolutionOverrideChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog

    enabled = scriptDialog.GetEnabled( "ResolutionOverrideCheck" ) and scriptDialog.GetValue( "ResolutionOverrideCheck" ) 

    scriptDialog.SetEnabled( "WidthOverrideBox", enabled )
    scriptDialog.SetEnabled( "HeightOverrideBox", enabled )
    scriptDialog.SetEnabled( "WidthOverrideLabel", enabled )
    scriptDialog.SetEnabled( "HeightOverrideLabel", enabled )

    #jigsaw can't assemble vrimg files
    scriptDialog.SetEnabled( "EnableTilesCheck", not scriptDialog.GetEnabled("Vrimg2ExrBox") )

    TilesChanged()

def TilesChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    enableRegionRendering = ( scriptDialog.GetValue( "EnableTilesCheck" ) and scriptDialog.GetEnabled( "EnableTilesCheck" ) )

    scriptDialog.nameControlPairs[ "TileRenderWarningLabel" ].setVisible( not scriptDialog.GetEnabled( "EnableTilesCheck" ) )

    scriptDialog.SetEnabled( "XTilesLabel", enableRegionRendering )
    scriptDialog.SetEnabled( "XTilesBox", enableRegionRendering )
    scriptDialog.SetEnabled( "YTilesLabel", enableRegionRendering )
    scriptDialog.SetEnabled( "YTilesBox", enableRegionRendering )
    scriptDialog.SetEnabled( "SingleFrameEnabledCheck", enableRegionRendering )
    scriptDialog.SetEnabled( "SubmitDependentCheck", enableRegionRendering )
    
    SingleFrameChanged()
    SubmitDependentChanged()

def SubmitDependentChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    submitDependentEnabled = ( scriptDialog.GetValue( "SubmitDependentCheck" ) and scriptDialog.GetEnabled( "SubmitDependentCheck" ) )
    
    scriptDialog.SetEnabled( "CleanupTilesCheck", submitDependentEnabled )
    scriptDialog.SetEnabled( "ErrorOnMissingCheck", submitDependentEnabled )
    scriptDialog.SetEnabled( "ErrorOnMissingBackgroundCheck", submitDependentEnabled )
    scriptDialog.SetEnabled( "AssembleOverLabel", submitDependentEnabled )
    scriptDialog.SetEnabled( "AssembleOverBox", submitDependentEnabled )
    
    AssembleOverChanged()
    
def AssembleOverChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    AssembleOverEnabled = ( (scriptDialog.GetValue( "AssembleOverBox" ) == "Selected Image") and scriptDialog.GetEnabled( "AssembleOverBox" ) )
    
    scriptDialog.SetEnabled( "BackgroundLabel", AssembleOverEnabled )
    scriptDialog.SetEnabled( "BackgroundBox", AssembleOverEnabled )
    
def SingleFrameChanged( *args ):
    # type: (*Any) -> None
    global scriptDialog
    enableSingleFrameRegion = ( scriptDialog.GetValue( "SingleFrameEnabledCheck" ) and scriptDialog.GetEnabled( "SingleFrameEnabledCheck" ) )
    
    scriptDialog.SetEnabled( "SingleJobFrameLabel", enableSingleFrameRegion )
    scriptDialog.SetEnabled( "SingleJobFrameBox", enableSingleFrameRegion )

def ParseVRayFileName( filename ):
    # type: (str) -> Optional[List[Union[bool, str]]]
    results=[""]*2  # type: List[Union[bool, str]]
    frameString = "1"
    multiFrame=True
    
    try:
        startFrame=0
        endFrame=0
        initFrame=FrameUtils.GetFrameNumberFromFilename(filename)
        paddingSize=FrameUtils.GetPaddingSizeFromFilename(filename)
    
        try:
            startFrame=FrameUtils.GetLowerFrameRange(filename,initFrame,paddingSize)
            endFrame=FrameUtils.GetUpperFrameRange(filename,initFrame,paddingSize)
            
            if(startFrame == endFrame):
                frameString = str(startFrame)
            else:
                frameString = str(startFrame) + "-" + str(endFrame)
            
            multiFrame=False
        except:
            multiFrame=True
            
        results[0]=frameString
        results[1]=multiFrame
        return results
    except:
        return None
    
def GetSettingsFilename():
    # type: () -> str
    return Path.Combine( ClientUtils.GetUsersSettingsDirectory(), "VraySettings.ini" )

def RightReplace( fullString, oldString, newString, occurences ):
    return newString.join( fullString.rsplit( oldString, occurences ) )

def WriteIntegrationSettings( writer, groupBatch ):
    # type: (StreamWriter, bool) -> bool
    # Integration
    extraKVPIndex = 0

    if integration_dialog is not None and integration_dialog.IntegrationProcessingRequested():
        extraKVPIndex = integration_dialog.WriteIntegrationInfo( writer, extraKVPIndex )
        groupBatch = groupBatch or integration_dialog.IntegrationGroupBatchRequested()

    tileRendering = scriptDialog.GetValue( "EnableTilesCheck" )
    dependentAssembly = scriptDialog.GetValue( "SubmitDependentCheck" )
    singleFrameJob = scriptDialog.GetValue( "SingleFrameEnabledCheck" )

    if tileRendering and dependentAssembly and singleFrameJob:
        tileFrame = scriptDialog.GetValue( "SingleJobFrameBox" )
        writer.WriteLine( "ExtraInfoKeyValue%d=FrameRangeOverride=%d\n" % ( extraKVPIndex, tileFrame ) )

    return groupBatch

def SubmitButtonPressed( *args ):
    # type: (*ButtonControl) -> None
    global scriptDialog
    global integration_dialog

    warnings = ""
    errors = ""

    paddedNumberRegex = Regex( "\\$F([0-9]+)" )
    
    # Check if Vray file exist.
    sceneFiles = scriptDialog.GetValue( "SceneBox" )
    sceneFiles = sceneFiles.split( ";" )

    for sceneFile in sceneFiles:
        if( not File.Exists( sceneFile ) ):
            errors += "The V-Ray file %s does not exist.\n\n" % sceneFile
        elif (PathUtils.IsPathLocal(sceneFile)):
            warnings += "The V-Ray file %s is local.\n\n" % sceneFile
    
    regionRendering = scriptDialog.GetEnabled( "EnableTilesCheck" ) and scriptDialog.GetValue( "EnableTilesCheck" )
    singleRegionJob = regionRendering and scriptDialog.GetEnabled( "SingleFrameEnabledCheck" ) and scriptDialog.GetValue( "SingleFrameEnabledCheck" )
    overrideResolution = scriptDialog.GetEnabled("ResolutionOverrideCheck") and scriptDialog.GetValue( "ResolutionOverrideCheck" )
    overrideWidth = -1
    overrideHeight = -1
    regionJobCount = 1
    tilesInX = 1
    tilesInY = 1
    paddedOutputFile = ""
    outputFile = ""
    groupBatch = False
    renderEngine = scriptDialog.GetValue( "rtEngineBox" )
    vrimg2exr = scriptDialog.GetEnabled( "Vrimg2ExrBox" ) and scriptDialog.GetValue( "Vrimg2ExrBox" )
    parsingSceneFile = regionRendering or scriptDialog.GetValue( "RenderableOnAWSCheck") or vrimg2exr
    parsedFramePadding = False
    frameList = []
    sequentialFramePlaceholders = False
    framePlaceholderInDirectory = False
    outputOverride = scriptDialog.GetValue( "OutputBox" ).strip()
    separateFiles = scriptDialog.GetValue( "SeparateFilesBox" )
    dlTileGenerator = None  # type: TileRendering.TileGenerator

    # Check if a valid frame range has been specified.
    frames = scriptDialog.GetValue( "FramesBox" )
    if( not FrameUtils.FrameRangeValid( frames ) ):
        errors += "Frame range %s is not valid.\n\n" % frames
    elif singleRegionJob:
        frameList = [scriptDialog.GetValue( "SingleJobFrameBox" )]
    else:
        frameList = FrameUtils.Parse( frames )
    
    
    pulledOutputFiles = []

    if separateFiles:
        for sceneFile in sceneFiles:
            if not re.search( r'\d+\.[^.]+$', sceneFile ):
                errors += 'Separate input vrscene files per frame is checked, but the vrscene file %s does not contain a frame number.\n\n' % sceneFile
        
    # Generate the output filename for the submit info file
    outputFile = outputOverride
    if outputOverride:
        # Sanity checks on output override

        outputDir = os.path.dirname(outputFile)
        if(not os.path.isdir(outputDir)):
            errors += "The directory of the output file does not exist:\n%s\n\n" % Path.GetDirectoryName(outputFile)
        elif (PathUtils.IsPathLocal(outputFile)):
            warnings += "The output file %s is local.\n\n" % outputFile

        framePlaceholderInDirectory = '#' in outputDir
        if framePlaceholderInDirectory:
            warnings += 'You are embedding the frame number in the directory. Deadline does not support viewing job output in the monitor for such jobs.\n\n'

        if len(re.findall('#', outputFile)) > 1:
            warnings += 'The output path %s contains multiple hash ("#") characters. VRay will substitute each one with the frame number.\n\n' % outputFile

        if re.search( r'#{2,}', outputFile ):
            _errorMsg = 'The output path %s contains consecutive hash ("#") characters. '
            sequentialFramePlaceholders = True
            if regionRendering:
                _errorMsg += 'This is incompatible with tile rendering\n\n'
                errors += _errorMsg
            else:
                _errorMsg += 'This is likely not what you want and will disable the ability to view job output in the Monitor\n\n'
                warnings += _errorMsg
        if paddedNumberRegex.IsMatch( outputFile ):
            warnings += 'The output path %s contains a $F[0-9] macro, which is not supported for VRay.\n\n' % outputFile
    paddedOutputFile = outputFile.replace( "$F", "#" )
    
    if overrideResolution:
        overrideWidth = scriptDialog.GetValue( "WidthOverrideBox" )
        overrideHeight = scriptDialog.GetValue( "HeightOverrideBox" )
    
    if regionRendering:
        tilesInX = scriptDialog.GetValue( "XTilesBox" )
        tilesInY = scriptDialog.GetValue( "YTilesBox" )
        
        if singleRegionJob:
            regionJobCount = 1
            taskLimit = RepositoryUtils.GetJobTaskLimit()
            if tilesInX * tilesInY > taskLimit:
                errors += "Unable to submit job with %s tasks. Task Count exceeded Job Task Limit of %s.\n\n" % ( ( str( tilesInX * tilesInY ) ), str( taskLimit ) )
        else:
            regionJobCount = tilesInX * tilesInY
        
        try:
            outputExt = Path.GetExtension(outputFile)
        except:
            errors += "No extension was found in output file name.\n\n"
    
    # Check if Integration options are valid.
    if integration_dialog is not None and not integration_dialog.CheckIntegrationSanity( outputFile ):
        return

    if len( errors ) > 0:
        errors = "The following errors were encountered:\n\n%s\n\nPlease resolve these issues and submit again.\n" % errors
        scriptDialog.ShowMessageBox( errors, "Error" )
        return

    if len( warnings ) > 0:
        warnings = "Warnings:\n\n%s\nAre you sure you want to continue?\n" % warnings
        result = scriptDialog.ShowMessageBox( warnings, "Warning", ( "Yes", "No" ) )
        if result == "No":
            return
    
    if parsingSceneFile:
        vrScriptDialog = deadlineParsingProgressDialog( sceneFiles[0], paddedOutputFile or outputFile )
        vrScriptDialog.ShowDialog( True )

        results = VrsceneUtils.GetOutputValue()
        pulledOutputFiles = results[0]
        outputFile = results[1]
        overrideResolution = True
        overrideWidth = overrideWidth if overrideWidth > 0 else results[ 2 ]
        overrideHeight = overrideHeight if overrideHeight > 0 else results[ 3 ]
        parsedFramePadding = results[ 4 ]
        needFrameNumber = results[ 5 ]

        if pulledOutputFiles is None:
            scriptDialog.ShowMessageBox( "File parsing was cancelled before it could be completed.", "Error" )
            return
        elif len(pulledOutputFiles) == 0:
            scriptDialog.ShowMessageBox( "The vrscene file does not contain any output file name data and no overrides were set.\n\nPlease resolve these issues and submit again.\n", "Error" )
            return
        elif overrideWidth < 0 or overrideHeight <0:
            scriptDialog.ShowMessageBox( "The vrscene file does not contain any output file resolution data and no resolution overrides were set.\n\nPlease resolve these issues and submit again.\n", "Error" )
            return
        elif parsedFramePadding == 0 and len(frameList) > 1:
            scriptDialog.ShowMessageBox( "The vrscene file has a frame padding of 0. Your submission specifies multiple frames. All frame outputs will write to the same file.\n", "Error" )
            return
        elif not outputOverride:
            # Sanity checks when user didn't override but parsed the scene
            outputDir = os.path.dirname(outputFile)
            framePlaceholderInDirectory = '#' in outputDir
            warnings_list = []

            if framePlaceholderInDirectory:
                warnings_list.append('The output directory %s contains a frame number placeholder ("#"). Deadline does not support viewing job output in the monitor for such jobs.\n\n' % outputDir)

            if len(re.findall('#', outputFile)) > 1:
                warnings_list.append('The output path %s contains multiple hash ("#") characters. VRay will substitute each one with the frame number.\n\n' % outputFile)

            if re.search( r'#{2,}', outputFile ):
                _errorMsg = 'The output path %s contains consecutive hash ("#") characters. ' % outputFile
                sequentialFramePlaceholders = True
                if regionRendering:
                    _errorMsg += 'This is incompatible with tile rendering\n\n'
                    scriptDialog.ShowMessageBox( _errorMsg, "Error" )
                    return
                else:
                    _errorMsg += 'This is likely not what you want and will disable the ability to view job output in the Monitor\n\n'
                    warnings_list.append(_errorMsg)

            if warnings_list:
                warningMsg = 'Warnings:\n\n%s\nAre you sure you want to continue?\n' % '\n\n'.join(warnings)
                result = scriptDialog.ShowMessageBox( warningMsg, "Continue Submission", ( "Yes", "No" ) )
                if result == "No":
                    return
        else:
            # Find duplicates. collections.Counter isn't the fastest, but it's O(n) and our lists are generally small so it's negligible.
            countedOutputFiles = OrderedCounter( pulledOutputFiles ) # Order matters for this
            pulledOutputFiles = list(countedOutputFiles.keys()) # No duplicates
            duplicates = [ path for path, count in countedOutputFiles.items() if count > 1 ]

            warnDuplicates = ""
            if duplicates:
                warnDuplicates = "The following output paths have duplicates:\n\n%s\n\n" % "\n".join( duplicates )

            result = scriptDialog.ShowMessageBox( "%sThe following output file paths were found within the scene:\n\n%s\n\nWould you like to continue to submit the job?" % ( warnDuplicates, "\n".join(pulledOutputFiles) ), "Continue Submission", ( "Yes", "No" ) )
            if result == "No":
                return

    if regionRendering:
        dlTileGenerator = TileRendering.TileGenerator( tilesInX, tilesInY, overrideWidth, overrideHeight )

    jobIds = []
    jobCount = 0
    jobResult = ""
    jobName = scriptDialog.GetValue( "NameBox" )

    for sceneFile in sceneFiles:
        for jobNum in range(regionJobCount):
            modifiedName = jobName

            if len( sceneFiles ) > 1:
                fileName = os.path.basename( sceneFile )
                fileName = os.path.splitext( fileName )[0]
                modifiedName = fileName
                groupBatch = True

            if regionRendering and not singleRegionJob:
                modifiedName = modifiedName + " - Region " + str(jobNum)
            
            batchName = jobName

            # Create job info file.
            jobInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "vray_job_info.job" )
            writer = StreamWriter( jobInfoFilename, False, Encoding.Unicode )
            writer.WriteLine( "Plugin=Vray" )
            writer.WriteLine( "Name=%s" % modifiedName )
            writer.WriteLine( "Comment=%s" % scriptDialog.GetValue( "CommentBox" ) )
            writer.WriteLine( "Department=%s" % scriptDialog.GetValue( "DepartmentBox" ) )
            writer.WriteLine( "Pool=%s" % scriptDialog.GetValue( "PoolBox" ) )
            writer.WriteLine( "SecondaryPool=%s" % scriptDialog.GetValue( "SecondaryPoolBox" ) )
            writer.WriteLine( "Group=%s" % scriptDialog.GetValue( "GroupBox" ) )
            writer.WriteLine( "Priority=%s" % scriptDialog.GetValue( "PriorityBox" ) )
            writer.WriteLine( "TaskTimeoutMinutes=%s" % scriptDialog.GetValue( "TaskTimeoutBox" ) )
            writer.WriteLine( "EnableAutoTimeout=%s" % scriptDialog.GetValue( "AutoTimeoutBox" ) )
            writer.WriteLine( "ConcurrentTasks=%s" % scriptDialog.GetValue( "ConcurrentTasksBox" ) )
            writer.WriteLine( "LimitConcurrentTasksToNumberOfCpus=%s" % scriptDialog.GetValue( "LimitConcurrentTasksBox" ) )

            writer.WriteLine( "MachineLimit=%s" % scriptDialog.GetValue( "MachineLimitBox" ) )
            if( bool(scriptDialog.GetValue( "IsBlacklistBox" )) ):
                writer.WriteLine( "Blacklist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
            else:
                writer.WriteLine( "Whitelist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
            
            writer.WriteLine( "LimitGroups=%s" % scriptDialog.GetValue( "LimitGroupBox" ) )
            writer.WriteLine( "JobDependencies=%s" % scriptDialog.GetValue( "DependencyBox" ) )
            writer.WriteLine( "OnJobComplete=%s" % scriptDialog.GetValue( "OnJobCompleteBox" ) )
            
            if( bool(scriptDialog.GetValue( "SubmitSuspendedBox" )) ):
                writer.WriteLine( "InitialStatus=Suspended" )
            
            if singleRegionJob:
                writer.WriteLine( "TileJob=True" )
                writer.WriteLine( "TileJobTilesInX=%s" % tilesInX )
                writer.WriteLine( "TileJobTilesInY=%s" % tilesInY )
                writer.WriteLine( "TileJobFrame=%s" % scriptDialog.GetValue( "SingleJobFrameBox" ) )
            else:
                writer.WriteLine( "Frames=%s" % frames )
            
            if( separateFiles ):
                writer.WriteLine( "ChunkSize=1" )
            else:
                writer.WriteLine( "ChunkSize=%s" % scriptDialog.GetValue( "ChunkSizeBox" ) )
            
            tempOutputFiles = [ outputFile ]
            if len(pulledOutputFiles) > 0:
                tempOutputFiles = pulledOutputFiles
            elif paddedOutputFile:
                tempOutputFiles = [ paddedOutputFile ]
            
            if regionRendering:
                for index, tempOutputFile in enumerate(tempOutputFiles):
                    tileName = tempOutputFile.replace( '#', '#' * parsedFramePadding )
                    splitFilename = os.path.split(tileName)
                    tileName = os.path.join(splitFilename[0], "_tile?_"+splitFilename[1])
                    if singleRegionJob:
                        for currTile in range(tilesInX*tilesInY):
                            regionOutputFileName = tileName.replace( "?", str(currTile) )
                            writer.WriteLine( "OutputFilename%sTile%s=%s" % ( index, currTile, regionOutputFileName ) )
                    else:
                        regionOutputFileName = tileName.replace( "?", str(jobNum) )
                        writer.WriteLine( "OutputFilename%s=%s" % ( index, regionOutputFileName ) )
            # We can only reliably determine the output path under certain conditions
            elif parsingSceneFile and not sequentialFramePlaceholders and not framePlaceholderInDirectory:
                for index, tempOutputFile in enumerate(tempOutputFiles):
                    if '#' in tempOutputFile:
                        tempOutputFile = tempOutputFile.replace( '#', '#' * parsedFramePadding )
                    elif needFrameNumber:
                        tempOutputPrefix, tempOuputExt = os.path.splitext( tempOutputFile )
                        tempOutputFile = tempOutputPrefix + '.' + ('#' * parsedFramePadding) + tempOuputExt
                    writer.WriteLine( "OutputFilename%s=%s" % ( index, tempOutputFile ) )
            
            if vrimg2exr:
                groupBatch = True

            if regionRendering:
                groupBatch = True
            
            dependentAssembly = scriptDialog.GetValue( "SubmitDependentCheck" )

            if not ( regionRendering and dependentAssembly ):
                groupBatch = WriteIntegrationSettings( writer, groupBatch )

            if groupBatch:
                writer.WriteLine( "BatchName=%s\n" % ( batchName ) ) 
            writer.Close()
            
            # Create plugin info file.
            pluginInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "vray_plugin_info.job" )
            writer = StreamWriter( pluginInfoFilename, False, Encoding.Unicode )
            
            writer.WriteLine( "InputFilename=%s" % sceneFile )
            writer.WriteLine( "Threads=%s" % scriptDialog.GetValue( "ThreadsBox" ) )
            writer.WriteLine( "OutputFilename=%s" % outputFile )
            writer.WriteLine( "SeparateFilesPerFrame=%s" % separateFiles )
            writer.WriteLine( "CommandLineOptions=%s" % scriptDialog.GetValue( "CommandLineBox" ) )

            writer.WriteLine( "VRayEngine=%s" % renderEngine )
            writer.WriteLine( "RTTimeout=%s" % scriptDialog.GetValue( "rtTimeoutBox" ) )
            writer.WriteLine( "RTNoise=%s" % scriptDialog.GetValue( "rtNoiseBox" ) )
            writer.WriteLine( "RTSamples=%s" % scriptDialog.GetValue( "rtSampleBox" ) )

            writer.WriteLine( "DisplayVFB=%s" % scriptDialog.GetValue( "DisplayVFBBox" ) )
            writer.WriteLine( "AutocloseVFB=%s" % scriptDialog.GetValue( "AutocloseVFBBox" ) )
            writer.WriteLine( "DisplaySRGB=%s" % scriptDialog.GetValue( "sRGBBox" ) )

            if overrideResolution:
                writer.WriteLine( "OverrideResolution=True" )
                writer.WriteLine( "Width=%s" % overrideWidth )
                writer.WriteLine( "Height=%s" % overrideHeight )

            if regionRendering:
                writer.WriteLine( "RegionRendering=True" )
                writer.WriteLine( "CoordinatesInPixels=True" )
                
                if singleRegionJob:
                    #Vray uses an inverted Y axis when compared to Draft
                    for curRegion, (xStart,xEnd,yStart,yEnd) in enumerate( dlTileGenerator.getEachTile( origin='top-left' ) ):
                        writer.WriteLine( "RegionXStart%s=%s" % ( curRegion, xStart ) )
                        writer.WriteLine( "RegionXEnd%s=%s" % ( curRegion, xEnd ) )
                        writer.WriteLine( "RegionYStart%s=%s" % ( curRegion, yStart ) )
                        writer.WriteLine( "RegionYEnd%s=%s" % ( curRegion,yEnd ) )
                else:
                    writer.WriteLine( "CurrentTile=%s" % jobNum )
                    # Vray uses an inverted Y axis when compared to Draft
                    xStart, xEnd, yStart, yEnd = dlTileGenerator.getTile( jobNum, origin='top-left' )
                
                    writer.WriteLine( "RegionXStart=%s" % xStart )
                    writer.WriteLine( "RegionXEnd=%s" % xEnd )
                    writer.WriteLine( "RegionYStart=%s" % yStart )
                    writer.WriteLine( "RegionYEnd=%s" % yEnd )

            writer.Close()
            
            # Setup the command line arguments.
            arguments = StringCollection()
            #arguments.Add( "-notify" )
            arguments.Add( jobInfoFilename )
            arguments.Add( pluginInfoFilename )

            jobResult = results = ClientUtils.ExecuteCommandAndGetOutput( arguments )
            jobId = ""
            resultArray = jobResult.split("\n")
            for line in resultArray:
                if line.startswith( "JobID=" ):
                    jobId = line.replace( "JobID=", "" )
                    jobId = jobId.strip()
                    break
            
            jobIds.append(jobId)
            jobCount += 1
        
        if regionRendering and scriptDialog.GetValue( "SubmitDependentCheck" ):
            outputFiles = [ paddedOutputFile ]
            if len(pulledOutputFiles) > 0:
                outputFiles = pulledOutputFiles
            
            numRegionJobs = 1
            if not singleRegionJob:
                # Create one assembly job for each detected vrscene output
                # Each job will create one task per frame which assembles all regions for that frame/output combination
                numRegionJobs = len( outputFiles )
            
            for regionJobNum in range(numRegionJobs):
                jobName = scriptDialog.GetValue( "NameBox" )
                jobName = "%s - Assembly" % ( jobName )
                
                # Create submission info file
                jigsawJobInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "jigsaw_submit_info.job" )
                jigsawPluginInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "jigsaw_plugin_info.job" )        
                
                writer = StreamWriter( jigsawJobInfoFilename, False, Encoding.Unicode )
                writer.WriteLine( "Plugin=DraftTileAssembler" )
                writer.WriteLine( "Name=%s" % jobName )
                writer.WriteLine( "Comment=%s" % scriptDialog.GetValue( "CommentBox" ) )
                writer.WriteLine( "Department=%s" % scriptDialog.GetValue( "DepartmentBox" ) )
                writer.WriteLine( "Pool=%s" % scriptDialog.GetValue( "PoolBox" ) )
                writer.WriteLine( "SecondaryPool=%s" % scriptDialog.GetValue( "SecondaryPoolBox" ) )
                writer.WriteLine( "Group=%s" % scriptDialog.GetValue( "GroupBox" ) )
                writer.WriteLine( "Priority=%s" % scriptDialog.GetValue( "PriorityBox" ) )
                writer.WriteLine( "TaskTimeoutMinutes=%s" % scriptDialog.GetValue( "TaskTimeoutBox" ) )
                writer.WriteLine( "EnableAutoTimeout=%s" % scriptDialog.GetValue( "AutoTimeoutBox" ) )
                writer.WriteLine( "ConcurrentTasks=%s" % scriptDialog.GetValue( "ConcurrentTasksBox" ) )
                writer.WriteLine( "LimitConcurrentTasksToNumberOfCpus=%s" % scriptDialog.GetValue( "LimitConcurrentTasksBox" ) )
                writer.WriteLine( "MachineLimit=%s" % scriptDialog.GetValue( "MachineLimitBox" ) )
                
                if( bool(scriptDialog.GetValue( "IsBlacklistBox" )) ):
                    writer.WriteLine( "Blacklist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
                else:
                    writer.WriteLine( "Whitelist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
                    
                writer.WriteLine( "JobDependencies=%s" % ",".join(jobIds) )
                
                if( bool(scriptDialog.GetValue( "SubmitSuspendedBox" )) ):
                    writer.WriteLine( "InitialStatus=Suspended" )
                
                if singleRegionJob:
                    writer.WriteLine( "Frames=1-%s" % len( pulledOutputFiles ) )
                else:
                    writer.WriteLine( "Frames=%s" % frames )

                writer.WriteLine( "ChunkSize=1" )
                
                for index, assemblyOutputFile in enumerate(outputFiles):
                    if '#' in assemblyOutputFile:
                        assemblyOutputFile = assemblyOutputFile.replace( '#', '#' * parsedFramePadding )
                    elif needFrameNumber:
                        splitExt = os.path.splitext( assemblyOutputFile )
                        assemblyOutputFile = splitExt[0] + '.' + '#' * parsedFramePadding + splitExt[1]
                    writer.WriteLine( "OutputFilename%s=%s" % ( index, assemblyOutputFile ) )
                
                writer.WriteLine( "BatchName=%s" % ( batchName ) )

                WriteIntegrationSettings( writer, True ) 

                writer.Close()
                
                # Create plugin info file
                writer = StreamWriter( jigsawPluginInfoFilename, False, Encoding.Unicode )
                
                writer.WriteLine( "ErrorOnMissing=%s" % (scriptDialog.GetValue( "ErrorOnMissingCheck" )) )
                writer.WriteLine( "ErrorOnMissingBackground=%s" % (scriptDialog.GetValue( "ErrorOnMissingBackgroundCheck" )) )
                writer.WriteLine( "CleanupTiles=%s" % (scriptDialog.GetValue( "CleanupTilesCheck" )) )
                writer.WriteLine( "MultipleConfigFiles=True" )
                
                writer.Close()
                
                configFiles = []
                
                outputList = []
                if singleRegionJob:
                    outputList = outputFiles
                else:
                    outputList = [ outputFiles[ regionJobNum ] ]
                
                for frame in frameList:
                    if parsedFramePadding > 0:
                        paddedFrameNumber = str(frame).zfill(parsedFramePadding)
                    else:
                        # Vray effectively deletes hash characters when the frame padding is zero
                        paddedFrameNumber = ""
                    
                    for output in outputList:
                        imageFileName = output.replace("\\","/")
                        
                        tileName = imageFileName
                        outputName = imageFileName
                        paddingRegex = re.compile( "(#+)", re.IGNORECASE )
                        matches = paddingRegex.findall( os.path.basename( imageFileName ) )
                        if matches != None and len( matches ) > 0:
                            outputName = imageFileName.replace( '#', paddedFrameNumber )
                            splitFilename = os.path.split( outputName )
                            tileName = os.path.join( splitFilename[0], "_tile?_" +splitFilename[1] )
                        else:
                            splitFilename = os.path.split( outputName )
                            if needFrameNumber:
                                splitExt = os.path.splitext( splitFilename[1] )
                                outputName = os.path.join(
                                    splitFilename[0],
                                    splitExt[0] + '.' + paddedFrameNumber + splitExt[1]
                                )
                                splitFilename = os.path.split( outputName )
                            tileName = os.path.join( splitFilename[0], "_tile?_"+splitFilename[1] )

                        date = time.strftime("%Y_%m_%d_%H_%M_%S")
                        configFilename = os.path.join( ClientUtils.GetDeadlineTempPath(), os.path.basename(outputName)+"_"+str(frame)+"_config_"+date+".txt" )
                        configFilename = configFilename.replace( "\\", "/" )
                        
                        writer = StreamWriter( configFilename, False, Encoding.Unicode )
                        writer.WriteLine( "" )
                        writer.WriteLine( "ImageFileName=" + outputName )
                        backgroundType = scriptDialog.GetValue( "AssembleOverBox" )
                        if backgroundType == "Previous Output":
                            writer.WriteLine( "BackgroundSource=" +outputName +"\n" )
                        elif backgroundType == "Selected Image":
                            writer.WriteLine( "BackgroundSource=" +scriptDialog.GetValue( "BackgroundBox" ) +"\n" )
                        
                        writer.WriteLine( "TilesCropped=False" )
                        writer.WriteLine( "TileCount=" +str( tilesInX * tilesInY ) )
                        writer.WriteLine( "DistanceAsPixels=True" )

                        for currTile, (xStart, xSize, yStart, ySize) in enumerate( dlTileGenerator.getEachTile( returnSize=True ) ):

                                regionOutputFileName = tileName.replace( "?", str(currTile) )
                                
                                writer.WriteLine( "Tile%iFileName=%s"%( currTile,regionOutputFileName ) )
                                writer.WriteLine( "Tile%iX=%s"%( currTile, xStart ) )
                                writer.WriteLine( "Tile%iY=%s"%( currTile, yStart ) )
                                writer.WriteLine( "Tile%iWidth=%s"%( currTile, xSize  ) )
                                writer.WriteLine( "Tile%iHeight=%s"%( currTile, ySize  ) )
                    
                        writer.Close()
                        configFiles.append(configFilename)
                
                arguments = []
                arguments.append( jigsawJobInfoFilename )
                arguments.append( jigsawPluginInfoFilename )
                arguments.extend( configFiles )
                jobResult = ClientUtils.ExecuteCommandAndGetOutput( arguments )
                jobCount += 1

        if vrimg2exr:
            imageFileName = paddedOutputFile.replace("\\","/")

            outputName = imageFileName
            vrimgPaddingStr = '0' * parsedFramePadding
            exrPaddingStr = '#' * parsedFramePadding
            if '#' in outputName:
                vrimgInputFilename = outputName.replace( '#', vrimgPaddingStr )
                exrOutputFilename = outputName.replace( '#', exrPaddingStr )
                exrOutputDir, _ = os.path.splitext( exrOutputFilename )
                exrOutputFilename = exrOutputDir + '.exr'
            else:
                if needFrameNumber:
                    vrimgInputPrefix, vrimgInputExt = os.path.splitext( outputName )
                    vrimgInputFilename = vrimgInputPrefix + '.' + vrimgPaddingStr + vrimgInputExt
                    exrOutputPrefix, _ = os.path.splitext( outputName )
                    exrOutputFilename = exrOutputPrefix + '.' + exrPaddingStr + '.exr'
                else:
                    vrimgInputFilename = outputName
                    exrOutputPrefix, _ = os.path.splitext( outputName )
                    exrOutputFilename = exrOutputPrefix + '.exr'
            
            # Create job info file.
            convertJobInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "vrimg_job_info.job" )
            writer = StreamWriter( convertJobInfoFilename, False, Encoding.Unicode )
            writer.WriteLine( "Plugin=Vrimg2Exr" )
            writer.WriteLine( "Name=%s - Conversion Job" % jobName )
            writer.WriteLine( "BatchName=%s" % ( batchName ) ) 
            writer.WriteLine( "Comment=%s" % scriptDialog.GetValue( "CommentBox" ) )
            writer.WriteLine( "Department=%s" % scriptDialog.GetValue( "DepartmentBox" ) )
            writer.WriteLine( "Pool=%s" % scriptDialog.GetValue( "PoolBox" ) )
            writer.WriteLine( "SecondaryPool=%s" % scriptDialog.GetValue( "SecondaryPoolBox" ) )
            writer.WriteLine( "Group=%s" % scriptDialog.GetValue( "GroupBox" ) )
            writer.WriteLine( "Priority=%s" % scriptDialog.GetValue( "PriorityBox" ) )
            writer.WriteLine( "LimitGroups=%s" % scriptDialog.GetValue( "LimitGroupBox" ) )
            writer.WriteLine( "OnJobComplete=%s" % scriptDialog.GetValue( "OnJobCompleteBox" ) )
            writer.WriteLine( "MachineLimit=%s" % scriptDialog.GetValue( "MachineLimitBox" ) )
            writer.WriteLine( "Frames=%s" % frames )
            writer.WriteLine( "ChunkSize=1" )
            writer.WriteLine( "JobDependencies=%s" % ",".join(jobIds) )
            
            if( bool(scriptDialog.GetValue( "IsBlacklistBox" )) ):
                writer.WriteLine( "Blacklist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
            else:
                writer.WriteLine( "Whitelist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
            
            if( bool(scriptDialog.GetValue( "SubmitSuspendedBox" )) ):
                writer.WriteLine( "InitialStatus=Suspended" )
            
            if(len(outputFile) > 0):
                writer.WriteLine( "OutputFilename0=%s" % exrOutputFilename )
            
            writer.Close()
            
            # Create plugin info file.
            convertPluginInfoFilename = Path.Combine( ClientUtils.GetDeadlineTempPath(), "vrimg_plugin_info.job" )
            writer = StreamWriter( convertPluginInfoFilename, False, Encoding.Unicode )
            writer.WriteLine( "InputFile=%s" % vrimgInputFilename )
            writer.WriteLine( "OutputFile=" )
            writer.WriteLine( "Half=False" )
            writer.WriteLine( "sRGB=False" )
            writer.WriteLine( "SetGamma=False" )
            writer.WriteLine( "Gamma=1.8" )
            writer.WriteLine( "SetChannel=False" )
            writer.WriteLine( "Channel=" )
            writer.WriteLine( "SetCompression=False" )
            writer.WriteLine( "Compression=zip" )
            writer.WriteLine( "SetBufferSize=False" )
            writer.WriteLine( "BufferSize=10" )
            writer.WriteLine( "DeleteInputFiles=%s" % scriptDialog.GetValue( "DeleteVrimgBox" ) )
            writer.Close()
            
            # Setup the command line arguments.
            arguments = StringCollection()
            arguments.Add( convertJobInfoFilename )
            arguments.Add( convertPluginInfoFilename )
            jobResult = ClientUtils.ExecuteCommandAndGetOutput( arguments )
            jobCount += 1
        
    if jobCount == 1:
        scriptDialog.ShowMessageBox( jobResult, "Submission Results" )
    else:
        scriptDialog.ShowMessageBox( ("All %d jobs submitted" % jobCount), "Submission Results" )
        
class deadlineParsingProgressDialog(DeadlineScriptDialog):
    # ...
    finishedParse = QtCore.pyqtSignal()
    
    def __init__(self, filename, pathOverride, parent=None):
        # type: (str, str, Optional[Any]) -> None
        self.filename = filename
        self.parent = parent
        super(deadlineParsingProgressDialog, self).__init__(self.parent)
        
        self.vrsceneUpdateTimer = None  # type: Any
        self.vrsceneThread = None
        self.ParseThread = None
        self.PathOverride = pathOverride
        
        self.parseResults = []  # type: List
        
        self.SetTitle( "VrScene Parsing Progress" )
        self.SetIcon( self.GetIcon( 'Vray' ) )
        
        self.AddGrid()
        self.AddControlToGrid("infoLabel","LabelControl","The Vrscene is currently being parsed.\nCancelling this parsing will stop the job submission.", 0, 0, "", False)
        self.AddRangeControlToGrid("ProgressBox","ProgressBarControl", 0, 0, 100, 0, 0, 1, 0)
        closeButton = self.AddControlToGrid( "Cancel", "ButtonControl", "Cancel", 2, 0, expand=False )
        closeButton.ValueModified.connect(self.closeEvent)
        
        self.Shown.connect( self.onShown )
    
    def onShown( self ):
        # type: () -> None
        self.vrsceneUpdateTimer = threading.Timer( 1.0, self.updateProgress )
        self.vrsceneUpdateTimer.start()
        
        self.parseThread = threading.Thread( target = self.threadTarget, args = ( self.filename, self.PathOverride  ) )
        self.finishedParse.connect( self.close )
        self.parseThread.start()
                    
    def closeEvent(self, event):        
        # type: (QCloseEvent) -> None
        self.vrsceneUpdateTimer.cancel()
        if self.parseThread.isAlive():
            VrsceneUtils.CancelParsing()
                
        while self.parseThread.isAlive():
            time.sleep( 0.2 )
        
        super(deadlineParsingProgressDialog, self).closeEvent(self.parent)
        
    def updateProgress( self ):
        # type: () -> None
        if self.parseThread.isAlive():
            self.SetValue( "ProgressBox", VrsceneUtils.GetProgress()*100 )
            self.vrsceneUpdateTimer = threading.Timer(1.0, self.updateProgress)
            self.vrsceneUpdateTimer.start()
        else:
            self.CloseDialog()
 
    def threadTarget( self, filename, PathOverride ):
        # type: (str, str) -> None
        try:
            VrsceneUtils.get_output_data_from_vrscene_file( filename, PathOverride )
        except Exception as e:
            self.ShowMessageBox( six.text_type(e), "Parsing Error" )
        finally:
            self.finishedParse.emit(  )
