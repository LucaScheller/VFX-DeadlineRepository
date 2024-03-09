from __future__ import annotations

import copy
import datetime
import enum
import getpass
import os
import re
import logging
from dataclasses import dataclass

LOG = logging.getLogger(__name__)

#########################################
# Deadline Scripting API
# This is a 1:1 Jobs Enum compatibility layer.
# Differences:
#   - DateTime/TimeSpan Classes wrap
#     Python's internals to allow invalid
#     state tracking.
#########################################


class AutoJobCleanupType(enum.Enum):
    DeleteJobs = 0
    ArchiveJobs = 1


class JobCompleteAction(enum.Enum):
    Archive = 0
    Delete = 1
    Nothing = 2


class JobStatus(enum.Enum):
    Unknown = 0
    Active = 1
    Suspended = 2
    Completed = 3
    Failed = 4
    Pending = 6


class TaskOnTimeout(enum.Enum):
    ErrorAndNotify = 0
    Error = 1
    Notify = 2
    Complete = 3
    RequeueAndNotify = 4
    Requeue = 5
    FailAndNotify = 6
    Fail = 7


class JobScheduledType(enum.Enum):
    None_ = 0
    NotScheduled = None
    Once = 1
    Daily = 2
    Custom = 3


@dataclass
class BaseDependency:
    Notes: str
    IgnoreFrameOffsets: bool


@dataclass
class OffsetDependency(BaseDependency):
    OverrideFrameOffsets: bool
    StartOffset: int
    EndOffset: int


@dataclass
class AssetDependency(OffsetDependency):
    FileName: str
    IsFrameAware: bool
    FrameString: str


@dataclass
class ScriptDependency(OffsetDependency):
    FileName: str


@dataclass
class PathMappingRule:
    Path: str
    WindowsPath: str
    LinuxPath: str
    MacPath: str
    CaseSensitive: bool
    RegularExpression: bool
    Region: str


class DateTime:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        # This is a predefined constant from the WebAPI
        self._disabled = "0001-01-01T00:00:00Z"
        if not len(args) and not len(kwargs):
            self._datetime = None
            self._valid = False
        else:
            self._datetime = datetime.datetime(*args, **kwargs)
            self._valid = True

    def valid(self):
        """Check if the time is configured correctly.
        Returns:
            bool: The state.
        """
        return self._valid

    def record(self):
        """Get the internal time record. This may be None
        if the record is invalid.
        Returns:
            datetime.datetime | None: The time record.
        """
        if self._valid:
            return self._datetime
        else:
            return None

    def parse(self, value: str):
        """Parse the given time.
        Args:
            value (str): A iso formatted time.
        """
        try:
            self._datetime = datetime.time.fromisoformat(value)
            self._valid = True
        except ValueError:
            self._valid = False

    def format(self):
        """Format the defined time.
        Returns:
            str: A iso formatted time.
        """
        if not self._valid:
            return self._disabled
        else:
            return self._datetime.isoformat()


class TimeSpan:
    def __init__(self, hour=0, minute=0, second=0) -> None:
        super().__init__()
        self._time = datetime.time(hour=hour, minute=minute, second=second)
        # This is a predefined constant from the WebAPI
        self._disabled = "-10675199.02:48:05.4775808"
        self._valid = not (hour == 0 and minute == 0 and second == 0)

    def valid(self):
        """Check if the time is configured correctly.
        Returns:
            bool: The state.
        """
        return self._valid

    def record(self):
        """Get the internal time record. This may be None
        if the record is invalid.
        Returns:
            datetime.time | None: The time record.
        """
        if self._valid:
            return self._time
        else:
            return None

    def parse(self, value: str):
        """Parse the given time.
        Args:
            value (str): A iso formatted time.
        """
        try:
            self._time = datetime.time.fromisoformat(value)
            self._valid = True
        except ValueError:
            self._valid = False

    def format(self):
        """Format the defined time.
        Returns:
            str: A iso formatted time.
        """
        if not self._valid:
            return self._disabled
        else:
            return self._time.isoformat()


class FrameList:
    @staticmethod
    def convertFrameListToFrameString(frameList: list[int]):
        """Convert the frame list into a frame string.
        As per deadline's specification, the frame string may contain duplicate entries.
        Args:
            frameList (list[int]): A list of frames.
        Returns:
            str: A frame string.
        """
        # Expand iterables
        # Make copy to avoid ptr leaks
        frameList = list(copy.deepcopy(frameList))
        # Stringify
        if len(frameList) == 0:
            return ""
        elif len(frameList) == 1:
            return str(frameList[0])
        elif len(frameList) == 2:
            return ",".join([str(f) for f in frameList])
        frameString = []
        frameStack = []
        frameIntervals = set()
        framePreviousInterval = -1
        framePrevious = []
        frameIter = 0
        for frame in frameList:
            frameIter += 1
            if framePrevious:
                frameIntervals.add(abs(frame - framePrevious[-1]))
            framePrevious.append(frame)
            frameStack.append(frame)
            if frameIter == 1:
                continue
            if len(frameIntervals) == 1:
                framePreviousInterval = list(frameIntervals)[0]
                if frameIter != len(frameList):
                    continue
            if framePreviousInterval != -1:
                if framePreviousInterval != 1:
                    if len(frameStack) > 3:
                        if frameIter != len(frameList):
                            frameString.append(
                                "{}-{}x{}".format(
                                    frameStack[0], frameStack[-2], framePreviousInterval
                                )
                            )
                        else:
                            frameString.append(
                                "{}-{}x{}".format(
                                    frameStack[0], frameStack[-1], framePreviousInterval
                                )
                            )
                    else:
                        frameString.extend([str(f) for f in frameStack[:-1]])
                        frameString.append(str(frameStack[-1]))
                else:
                    if frameIter != len(frameList):
                        frameString.append(
                            "{}-{}".format(frameStack[0], frameStack[-2])
                        )
                    else:
                        frameString.append(
                            "{}-{}".format(frameStack[0], frameStack[-1])
                        )
            else:
                frameString.extend([str(f) for f in frameStack[:-1]])
            frameStack = frameStack[-1:]
            frameIntervals.clear()
            framePreviousInterval = -1
        return ",".join(frameString)

    @staticmethod
    def convertFrameStringToFrameList(frameStr: str):
        """Convert the frame list into a frame string.
        As per deadline's specification, the list may contain duplicate entries.

        Args:
            frameStr (str): A frame string.
        Returns:
            list[int]: A list of frames.
        """
        # Conform
        frameStr = frameStr.replace("step", "x")
        frameStr = frameStr.replace("by", "x")
        frameStr = frameStr.replace("every", "x")
        frameItems = re.split(",| ", frameStr)
        frameItems = [i for i in frameItems if i]
        # Expand
        frameList = []
        for frameItem in frameItems:
            if frameItem.count(":") == 2:
                frameStart, frameEnd, frameStep = frameItem.split(":")
                frameList.extend(
                    range(int(frameStart), int(frameEnd) + 1, int(frameStep))
                )
            elif frameItem.count("-") == 1 and (
                frameItem.count(":") == 1 or frameItem.count("x") == 1
            ):
                frameRange, frameStep = re.split(":|x", frameItem)
                frameStart, frameEnd = frameRange.split("-")
                if frameEnd < frameStart:
                    frameRange = reversed(
                        range(int(frameEnd), int(frameStart) + 1, int(frameStep))
                    )
                else:
                    frameRange = range(
                        int(frameStart), int(frameEnd) + 1, int(frameStep)
                    )
                frameList.extend(frameRange)
            elif frameItem.count("-") == 1:
                frameStart, frameEnd = frameItem.split("-")
                if frameEnd < frameStart:
                    frameRange = reversed(range(int(frameEnd), int(frameStart) + 1))
                else:
                    frameRange = range(int(frameStart), int(frameEnd) + 1)
                frameList.extend(frameRange)
            else:
                frameList.append(int(frameItem))

        return frameList


#########################################
# Deadline Scripting API
# This is a 1:1 Job Class compatibility layer.
#########################################


def jobPermissionSubmit(func):
    def wrapper_method(*args, **kwargs):
        cls_self = args[0]
        if cls_self.JobId is not None:
            raise Exception("'{}' can only be edited pre-submit.".format(func.__name__))
        func(*args, **kwargs)
    return wrapper_method


def jobPermissionRead(func):
    def wrapper_method(*args, **kwargs):
        raise Exception("'{}' can only be edited pre-submit.".format(func.__name__))
        func(*args, **kwargs)
    return wrapper_method

class JobInternalData(dict):
    """Instead of storing nested dicts, we store the
    configuration state as a flat dict, so that we
    can easily track the changeset."""

    def __init__(self) -> None:
        self._changeSet = set()

        self.setupData()
        self.resetChangeTracker()

    def __getattribute__(self, __name: str) -> any:
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: any) -> None:
        if hasattr(self, "_change_set"):
            self._changeSet.add(__name)
        return super().__setattr__(__name, __value)

    def setupData(self) -> None:
        """This defines the job defaults."""

        # This data couldn't be mapped from the WebService API
        _unknownData = {
            "Props": {
                "Region": "",
                "OptIns": {},
                "AWSPortalAssets": [],
                "AWSPortalAssetFileWhitelist": [],
            },
            "ComFra": 0,
            "SnglTskPrg": "0 %",
            "Bad": [],  # Bad Workers, can't be updated by WebService
            "IsSub": True,
            "Purged": False,
            "DataSize": -1,
            "ConcurrencyToken": None,
            "ExtraElements": None,
        }

        # Job General
        self.repository = ""
        self.id = None
        self.name = "JobName"
        self.batchName = "JobBatchName"
        self.priority = 0
        self.protected = False
        self.userName = getpass.getuser()
        self.department = "pipeline"
        self.comment = ""
        self.frames = []
        self.framesPerTask = 1
        self.framesSequential = False
        # Job Environment
        self.environment = {}
        self.environmentIsolateEnable = False
        self.environmentSubmissionIncludeEnable = False
        # Job Info
        self.info = {}
        self.infoExtra = {}
        self.infoExtraIndexed = {idx: "" for idx in range(0, 10)}
        # Job Files
        self.filePathMapping = []
        self.fileOutputDirectoryPaths = []
        self.fileOutputFileNames = []
        self.fileAuxiliarySubmissionFileNames = []
        self.fileAuxiliarySubmissionSyncFileEnable = False
        # Job Limits/Groups/Pools/Machines
        self.resourceLimits = []
        self.machinePool = ""
        self.machineSecondaryPool = ""
        self.machineGroup = ""
        self.machineLimit = 0
        self.machineLimitProgress = 100.0
        self.machineListedInclude = False
        self.machineListedNames = []
        self.taskConcurrencyLimit = 10
        self.taskConcurrencyLimitToNumberOfCpus = True
        # Job State
        self.status = JobStatus.Unknown
        self.statusErrorWarningSend = False
        self.statusFailureDetectionJobOverrideEnable = False
        self.statusFailureDetectionJobErrors = 0
        self.statusFailureDetectionTaskOverrideEnable = False
        self.statusFailureDetectionTaskErrors = 0
        self.statusFailureDetectionMachineBadIgnore = False
        self.statusInterruptable = False
        self.statusInterruptablePercentage = 1
        self.statusInterruptableRemainingTimeThreshold = 0
        self.statusTimeoutJobMinSeconds = 0
        self.statusTimeoutPluginInitializeMaxSeconds = 0
        self.statusTimeoutTaskMinSeconds = 0
        self.statusTimeoutTaskMaxSeconds = 0
        self.statusTimeoutScriptEnable = True
        self.statusTimeoutAutoEnable = False
        self.statusTimeoutFrameBasedEnable = False
        self.onJobComplete = JobCompleteAction.Nothing
        self.onTaskTimeout = TaskOnTimeout.Error
        # Job Tasks
        self.taskInfoExtraNameOverrideEnable = False
        self.taskInfoExtraNameIndexed = {idx: "" for idx in range(0, 10)}
        # Job Plugin
        self.plugin = ""
        self.pluginInfo = {}
        self.pluginForceReload = False
        self.pluginDirectoryCustom = ""
        # Job Event Plugins
        self.eventOptIns = []
        self.eventSuppress = False
        self.eventDirectoryCustom = ""
        # Job Pre/Post (Task) Scripts
        self.scriptPreJob = ""
        self.scriptPostJob = ""
        self.scriptPreTask = ""
        self.scriptPostTask = ""
        # Job Dependencies
        self.dependencyResumeOnCompleted = True
        self.dependencyResumeOnDeleted = False
        self.dependencyResumeOnFailed = False
        self.dependencyResumePendingPercentageValue = 100.0
        self.dependencyFrameEnabled = True
        self.dependencyFrameOffsetStart = 0
        self.dependencyFrameOffsetEnd = 0
        self.dependencyJobs = []
        self.dependencyAssets = []
        self.dependencyScripts = []
        # Job Cleanup
        self.cleanupAutomaticOverrideEnable = False
        self.cleanupAutomaticType = AutoJobCleanupType.DeleteJobs
        self.cleanupOverrideEnable = False
        self.cleanupOverrideDays = 0
        # Job Stats
        self.statsJobSubmissionMachine = ""
        self.statsJobSubmissionDateTime = DateTime()
        self.statsJobStartedDateTime = DateTime()
        self.statsJobCompletedDateTime = DateTime()
        self.statsJobErrors = -1
        self.statsTasksCount = -1
        self.statsTasksQueued = -1
        self.statsTasksRendering = -1
        self.statsTasksPending = -1
        self.statsTasksCompleted = -1
        self.statsTasksSuspended = -1
        self.statsTasksFailed = -1
        # Job Notifications
        self.notificationMethodOverrideEnable = False
        self.notificationTargets = []
        self.notificationPopupEnable = False
        self.notificationEmailEnable = False
        self.notificationEmails = []
        self.notificationNote = ""
        # Job Maintenance
        self.maintenanceJobEnable = False
        self.maintenanceJobStartFrame = 0
        self.maintenanceJobEndFrame = 0
        # Job Time Schedule
        self.scheduledType = JobScheduledType.None_
        self.scheduledDayInterval = 3
        self.scheduledDayTimeStart = DateTime()
        self.scheduledDayTimeEnd = DateTime()
        self.scheduledDayTimeDisabled = TimeSpan()
        self.scheduledDayMondayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDayMondayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDayTuesdayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDayTuesdayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDayWednesdayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDayWednesdayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDayThursdayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDayThursdayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDayFridayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDayFridayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDaySaturdayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDaySaturdayTimeEnd = self.scheduledDayTimeDisabled
        self.scheduledDaySundayTimeStart = self.scheduledDayTimeDisabled
        self.scheduledDaySundayTimeEnd = self.scheduledDayTimeDisabled
        # Job Tile Rendering
        self.tileEnable = False
        self.tileFrame = -1
        self.tileOutputFileNames = []
        self.tileTilesCount = -1
        self.tileTilesInX = 0
        self.tileTilesInY = 0

    def getChangeSet(self):
        return self._changeSet

    def resetChangeTracker(self):
        self._changeSet.clear()


class Job(object):
    def __init__(self) -> None:
        self._data = JobInternalData()

    #########################################
    # Private
    #########################################

    def _GetJobExtraInfoIndex(self, idx: int):
        return self._data.infoExtraIndexed.get(idx, None)

    def _SetJobExtraInfoIndex(self, idx: int, value: str):
        if value is None:
            self._data.infoExtraIndexed.pop(idx, None)
        else:
            self._data.infoExtraIndexed[idx] = value

    def _GetJobTaskExtraInfoNameIndex(self, idx: int):
        return self._data.taskInfoExtraNameIndexed.get(idx, None)

    def _SetJobTaskExtraInfoNameIndex(self, idx: int, value: str):
        if value is None:
            self._data.taskInfoExtraNameIndexed.pop(idx, None)
        else:
            self._data.taskInfoExtraNameIndexed[idx] = value

    #########################################
    # Public
    #########################################

    def deserializeWebAPI(self, data: dict) -> Job:
        """Deserialize this class from the Web API compatible format.
        Args:
            data (dict): A REST API dict.
        Returns:
            Job: The deserialized job object.
        """
        # Job General
        self._data.id = data["_id"]
        self._data.name = data["Props"]["Name"]
        self._data.batchName = data["Props"]["Batch"]
        self._data.priority = data["Props"]["Pri"]
        self._data.protected = data["Props"]["Protect"]
        self._data.userName = data["Props"]["User"]
        self._data.department = data["Props"]["Dept"]
        self._data.comment = data["Props"]["Cmmt"]
        self._data.frames = FrameList.convertFrameStringToFrameList(
            data["Props"]["Frames"]
        )
        self._data.framesPerTask = data["Props"]["Chunk"]
        self._data.framesSequential = data["Props"]["Seq"]
        # Job Environment
        self._data.environment = data["Props"]["Env"]
        self._data.environmentIsolateEnable = data["Props"]["EnvOnly"]
        self._data.environmentSubmissionIncludeEnable = False
        # Job Info
        self._data.info = {}  # TODO HINT Deprecated
        self._data.infoExtra = data["Props"]["ExDic"]
        self._data.infoExtraIndexed = {
            idx: data["Props"]["Ex{}".format(idx)] for idx in range(0, 10)
        }
        # Job Files
        for pathMappingData in data["Props"]["PathMap"]:
            pathMappingRule = PathMappingRule(
                Path=pathMappingData["Path"],
                WindowsPath=pathMappingData["WindowsPath"],
                LinuxPath=pathMappingData["LinuxPath"],
                MacPath=pathMappingData["MacPath"],
                CaseSensitive=pathMappingData["CaseSensitive"],
                RegularExpression=pathMappingData["RegularExpression"],
                Region=pathMappingData["Region"],
            )
            self._data.filePathMapping.append(pathMappingRule)
        self._data.fileOutputDirectoryPaths = data["OutDir"]
        self._data.fileOutputFileNames = data["OutFile"]
        self._data.fileAuxiliarySubmissionFileNames = data["Aux"]
        self._data.fileAuxiliarySubmissionSyncFileEnable = data["Props"]["AuxSync"]
        # Job Limits/Pools/Groups/Machines
        self._data.resourceLimits = data["Props"]["Limits"]
        self._data.machinePool = data["Props"]["Pool"]
        self._data.machineSecondaryPool = data["Props"]["SecPool"]
        self._data.machineGroup = data["Props"]["Grp"]
        self._data.machineLimit = data["Props"]["MachLmt"]
        self._data.machineLimitProgress = data["Props"]["MachLmtProg"]
        self._data.machineListedInclude = data["Props"]["White"]
        self._data.machineListedNames = data["Props"]["ListedSlaves"]
        self._data.taskConcurrencyLimit = data["Props"]["Conc"]
        self._data.taskConcurrencyLimitToNumberOfCpus = data["Props"]["ConcLimt"]
        # Job State
        self._data.status = JobStatus(data["Stat"])
        self._data.statusErrorWarningSend = data["Props"]["SndWarn"]
        self._data.statusFailureDetectionJobOverrideEnable = data["Props"]["JobFailOvr"]
        self._data.statusFailureDetectionJobErrors = data["Props"]["JobFailErr"]
        self._data.statusFailureDetectionTaskOverrideEnable = data["Props"][
            "TskFailOvr"
        ]
        self._data.statusFailureDetectionTaskErrors = data["Props"]["TskFailErr"]
        self._data.statusFailureDetectionMachineBadIgnore = data["Props"]["NoBad"]
        self._data.statusInterruptable = data["Props"]["Int"]
        self._data.statusInterruptablePercentage = data["Props"]["IntPer"]
        self._data.statusInterruptableRemainingTimeThreshold = data["Props"]["RemTmT"]
        self._data.statusTimeoutJobMinSeconds = data["Props"]["StartTime"]
        self._data.statusTimeoutPluginInitializeMaxSeconds = data["Props"][
            "InitializePluginTime"
        ]
        self._data.statusTimeoutTaskMinSeconds = data["Props"]["MinTime"]
        self._data.statusTimeoutTaskMaxSeconds = data["Props"]["MaxTime"]
        self._data.statusTimeoutScriptEnable = data["Props"]["TimeScrpt"]
        self._data.statusTimeoutAutoEnable = data["Props"]["AutoTime"]
        self._data.statusTimeoutFrameBasedEnable = data["Props"]["FrameTimeout"]
        self._data.onJobComplete = JobCompleteAction(data["Props"]["OnComp"])
        self._data.onTaskTimeout = TaskOnTimeout(data["Props"]["Timeout"])
        # Job Tasks
        self._data.taskInfoExtraNameOverrideEnable = data["Props"]["OvrTaskEINames"]
        self._data.taskInfoExtraNameIndexed = {
            idx: data["Props"]["TaskEx{}".format(idx)] for idx in range(0, 10)
        }
        # Job Plugin
        self._data.plugin = data["Plug"]
        self._data.pluginInfo = data["Props"]["PlugInfo"]
        self._data.pluginForceReload = data["Props"]["Reload"]
        self._data.pluginDirectoryCustom = data["Props"]["PlugDir"]
        # Job Event Plugins
        self._data.eventSuppress = data["Props"]["NoEvnt"]
        self._data.eventDirectoryCustom = data["Props"]["EventDir"]
        # Job Pre/Post (Task) Scripts
        self._data.scriptPreJob = data["Props"]["PrJobScrp"]
        self._data.scriptPostJob = data["Props"]["PoJobScrp"]
        self._data.scriptPreTask = data["Props"]["PrTskScrp"]
        self._data.scriptPostTask = data["Props"]["PoTskScrp"]
        # Job Dependencies
        self._data.dependencyResumeOnCompleted = data["Props"]["DepComp"]
        self._data.dependencyResumeOnDeleted = data["Props"]["DepDel"]
        self._data.dependencyResumeOnFailed = data["Props"]["DepFail"]
        self._data.dependencyResumePendingPercentageValue = data["Props"]["DepPer"]
        self._data.dependencyFrameEnabled = data["Props"]["DepFrame"]
        self._data.dependencyFrameOffsetStart = data["Props"]["DepFrameStart"]
        self._data.dependencyFrameOffsetEnd = data["Props"]["DepFrameEnd"]
        self._data.dependencyJobs = data["Props"]["Dep"]
        self._data.dependencyAssets = [
            AssetDependency(
                FileName=d["FileName"],
                Notes=d["Notes"],
                IgnoreFrameOffsets=d["IgnoreFrameOffsets"],
                IsFrameAware=d["IsFrameAware"],
                FrameString=d["FrameString"],
                OverrideFrameOffsets=d["OverrideFrameOffsets"],
                StartOffset=d["StartOffset"],
                EndOffset=d["EndOffset"],
            )
            for d in data["Props"]["ReqAss"]
        ]
        self._data.dependencyScripts = [
            ScriptDependency(
                FileName=s["FileName"],
                Notes=s["Notes"],
                IgnoreFrameOffsets=s["IgnoreFrameOffsets"],
            )
            for s in data["Props"]["ScrDep"]
        ]
        # Job Cleanup
        self._data.cleanupAutomaticOverrideEnable = data["Props"]["OverAutoClean"]
        self._data.cleanupAutomaticType = AutoJobCleanupType(
            data["Props"]["OverCleanType"]
        )
        self._data.cleanupOverrideEnable = data["Props"]["OverClean"]
        self._data.cleanupOverrideDays = data["Props"]["OverCleanDays"]
        # Job Stats
        self._data.statsJobSubmissionMachine = data["Mach"]
        self._data.statsJobSubmissionDateTime.parse(data["Date"])
        self._data.statsJobStartedDateTime.parse(data["DateStart"])
        self._data.statsJobCompletedDateTime.parse(data["DateComp"])
        self._data.statsJobErrors = data["Errs"]
        self._data.statsTasksCount = data["Props"]["Tasks"]
        self._data.statsTasksQueued = data["QueuedChunks"]
        self._data.statsTasksRendering = data["RenderingChunks"]
        self._data.statsTasksPending = data["PendingChunks"]
        self._data.statsTasksCompleted = data["CompletedChunks"]
        self._data.statsTasksSuspended = data["SuspendedChunks"]
        self._data.statsTasksFailed = data["FailedChunks"]
        # Job Notifications
        self._data.notificationMethodOverrideEnable = data["Props"]["NotOvr"]
        self._data.notificationTargets = data["Props"]["NotUser"]
        self._data.notificationPopupEnable = data["Props"]["SndPopup"]
        self._data.notificationEmailEnable = data["Props"]["SndEmail"]
        self._data.notificationEmails = data["Props"]["NotEmail"]
        self._data.notificationNote = data["Props"]["NotNote"]
        # Job Maintenance
        self._data.maintenanceJobEnable = data["Main"]
        self._data.maintenanceJobStartFrame = data["MainStart"]
        self._data.maintenanceJobEndFrame = data["MainEnd"]
        # Job Time Schedule
        self._data.scheduledType = JobScheduledType(data["Props"]["Schd"])
        self._data.scheduledDayInterval = data["Props"]["SchdDays"]
        self._data.scheduledDayTimeStart.parse(data["Props"]["SchdDate"])
        self._data.scheduledDayTimeEnd.parse(data["Props"]["SchdStop"])
        self._data.scheduledDayMondayTimeStart.parse(data["Props"]["MonStart"])
        self._data.scheduledDayMondayTimeStart.parse(data["Props"]["MonStop"])
        self._data.scheduledDayTuesdayTimeStart.parse(data["Props"]["TueStart"])
        self._data.scheduledDayTuesdayTimeEnd.parse(data["Props"]["TueStop"])
        self._data.scheduledDayWednesdayTimeStart.parse(data["Props"]["WedStart"])
        self._data.scheduledDayWednesdayTimeEnd.parse(data["Props"]["WedStop"])
        self._data.scheduledDayThursdayTimeStart.parse(data["Props"]["ThuStart"])
        self._data.scheduledDayThursdayTimeEnd.parse(data["Props"]["ThuStop"])
        self._data.scheduledDayFridayTimeStart.parse(data["Props"]["FriStart"])
        self._data.scheduledDayFridayTimeEnd.parse(data["Props"]["FriStop"])
        self._data.scheduledDaySaturdayTimeStart.parse(data["Props"]["SatStart"])
        self._data.scheduledDaySaturdayTimeEnd.parse(data["Props"]["SatStop"])
        self._data.scheduledDaySundayTimeStart.parse(data["Props"]["SunStart"])
        self._data.scheduledDaySundayTimeEnd.parse(data["Props"]["SunStop"])
        # Job Tile Rendering
        self._data.tileEnable = data["Tile"]
        self._data.tileFrame = data["TileFrame"]
        self._data.tileOutputFileNames = data["TileFile"]
        self._data.tileTilesCount = data["TileCount"]
        self._data.tileTilesInX = data["TileX"]
        self._data.tileTilesInY = data["TileY"]

        return self

    def serializeWebAPI(self) -> dict:
        """Serialize this class to the Web API compatible format.
        Returns:
            dict: The serialized job object.
        """
        data = {"Props": {}}
        # Job General
        data["_id"] = self._data.id
        data["Props"]["Name"] = self._data.name
        data["Props"]["Batch"] = self._data.batchName
        data["Props"]["Pri"] = self._data.priority
        data["Props"]["Protect"] = self._data.protected
        data["Props"]["User"] = self._data.userName
        data["Props"]["Dept"] = self._data.department
        data["Props"]["Cmmt"] = self._data.comment
        data["Props"]["Frames"] = FrameList.convertFrameListToFrameString(
            self._data.frames
        )
        data["Props"]["Chunk"] = self._data.framesPerTask
        data["Props"]["Seq"] = self._data.framesSequential
        # Job Environment
        data["Props"]["Env"] = self._data.environment
        data["Props"]["EnvOnly"] = self._data.environmentIsolateEnable
        if self._data.id is None:
            # On submission env merge
            if self._data.environmentSubmissionIncludeEnable:
                systemEnv = copy.deepcopy(os.environ.items())
                systemEnv.update(copy.deepcopy(self._data.environment))
                data["Props"]["Env"] = systemEnv
        # Job Info
        # data[""] = self._data.info # TODO HINT Deprecated
        data["Props"]["ExDic"] = self._data.infoExtra
        for key, value in self._data.infoExtraIndexed.items():
            data["Props"]["Ex{}".format(key)] = value
        # Job Files
        data["Props"]["PathMap"] = []
        for pathMappingRule in self._data.filePathMapping:
            data["Props"]["PathMap"].append(
                {
                    "Path": pathMappingRule.Path,
                    "WindowsPath": pathMappingRule.WindowsPath,
                    "LinuxPath": pathMappingRule.LinuxPath,
                    "MacPath": pathMappingRule.MacPath,
                    "CaseSensitive": pathMappingRule.CaseSensitive,
                    "RegularExpression": pathMappingRule.RegularExpression,
                    "Region": pathMappingRule.Region,
                }
            )
        data["OutDir"] = self._data.fileOutputDirectoryPaths
        data["OutFile"] = self._data.fileOutputFileNames
        data["Aux"] = self._data.fileAuxiliarySubmissionFileNames
        data["Props"]["AuxSync"] = self._data.fileAuxiliarySubmissionSyncFileEnable
        # Job Limits/Groups/Pools/Machines
        data["Props"]["Limits"] = self._data.resourceLimits
        data["Props"]["Pool"] = self._data.machinePool
        data["Props"]["SecPool"] = self._data.machineSecondaryPool
        data["Props"]["Grp"] = self._data.machineGroup
        data["Props"]["MachLmt"] = self._data.machineLimit
        data["Props"]["MachLmtProg"] = self._data.machineLimitProgress
        data["Props"]["White"] = self._data.machineListedInclude
        data["Props"]["ListedSlaves"] = self._data.machineListedNames
        data["Props"]["Conc"] = self._data.taskConcurrencyLimit
        data["Props"]["ConcLimt"] = self._data.taskConcurrencyLimitToNumberOfCpus
        # Job State
        data["Stat"] = self._data.status.value
        data["Props"]["SndWarn"] = self._data.statusErrorWarningSend
        data["Props"]["JobFailOvr"] = self._data.statusFailureDetectionJobOverrideEnable
        data["Props"]["JobFailErr"] = self._data.statusFailureDetectionJobErrors
        data["Props"][
            "TskFailOvr"
        ] = self._data.statusFailureDetectionTaskOverrideEnable
        data["Props"]["TskFailErr"] = self._data.statusFailureDetectionTaskErrors
        data["Props"]["NoBad"] = self._data.statusFailureDetectionMachineBadIgnore
        data["Props"]["Int"] = self._data.statusInterruptable
        data["Props"]["IntPer"] = self._data.statusInterruptablePercentage
        data["Props"]["RemTmT"] = self._data.statusInterruptableRemainingTimeThreshold
        data["Props"]["StartTime"] = self._data.statusTimeoutJobMinSeconds
        data["Props"][
            "InitializePluginTime"
        ] = self._data.statusTimeoutPluginInitializeMaxSeconds
        data["Props"]["MinTime"] = self._data.statusTimeoutTaskMinSeconds
        data["Props"]["MaxTime"] = self._data.statusTimeoutTaskMaxSeconds
        data["Props"]["TimeScrpt"] = self._data.statusTimeoutScriptEnable
        data["Props"]["AutoTime"] = self._data.statusTimeoutAutoEnable
        data["Props"]["FrameTimeout"] = self._data.statusTimeoutFrameBasedEnable
        data["Props"]["OnComp"] = self._data.onJobComplete.value
        data["Props"]["Timeout"] = self._data.onTaskTimeout.value
        # Job Tasks
        data["Props"]["OvrTaskEINames"] = self._data.taskInfoExtraNameOverrideEnable
        for idx in range(0, 10):
            data["Props"]["TaskEx{}".format(idx)] = self._data.taskInfoExtraNameIndexed[
                idx
            ]
        # Job Plugin
        data["Plug"] = self._data.plugin
        data["Props"]["PlugInfo"] = self._data.pluginInfo
        data["Props"]["Reload"] = self._data.pluginForceReload
        data["Props"]["PlugDir"] = self._data.pluginDirectoryCustom
        # Job Event Plugins
        data["Props"]["EventOI"] = ",".join(self._data.eventOptIns)
        data["Props"]["NoEvnt"] = self._data.eventSuppress
        data["Props"]["EventDir"] = self._data.eventDirectoryCustom
        # Job Pre/Post (Task) Scripts
        data["Props"]["PrJobScrp"] = self._data.scriptPreJob
        data["Props"]["PoJobScrp"] = self._data.scriptPostJob
        data["Props"]["PrTskScrp"] = self._data.scriptPreTask
        data["Props"]["PoTskScrp"] = self._data.scriptPostTask
        # Job Dependencies
        data["Props"]["DepComp"] = self._data.dependencyResumeOnCompleted
        data["Props"]["DepDel"] = self._data.dependencyResumeOnDeleted
        data["Props"]["DepFail"] = self._data.dependencyResumeOnFailed
        data["Props"]["DepPer"] = self._data.dependencyResumePendingPercentageValue
        data["Props"]["DepFrame"] = self._data.dependencyFrameEnabled
        data["Props"]["DepFrameStart"] = self._data.dependencyFrameOffsetStart
        data["Props"]["DepFrameEnd"] = self._data.dependencyFrameOffsetEnd
        data["Props"]["Dep"] = self._data.dependencyJobs
        data["Props"]["ReqAss"] = []
        for assetDependency in self._data.dependencyAssets:
            data["Props"]["ReqAss"].append(
                {
                    "FileName": assetDependency.FileName,
                    "Notes": assetDependency.Notes,
                    "IgnoreFrameOffsets": assetDependency.IgnoreFrameOffsets,
                    "IsFrameAware": assetDependency.IsFrameAware,
                    "FrameString": assetDependency.FrameString,
                    "OverrideFrameOffsets": assetDependency.OverrideFrameOffsets,
                    "StartOffset": assetDependency.StartOffset,
                    "EndOffset": assetDependency.EndOffset,
                }
            )
        data["Props"]["ScrDep"] = []
        for scriptDependency in self._data.dependencyScripts:
            data["Props"]["ScrDep"].append(
                {
                    "FileName": scriptDependency.FileName,
                    "Notes": scriptDependency.Notes,
                    "IgnoreFrameOffsets": scriptDependency.IgnoreFrameOffsets,
                }
            )
        # Job Cleanup
        data["Props"]["OverAutoClean"] = self._data.cleanupAutomaticOverrideEnable
        data["Props"]["OverCleanType"] = self._data.cleanupAutomaticType.value
        data["Props"]["OverClean"] = self._data.cleanupOverrideEnable
        data["Props"]["OverCleanDays"] = self._data.cleanupOverrideDays
        # Job Stats
        data["Mach"] = self._data.statsJobSubmissionMachine
        data["Date"] = self._data.statsJobSubmissionDateTime.format()
        # data["DateStart"] = self._data.statsJobStartedDateTime.format()
        # data["DateComp"] = self._data.statsJobCompletedDateTime.format()
        # data["Errs"] = self._data.statsJobErrors
        # data["Props"]["Tasks"] = self._data.statsTasksCount
        # data["QueuedChunks"] = self._data.statsTasksQueued
        # data["RenderingChunks"] = self._data.statsTasksRendering
        # data["PendingChunks"] = self._data.statsTasksPending
        # data["CompletedChunks"] = self._data.statsTasksCompleted
        # data["SuspendedChunks"] = self._data.statsTasksSuspended
        # data["FailedChunks"] = self._data.statsTasksFailed
        # Job Notifications
        data["Props"]["NotOvr"] = self._data.notificationMethodOverrideEnable
        data["Props"]["NotUser"] = self._data.notificationTargets
        data["Props"]["SndPopup"] = self._data.notificationPopupEnable
        data["Props"]["SndEmail"] = self._data.notificationEmailEnable
        data["Props"]["NotEmail"] = self._data.notificationEmails
        data["Props"]["NotNote"] = self._data.notificationNote
        # Job Maintenance
        data["Main"] = self._data.maintenanceJobEnable
        data["MainStart"] = self._data.maintenanceJobStartFrame
        data["MainEnd"] = self._data.maintenanceJobEndFrame
        # Job Time Schedule
        data["Props"]["Schd"] = self._data.scheduledType.value
        data["Props"]["SchdDays"] = self._data.scheduledDayInterval
        data["Props"]["SchdDate"] = self._data.scheduledDayTimeStart.format()
        data["Props"]["SchdStop"] = self._data.scheduledDayTimeEnd.format()
        data["Props"]["MonStart"] = self._data.scheduledDayMondayTimeStart.format()
        data["Props"]["MonStop"] = self._data.scheduledDayMondayTimeStart.format()
        data["Props"]["TueStart"] = self._data.scheduledDayTuesdayTimeStart.format()
        data["Props"]["TueStop"] = self._data.scheduledDayTuesdayTimeEnd.format()
        data["Props"]["WedStart"] = self._data.scheduledDayWednesdayTimeStart.format()
        data["Props"]["WedStop"] = self._data.scheduledDayWednesdayTimeEnd.format()
        data["Props"]["ThuStart"] = self._data.scheduledDayThursdayTimeStart.format()
        data["Props"]["ThuStop"] = self._data.scheduledDayThursdayTimeEnd.format()
        data["Props"]["FriStart"] = self._data.scheduledDayFridayTimeStart.format()
        data["Props"]["FriStop"] = self._data.scheduledDayFridayTimeEnd.format()
        data["Props"]["SatStart"] = self._data.scheduledDaySaturdayTimeStart.format()
        data["Props"]["SatStop"] = self._data.scheduledDaySaturdayTimeEnd.format()
        data["Props"]["SunStart"] = self._data.scheduledDaySundayTimeStart.format()
        data["Props"]["SunStop"] = self._data.scheduledDaySundayTimeEnd.format()
        # Job Tile Rendering
        data["Tile"] = self._data.tileEnable
        data["TileFrame"] = self._data.tileFrame
        data["TileCount"] = self._data.tileTilesCount
        data["TileFile"] = self._data.tileOutputFileNames
        data["TileX"] = self._data.tileTilesInX
        data["TileY"] = self._data.tileTilesInY

        return data

    def serializeSubmissionCommandlineDictionaries(self):
        """Serialize this class to the deadlinecommand submission
        file compatible data format.
        Returns:
            dict: The job data.
            dict: The plugin data.
            list[str]: The list of auxiliary file paths.
        """
        jobData = {}
        pluginData = {}
        auxFilePaths = []
        # Job General
        if self._data.repository:
            jobData["NetworkRoot"] = self._data.repository
        jobData["Name"] = self._data.name
        jobData["BatchName"] = self._data.batchName
        jobData["Priority"] = self._data.priority
        jobData["Protected"] = self._data.protected
        jobData["UserName"] = self._data.userName
        jobData["Department"] = self._data.department
        jobData["Comment"] = self._data.comment
        jobData["Frames"] = FrameList.convertFrameListToFrameString(self._data.frames)
        jobData["ChunkSize"] = self._data.framesPerTask
        jobData["Sequential"] = self._data.framesSequential
        # Job Environment
        env_idx = -1
        for key, value in self._data.environment:
            env_idx += 1
            jobData["EnvironmentKeyValue{}".format(env_idx)] = "{}={}".format(
                key, value
            )
        jobData["UseJobEnvironmentOnly"] = self._data.environmentIsolateEnable
        jobData["IncludeEnvironment"] = self._data.environmentSubmissionIncludeEnable
        # Job Info
        # job_data[""] = self._data.info # TODO HINT Deprecated
        extra_info_idx = -1
        for key, value in self._data.infoExtra.items():
            extra_info_idx += 1
            jobData["ExtraInfoKeyValue{}".format(extra_info_idx)] = "{}={}".format(
                key, value
            )
        for key, value in self._data.infoExtraIndexed.items():
            jobData["ExtraInfo{}".format(key)] = value
        # Job Files
        for idx, output_directory in enumerate(self._data.fileOutputDirectoryPaths):
            jobData["OutputDirectory{}".format(idx)] = output_directory
        if not self._data.tileEnable:
            for idx, output_file_name in enumerate(self._data.fileOutputFileNames):
                jobData["OutputFilename{}".format(idx)] = output_file_name
        for auxSubmissionFileName in self._data.fileAuxiliarySubmissionFileNames:
            auxFilePaths.append(auxSubmissionFileName)
        jobData["SynchronizeAllAuxiliaryFiles"] = (
            self._data.fileAuxiliarySubmissionSyncFileEnable
        )
        # Job Limits/Groups/Pools/Machines
        jobData["LimitGroups"] = ",".join(self._data.resourceLimits)
        jobData["Pool"] = self._data.machinePool
        jobData["SecondaryPool"] = self._data.machineSecondaryPool
        jobData["Group"] = self._data.machineGroup
        jobData["MachineLimit"] = self._data.machineLimit
        jobData["MachineLimitProgress"] = self._data.machineLimitProgress
        if self._data.machineListedInclude:
            jobData["Allowlist"] = ",".join(self._data.machineListedNames)
        else:
            jobData["Denylist"] = ",".join(self._data.machineListedNames)
        jobData["ConcurrentTasks"] = self._data.taskConcurrencyLimit
        jobData["LimitConcurrentTasksToNumberOfCpus"] = (
            self._data.taskConcurrencyLimitToNumberOfCpus
        )
        # Job State
        jobData["InitialStatus"] = self._data.status.name
        jobData["SendJobErrorWarning"] = self._data.statusErrorWarningSend
        jobData["OverrideJobFailureDetection"] = (
            self._data.statusFailureDetectionJobOverrideEnable
        )
        jobData["FailureDetectionJobErrors"] = (
            self._data.statusFailureDetectionJobErrors
        )
        jobData["OverrideTaskFailureDetection"] = (
            self._data.statusFailureDetectionTaskOverrideEnable
        )
        jobData["FailureDetectionTaskErrors"] = (
            self._data.statusFailureDetectionTaskErrors
        )
        jobData["IgnoreBadJobDetection"] = (
            self._data.statusFailureDetectionMachineBadIgnore
        )

        jobData["Interruptible"] = self._data.statusInterruptable
        jobData["InterruptiblePercentage"] = self._data.statusInterruptablePercentage
        jobData["RemTimeThreshold"] = (
            self._data.statusInterruptableRemainingTimeThreshold
        )
        jobData["StartJobTimeoutSeconds"] = self._data.statusTimeoutJobMinSeconds
        jobData["InitializePluginTimeoutSeconds"] = (
            self._data.statusTimeoutPluginInitializeMaxSeconds
        )
        jobData["MinRenderTimeSeconds"] = self._data.statusTimeoutTaskMinSeconds
        jobData["TaskTimeoutSeconds"] = self._data.statusTimeoutTaskMaxSeconds
        jobData["EnableTimeoutsForScriptTasks"] = self._data.statusTimeoutScriptEnable
        jobData["EnableAutoTimeout"] = self._data.statusTimeoutAutoEnable
        jobData["EnableFrameTimeouts"] = self._data.statusTimeoutFrameBasedEnable
        jobData["OnJobComplete"] = self._data.onJobComplete.name
        jobData["OnTaskTimeout"] = self._data.onTaskTimeout.value
        # Job Tasks
        jobData["OverrideTaskExtraInfoNames"] = (
            self._data.taskInfoExtraNameOverrideEnable
        )
        for key, value in self._data.taskInfoExtraNameIndexed.items():
            jobData["TaskExtraInfoName{}".format(key)] = value
        # Job Plugin
        jobData["Plugin"] = self._data.plugin
        for key, value in self._data.pluginInfo.items():
            pluginData[key] = value
        jobData["ForceReloadPlugin"] = self._data.pluginForceReload
        jobData["CustomPluginDirectory"] = self._data.pluginDirectoryCustom
        # Job Event Plugins
        jobData["EventOptIns"] = ",".join(self._data.eventOptIns)
        jobData["SuppressEvents"] = self._data.eventSuppress
        # data["Props"]["EventDir"] = self._data.custom_event_plugin_directory # TODO HINT NotImplemented
        # Job Pre/Post (Task) Scripts
        jobData["PreJobScript"] = self._data.scriptPreJob
        jobData["PostJobScript"] = self._data.scriptPostJob
        jobData["PreTaskScript"] = self._data.scriptPreTask
        jobData["PostTaskScript"] = self._data.scriptPostTask
        # Job Dependencies
        jobData["ResumeOnCompleteDependencies"] = (
            self._data.dependencyResumeOnCompleted
        )
        jobData["ResumeOnDeletedDependencies"] = self._data.dependencyResumeOnDeleted
        jobData["ResumeOnFailedDependencies"] = self._data.dependencyResumeOnFailed
        jobData["JobDependencyPercentage"] = (
            self._data.dependencyResumePendingPercentageValue
        )
        jobData["IsFrameDependent"] = self._data.dependencyFrameEnabled
        jobData["FrameDependencyOffsetStart"] = self._data.dependencyFrameOffsetStart
        jobData["FrameDependencyOffsetEnd"] = self._data.dependencyFrameOffsetEnd
        if self._data.dependencyJobs:
            jobData["JobDependencies"] = ",".join(self._data.dependencyJobs)
        if self._data.dependencyAssets:
            jobData["RequiredAssets"] = self._data.dependencyAssets
        if self._data.dependencyScripts:
            jobData["ScriptDependencies"] = ",".join(
                [script.FileName for script in self._data.dependencyScripts]
            )
        # Job Cleanup
        jobData["OverrideAutoJobCleanup"] = self._data.cleanupAutomaticOverrideEnable
        jobData["OverrideJobCleanupType"] = self._data.cleanupAutomaticType.name
        jobData["OverrideJobCleanup"] = self._data.cleanupOverrideEnable
        jobData["JobCleanupDays"] = self._data.cleanupOverrideDays
        # Job Stats
        if self._data.statsJobSubmissionMachine:
            jobData["MachineName"] = self._data.statsJobSubmissionMachine
        # Job Notifications
        jobData["OverrideNotificationMethod"] = (
            self._data.notificationMethodOverrideEnable
        )
        jobData["NotificationTargets"] = ",".join(self._data.notificationTargets)
        jobData["PopupNotification"] = self._data.notificationPopupEnable
        jobData["EmailNotification"] = self._data.notificationEmailEnable
        jobData["NotificationEmails"] = ",".join(self._data.notificationEmails)
        jobData["NotificationNote"] = self._data.notificationNote
        # Job Maintenance
        jobData["MaintenanceJob"] = self._data.maintenanceJobEnable
        jobData["MaintenanceJobStartFrame"] = self._data.maintenanceJobStartFrame
        jobData["MaintenanceJobEndFrame"] = self._data.maintenanceJobEndFrame
        # Job Time Schedule
        scheduled_type = self._data.scheduledType.name
        scheduled_type = scheduled_type if scheduled_type != "None_" else "None"
        jobData["ScheduledType"] = scheduled_type
        if self._data.scheduledType != JobScheduledType.None_:
            if self._data.scheduledType in [
                JobScheduledType.Once,
                JobScheduledType.Daily,
            ]:
                jobData["ScheduledDays"] = self._data.scheduledDayInterval
                jobData["ScheduledStartDateTime"] = (
                    self._data.scheduledDayTimeStart.record().strftime("%d/%m/%Y %H:%M")
                )
                # # TODO HINT NotImplemented by deadlinecommand
                # if self._data.scheduledDayTimeEnd.valid():
                #     job_data["ScheduledEndDateTime"] = self._data.scheduledDayTimeEnd.record().strftime("%d/%m/%Y %H:%M")
            if self._data.scheduledType == JobScheduledType.Custom:
                if self._data.scheduledDayMondayTimeStart.valid():
                    jobData["ScheduledMondayStartTime"] = (
                        self._data.scheduledDayMondayTimeStart.format()
                    )
                if self._data.scheduledDayMondayTimeEnd.valid():
                    jobData["ScheduledMondayStopTime"] = (
                        self._data.scheduledDayMondayTimeEnd.format()
                    )
                if self._data.scheduledDayTuesdayTimeStart.valid():
                    jobData["ScheduledTuesdayStartTime"] = (
                        self._data.scheduledDayTuesdayTimeStart.format()
                    )
                if self._data.scheduledDayTuesdayTimeEnd.valid():
                    jobData["ScheduledTuesdayStopTime"] = (
                        self._data.scheduledDayTuesdayTimeEnd.format()
                    )
                if self._data.scheduledDayWednesdayTimeStart.valid():
                    jobData["ScheduledWednesdayStartTime"] = (
                        self._data.scheduledDayWednesdayTimeStart.format()
                    )
                if self._data.scheduledDayWednesdayTimeEnd.valid():
                    jobData["ScheduledWednesdayStopTime"] = (
                        self._data.scheduledDayWednesdayTimeEnd.format()
                    )
                if self._data.scheduledDayThursdayTimeStart.valid():
                    jobData["ScheduledThursdayStartTime"] = (
                        self._data.scheduledDayThursdayTimeStart.format()
                    )
                if self._data.scheduledDayThursdayTimeEnd.valid():
                    jobData["ScheduledThursdayStopTime"] = (
                        self._data.scheduledDayThursdayTimeEnd.format()
                    )
                if self._data.scheduledDayFridayTimeStart.valid():
                    jobData["ScheduledFridayStartTime"] = (
                        self._data.scheduledDayFridayTimeStart.format()
                    )
                if self._data.scheduledDayFridayTimeEnd.valid():
                    jobData["ScheduledFridayStopTime"] = (
                        self._data.scheduledDayFridayTimeEnd.format()
                    )
                if self._data.scheduledDaySaturdayTimeStart.valid():
                    jobData["ScheduledSaturdayStartTime"] = (
                        self._data.scheduledDaySaturdayTimeStart.format()
                    )
                if self._data.scheduledDaySaturdayTimeEnd.valid():
                    jobData["ScheduledSaturdayStopTime"] = (
                        self._data.scheduledDaySaturdayTimeEnd.format()
                    )
                if self._data.scheduledDaySundayTimeStart.valid():
                    jobData["ScheduledSundayStartTime"] = (
                        self._data.scheduledDaySundayTimeStart.format()
                    )
                if self._data.scheduledDaySundayTimeEnd.valid():
                    jobData["ScheduledSundayStopTime"] = (
                        self._data.scheduledDaySundayTimeEnd.format()
                    )
        # Job Tile Rendering
        jobData["TileJob"] = self._data.tileEnable
        if self._data.tileEnable:
            jobData["TileJobFrame"] = self._data.tileFrame
            jobData["TileJobTileCount"] = self._data.tileTilesCount
            jobData["TileJobTilesInX"] = self._data.tileTilesInX
            jobData["TileJobTilesInY"] = self._data.tileTilesInY
            output_tile_idx = -1
            for output_tile_file_name in self._data.tileOutputFileNames:
                output_tile_idx += 1
                jobData["OutputFilename{}Tile?".format(output_tile_idx)] = (
                    output_tile_file_name
                )

        return jobData, pluginData, auxFilePaths

    def serializeSubmissionCommandlineFiles(
        self, jobFilePath: str, pluginFilePath: str
    ):
        """Serialize this class to the deadlinecommand submission files.
        Args:
            job_file_path (str): The job submission data file path.
            plugin_file_path (str): The plugin submission data file path.
        Returns:
            list[str]: A list of args to pass to deadlinecommand.

        Returns:
            str: The job data file path.
            str: The plugin data file path.
            list[str]: The list of auxiliary file paths.

        """
        jobData, pluginData, auxFilePaths = self.serializeSubmissionCommandlineDictionaries()

        # Write job submission file
        with open(jobFilePath, "w") as job_file:
            for key, value in sorted(jobData.items()):
                if isinstance(value, bool):
                    value = "true" if value else "false"
                job_file.write("{}={}\n".format(key, value))

        # Write plugin submission file
        with open(pluginFilePath, "w") as plugin_file:
            for key, value in sorted(pluginData.items()):
                if isinstance(bool, value):
                    value = "true" if value else "false"
                plugin_file.write("{}={}\n".format(key, value))

        return jobFilePath, pluginFilePath, auxFilePaths

    #########################################
    # Deadline Scripting API
    # This is a 1:1 Job Class compatibility layer.
    # As we can use this class to construct jobs
    # additional setters have been added.
    # Differences:
    #   JobRepository -> Added Property
    #   JobFrames -> Add property setter
    #   JobFramesList -> Add property setter
    #   JobFramesPerTask -> Add property setter
    #   JobPathMapping -> Added Property
    #   JobOutputDirectories -> Add property setter
    #   JobOutputFileNames -> Add property setter
    #   JobAuxiliarySubmissionFileNames -> Add property setter
    #   JobMachineLimit -> Add property setter
    #   JobMachineLimitProgress -> Add property setter
    #   JobWhitelistFlag -> Add property setter
    #   JobListedSlaves -> Add property setter
    #   JobStatus -> Signature Enum JobStatus
    #             -> Add property setter
    #   JobOnJobComplete -> Signature Enum JobCompleteAction
    #   JobOnTaskTimeout -> Signature Enum TaskOnTimeout
    #   JobSubmitMachine -> Add property setter
    #   JobPreJobScript -> Add property setter 
    #                   -> Adjust doc string
    #   JobPostJobScript -> Add property setter 
    #                    -> Adjust doc string
    #   JobMaintenanceJob -> Add property setter 
    #   JobMaintenanceJobStartFrame -> Add property setter 
    #   JobMaintenanceJobEndFrame -> Add property setter 
    #   JobTileJob -> Add property setter
    #   JobOutputTileFileNames -> Add property setter
    #########################################

    # Job General
    @property
    def JobRepository(self):
        """The job's repository to submit to.
        Args:
            value (str): The repository name.
        Returns:
            str: The repository name.
        """
        return self._data.repository

    @JobRepository.setter
    def JobRepository(self, value: str):
        self._data.repository = value

    @property
    def JobId(self):
        """The job's ID.
        Returns:
            str: The ID.
        """
        return self._data.id

    @property
    def JobName(self):
        """The job's name.
        Args:
            value (str): The job name.
        Returns:
            str: The job name.
        """
        return self._data.name

    @JobName.setter
    def JobName(self, value: str):
        self._data.name = value

    @property
    def JobBatchName(self):
        """The name of the Batch that this job belongs to.
        Args:
            value (str): The job batch name.
        Returns:
            str: The job batch name.
        """
        return self._data.batchName

    @JobBatchName.setter
    def JobBatchName(self, value):
        self._data.batchName = value

    @property
    def JobPriority(self):
        """The job's priority (0 is the lowest).
        Args:
            value (int): The priority.
        Returns:
            int: The priority.
        """
        return self._data.priority

    @JobPriority.setter
    def JobPriority(self, value: int):
        if value > 100:
            LOG.warning("Clamping job priority to the allowed max of 100")
        self._data.priority = value

    @property
    def JobProtected(self):
        """If set to True, the job can only be deleted or
        archived by the job's user, or by someone who has
        permissions to handle protected jobs.
        Args:
            value (bool): The protected state.
        Returns:
            bool: The protected state.
        """
        return self._data.protected

    @JobProtected.setter
    def JobProtected(self, value: bool):
        self._data.protected = value

    @property
    def JobUserName(self):
        """The user that submitted the job.
        Args:
            value (str): The user name.
        Returns:
            str: The user name.
        """
        return self._data.userName

    @JobUserName.setter
    def JobUserName(self, value: str):
        self._data.userName = value

    @property
    def JobDepartment(self):
        """The department to which the job's user belongs to.
        Args:
            value (str): The department name.
        Returns:
            str: The department name.
        """
        return self._data.department

    @JobDepartment.setter
    def JobDepartment(self, value: str):
        self._data.department = value

    @property
    def JobComment(self):
        """A brief comment about the job.
        Args:
            value (str): The comment.
        Returns:
            str: The comment.
        """
        return self._data.comment

    @JobComment.setter
    def JobComment(self, value):
        self._data.comment = value

    @property
    def JobFrames(self):
        """The job's frame list as a string.
        Args:
            value (str): The frame list string. 
        Returns:
            str: The frame list string.
        """
        return FrameList.convertFrameListToFrameString(self._data.frames)

    @JobFrames.setter
    @jobPermissionSubmit
    def JobFrames(self, value: str):
        self._data.frames = FrameList.convertFrameStringToFrameList(value)

    @property
    def JobFramesList(self):
        """The job's frame list as an array.
        Args:
            value (list[int]): The frame list array.
        Returns:
            str: The frame list array.
        """
        return self._data.frames

    @JobFramesList.setter
    @jobPermissionSubmit
    def JobFramesList(self, value):
        self._data.frames = value

    @property
    def JobFramesPerTask(self):
        """The number of frames per task.
        Args:
            value (int): The frames per task.
        Returns:
            int: The frames per task.
        """
        return self._data.framesPerTask

    @JobFramesPerTask.setter
    @jobPermissionSubmit
    def JobFramesPerTask(self, value):
        self._data.framesPerTask = value

    @property
    def JobSequentialJob(self):
        """If the job is a sequential job, which ensures
        its tasks only render in ascending order.
        Args:
            value (bool): The sequential state.
        Returns:
            bool: The sequential state.
        """
        return self._data.framesSequential

    @JobSequentialJob.setter
    def JobSequentialJob(self, value: bool):
        self._data.framesSequential = value

    # Job Environment
    def GetJobEnvironmentKeys(self):
        """Gets the keys for the job's environment variable entries.
        Returns:
            list[str]: A list of keys
        """
        return self._data.environment.keys()

    def GetJobEnvironmentKeyValue(self, key: str):
        """Gets the environment variable value for the given key.
        Args:
            key (str): The env variable name.
        Returns:
            str | None: The value of the env variable.
        """
        return self._data.environment.get(key, None)

    def SetJobEnvironmentKeyValue(self, key: str, value: str):
        """Sets the environment variable value for the given key.
        Args:
            key (str): The env variable name.
            value (str): The env variable value.
        """
        self._data.environment[key] = value

    def DeleteJobEnvironmentKey(self, key: str):
        """Deletes the environment variable for the given key.
        Args:
            key (str): The env variable name.
        """
        self._data.environment.pop(key, None)

    @property
    def JobUseJobSubmissionEnvironment(self):
        """If enabled, on submission the current user's environment
        will be saved into the job's environment.
        Args:
            value (bool): The job env state.
        Returns:
            bool: The job env state.
        """
        return self._data.environmentSubmissionIncludeEnable

    @JobUseJobSubmissionEnvironment.setter
    def JobUseJobSubmissionEnvironment(self, value: bool):
        self._data.environmentSubmissionIncludeEnable = value

    @property
    def JobUseJobEnvironmentOnly(self):
        """If only the job's environment variables should
        be used. If disabled, the job's environment will
        be merged with the current environment.
        Args:
            value (bool): The job env state.
        Returns:
            bool: The job env state.
        """
        return self._data.environmentIsolateEnable

    @JobUseJobEnvironmentOnly.setter
    def JobUseJobEnvironmentOnly(self, value: bool):
        self._data.environmentIsolateEnable = value

    # Job Info
    def GetJobInfoKeys(self):
        """Gets the job info keys.
        Returns:
            list[str]: The job info keys.
        """
        return self._data.info.keys()

    def GetJobInfoKeyValue(self, key: str):
        """Get the job info value for the provided key.
        Args:
            key (str): The key name.
        Returns:
            str | None: The value.
        """
        return self._data.info.get(key, None)

    # Job (Extra) Info
    def GetJobExtraInfoKeys(self):
        """Gets the keys for the job's extra info entries.
        Returns:
            list[str]: The value of the env var.
        """
        return self._data.infoExtra.keys()

    def GetJobExtraInfoKeyValue(self, key: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
        Returns:
            str | None: The value.
        """
        return self._data.infoExtra.get(key, None)

    def GetJobExtraInfoKeyValueWithDefault(self, key: str, defaultValue: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
            defaultValue (str): The fallback value if the key doesn't exist.
        Returns:
            str: The value.
        """
        return self._data.infoExtra.get(key, defaultValue)

    def SetJobExtraInfoKeyValue(self, key: str, value: str):
        """Sets the extra info value for the given key.
        Args:
            key (str): The key name.
            value (str): The value.
        """
        self._data.infoExtra[key] = value

    def DeleteJobExtraInfoKey(self, key: str):
        """Deletes the extra info for the given key.
        Args:
            key (str): The key name.
        """
        self._data.infoExtra.pop(key, None)

    @property
    def JobExtraInfo0(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(0)

    @JobExtraInfo0.setter
    def JobExtraInfo0(self, value: str):
        self._SetJobExtraInfoIndex(0, value)

    @property
    def JobExtraInfo1(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(1)

    @JobExtraInfo1.setter
    def JobExtraInfo1(self, value: str):
        self._SetJobExtraInfoIndex(1, value)

    @property
    def JobExtraInfo2(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(2)

    @JobExtraInfo2.setter
    def JobExtraInfo2(self, value: str):
        self._SetJobExtraInfoIndex(2, value)

    @property
    def JobExtraInfo3(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(3)

    @JobExtraInfo3.setter
    def JobExtraInfo3(self, value: str):
        self._SetJobExtraInfoIndex(3, value)

    @property
    def JobExtraInfo4(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(4)

    @JobExtraInfo4.setter
    def JobExtraInfo4(self, value: str):
        self._SetJobExtraInfoIndex(4, value)

    @property
    def JobExtraInfo5(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(5)

    @JobExtraInfo5.setter
    def JobExtraInfo5(self, value: str):
        self._SetJobExtraInfoIndex(5, value)

    @property
    def JobExtraInfo6(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(6)

    @JobExtraInfo6.setter
    def JobExtraInfo6(self, value: str):
        self._SetJobExtraInfoIndex(6, value)

    @property
    def JobExtraInfo7(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(7)

    @JobExtraInfo7.setter
    def JobExtraInfo7(self, value: str):
        self._SetJobExtraInfoIndex(7, value)

    @property
    def JobExtraInfo8(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(8)

    @JobExtraInfo8.setter
    def JobExtraInfo8(self, value: str):
        self._SetJobExtraInfoIndex(8, value)

    @property
    def JobExtraInfo9(self):
        """One of the Job's ten Extra Info fields.
        Args:
            value (str): The key name.
        Returns:
            str | None: The value.
        """
        self._GetJobExtraInfoIndex(9)

    @JobExtraInfo9.setter
    def JobExtraInfo9(self, value: str):
        self._SetJobExtraInfoIndex(9, value)

    # Job Files
    @property
    def JobPathMapping(self):
        """The path mapping rules for this job.
        Args:
            pathMapping (list[PathMappingRule]): A list of path mapping rules.
        Returns:
            list[PathMappingRule]: A list of path mapping rules.
        """
        return self._data.filePathMapping

    @JobPathMapping.setter
    def JobPathMapping(self, value: list[PathMappingRule]):
        self._data.filePathMapping = value

    @property
    def JobOutputDirectories(self):
        """The list of output directories.
        Args:
            value (list[str]): A list of directory paths.
        Returns:
            list[str]: A list of directory paths.
        """
        return self._data.fileOutputDirectoryPaths

    @JobOutputDirectories.setter
    @jobPermissionSubmit
    def JobOutputDirectories(self, value):
        self._data.fileOutputDirectoryPaths = value

    @property
    def JobOutputFileNames(self):
        """The list of output filenames.
        Args:
            value (list[str]): A list of file names.
        Returns:
            list[str]: A list of file names.
        """
        return self._data.fileOutputFileNames

    @JobOutputFileNames.setter
    @jobPermissionSubmit
    def JobOutputFileNames(self, value):
        self._data.fileOutputFileNames = value

    @property
    def JobAuxiliarySubmissionFileNames(self):
        """The auxiliary files submitted with the job.
        Args:
            value (list[str]): A list of file paths used as auxiliary files.
        Returns:
            list[str]: A list of file paths (pre-submit)/file names (post-submit) used as auxiliary files.
        """
        return self._data.fileAuxiliarySubmissionFileNames

    @JobAuxiliarySubmissionFileNames.setter
    def JobAuxiliarySubmissionFileNames(self, value: list[str]):
        self._data.fileAuxiliarySubmissionFileNames = value

    @property
    def JobSynchronizeAllAuxiliaryFiles(self):
        """If the job's auxiliary files should be
        synced up by the Worker between tasks.
        Args:
            value (bool): The sync state.
        Returns:
            bool: The sync state.
        """
        return self._data.fileAuxiliarySubmissionSyncFileEnable

    @JobSynchronizeAllAuxiliaryFiles.setter
    def JobSynchronizeAllAuxiliaryFiles(self, value: bool):
        self._data.fileAuxiliarySubmissionSyncFileEnable = value

    # Job Limits/Groups/Pools/Machines
    @property
    def JobLimitGroups(self):
        """The limit groups the job requires.
        Returns:
            list[str]:
        """
        return self._data.resourceLimits

    def SetJobLimitGroups(self, limitGroups: list[str]):
        """Sets the limit groups the job requires.
        Args:
            limitGroups (list[int]): The limit groups to set.
        """
        self._data.resourceLimits = limitGroups

    @property
    def JobPool(self):
        """The job's pool.
        Args:
            value (str): The pool name.
        Returns:
            str: The pool name.
        """
        return self._data.machinePool

    @JobPool.setter
    def JobPool(self, value: str):
        self._data.machinePool = value

    @property
    def JobSecondaryPool(self):
        """The Secondary Pool in which this job belongs.
        Args:
            value (str): The secondary pool name.
        Returns:
            str: The secondary pool name.
        """
        return self._data.machineSecondaryPool

    @JobSecondaryPool.setter
    def JobSecondaryPool(self, value: str):
        self._data.machineSecondaryPool = value

    @property
    def JobGroup(self):
        """The job's group.
        Args:
            value (str): The group name.
        Returns:
            str: The group name.
        """
        return self._data.machineGroup

    @JobGroup.setter
    def JobGroup(self, value: str):
        self._data.machineGroup = value

    @property
    def JobMachineLimit(self):
        """The machine limit for the job.
        Args:
            value (int): The machine limit.
        Returns:
            int: The machine limit.
        """
        return self._data.machineLimit

    @JobMachineLimit.setter
    def JobMachineLimit(self, value):
        self._data.machineLimit = value

    @property
    def JobMachineLimitProgress(self):
        """When the Worker reaches this progress for
        the job's task, it will release the limit group.
        Args:
            value (float): The progress percentage.
        Returns:
            float: The progress percentage.
        """
        return self._data.machineLimitProgress

    @JobMachineLimitProgress.setter
    def JobMachineLimitProgress(self, value):
        self._data.machineLimitProgress = value

    @property
    def JobWhitelistFlag(self):
        """If the job's listed Workers are an allow
        list or a deny list.
        Args:
            value (bool): The list mode state.
        Returns:
            bool: The list mode state.
        """
        return self._data.machineListedInclude


    @JobWhitelistFlag.setter
    def JobWhitelistFlag(self, value):
        self._data.machineListedInclude = value


    @property
    def JobListedSlaves(self):
        """The list of Workers in allow or deny list for
        the job. Use JobWhitelistFlag to determine if the
        list is a deny list or an allow list.
        Args:
            value (list[str]): The machine names to white/black list.
        Returns:
            list[str]: The machine names to white/black list.
        """
        return self._data.machineListedNames

    @JobListedSlaves.setter
    def JobListedSlaves(self, value):
        self._data.machineListedNames = value

    @property
    def JobConcurrentTasks(self):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Args:
            value (int): The concurrent task limit.
        Returns:
            int: The concurrent task limit.
        """
        return self._data.taskConcurrencyLimit

    @JobConcurrentTasks.setter
    def JobConcurrentTasks(self, value: int):
        self._data.taskConcurrencyLimit = value

    @property
    def JobLimitTasksToNumberOfCpus(self):
        """Whether or not the number of concurrent tasks
        a Worker can dequeue for this job should be limited
        to the number of CPUs the Worker has.
        Args:
            value (bool): The state.
        Returns:
            bool: The state.
        """
        return self._data.taskConcurrencyLimitToNumberOfCpus

    @JobLimitTasksToNumberOfCpus.setter
    def JobLimitTasksToNumberOfCpus(self, value: bool):
        self._data.taskConcurrencyLimitToNumberOfCpus = value

    # Job State
    @property
    def JobStatus(self):
        """The job's current state.
        Args:
            value (JobStatus): The job state.
        Returns:
            JobStatus: The job state.
        """
        return self._data.status

    @JobStatus.setter
    def JobStatus(self, value: JobStatus):
        self._data.status = value

    @property
    def JobSendJobErrorWarning(self):
        """If the job should send warning notifications when it
        reaches a certain number of errors.
        Args:
            value (bool): The notification enable state.
        Returns:
            bool: The notification enable state.
        """
        return self._data.statusErrorWarningSend

    @JobSendJobErrorWarning.setter
    def JobSendJobErrorWarning(self, value: bool):
        self._data.statusErrorWarningSend = value

    @property
    def JobOverrideJobFailureDetection(self):
        """Whether or not this job overrides the Job
        Failure Detection settings in the Repository Options.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.statusFailureDetectionJobOverrideEnable

    @JobOverrideJobFailureDetection.setter
    def JobOverrideJobFailureDetection(self, value: bool):
        self._data.statusFailureDetectionJobOverrideEnable = value

    @property
    def JobFailureDetectionJobErrors(self):
        """If JobOverrideJobFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a job failure.
        Args:
            value (int): The error max count.
        Returns:
            int: The error max count.
        """
        return self._data.statusFailureDetectionJobErrors

    @JobFailureDetectionJobErrors.setter
    def JobFailureDetectionJobErrors(self, value: int):
        self._data.statusFailureDetectionJobErrors = value

    @property
    def JobOverrideTaskFailureDetection(self):
        """Whether or not this job overrides the Task Failure
        Detection settings in the Repository Options.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.statusFailureDetectionTaskOverrideEnable

    @JobOverrideTaskFailureDetection.setter
    def JobOverrideTaskFailureDetection(self, value: bool):
        self._data.statusFailureDetectionTaskOverrideEnable = value

    @property
    def JobFailureDetectionTaskErrors(self):
        """If JobOverrideTaskFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a task failure.
        Args:
            value (int): The error max count.
        Returns:
            int: The error max count.
        """
        return self._data.statusFailureDetectionTaskErrors

    @JobFailureDetectionTaskErrors.setter
    def JobFailureDetectionTaskErrors(self, value: int):
        self._data.statusFailureDetectionTaskErrors = value

    @property
    def JobIgnoreBadSlaveDetection(self):
        """Whether or not this job overrides the Bad Worker Detection settings in the Repository Options.
        Args:
            value (bool): The ignore state.
        Returns:
            bool: The ignore state.
        """
        return self._data.statusFailureDetectionMachineBadIgnore

    @JobIgnoreBadSlaveDetection.setter
    def JobIgnoreBadSlaveDetection(self, value: bool):
        self._data.statusFailureDetectionMachineBadIgnore = value

    @property
    def JobInterruptible(self):
        """If the job is interruptible, which causes it
        to be canceled when a job with higher priority comes along.
        Args:
            value (bool): The interruptible state.
        Returns:
            bool: The interruptible state.
        """
        return self._data.statusInterruptable

    @JobInterruptible.setter
    def JobInterruptible(self, value: bool):
        self._data.statusInterruptable = value

    @property
    def JobInterruptiblePercentage(self):
        """The completion percentage that this Job must
        be less than in order to be interruptible.
        Args:
            value (int): The interruptible max percentage.
        Returns:
            int: The interruptible max percentage.
        """
        return self._data.statusInterruptablePercentage

    @JobInterruptiblePercentage.setter
    def JobInterruptiblePercentage(self, value: int):
        self._data.statusInterruptablePercentage = value

    @property
    def RemTimeThreshold(self):
        """The remaining time (in seconds) that this Job
        must have left more than in order to be interruptable.
        Args:
            value (int): The remaining time in seconds.
        Returns:
            int: The remaining time in seconds.
        """
        return self._data.statusInterruptableRemainingTimeThreshold

    @RemTimeThreshold.setter
    def RemTimeThreshold(self, value: int):
        self._data.statusInterruptableRemainingTimeThreshold = value

    @property
    def JobStartJobTimeoutSeconds(self):
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int): The job's min task timeout in seconds.
        Returns:
            int: The job's min timeout in seconds.
        """
        return self._data.statusTimeoutJobMinSeconds

    @JobStartJobTimeoutSeconds.setter
    def JobStartJobTimeoutSeconds(self, value: int):
        self._data.statusTimeoutJobMinSeconds = value

    @property
    def JobInitializePluginTimeoutSeconds(self):
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int): The job's min plugin timeout in seconds.
        Returns:
            int: The job's min plugin timeout in seconds.
        """
        return self._data.statusTimeoutPluginInitializeMaxSeconds

    @JobInitializePluginTimeoutSeconds.setter
    def JobInitializePluginTimeoutSeconds(self, value: int):
        self._data.statusTimeoutPluginInitializeMaxSeconds = value

    @property
    def JobMinRenderTimeSeconds(self):
        """The minimum number of seconds a job must run
        to be considered successful.
        Args:
            value (int): The job's min task timeout in seconds.
        Returns:
            int: The job's min task timeout in seconds.
        """
        return self._data.statusTimeoutTaskMinSeconds

    @JobMinRenderTimeSeconds.setter
    def JobMinRenderTimeSeconds(self, value: int):
        self._data.statusTimeoutTaskMinSeconds = value

    @property
    def JobTaskTimeoutSeconds(self):
        """The timespan a job's task has to render before
        a timeout occurs.
        Args:
            value (int): The job's min task timeout in seconds.
        Returns:
            int: The job's min task timeout in seconds.
        """
        return self._data.statusTimeoutTaskMaxSeconds

    @JobTaskTimeoutSeconds.setter
    def JobTaskTimeoutSeconds(self, value: int):
        self._data.statusTimeoutTaskMaxSeconds = value

    @property
    def JobEnableTimeoutsForScriptTasks(self):
        """If the timeouts should apply to pre/post job script tasks.
        Args:
            value (bool): The job's min script timeout in seconds.
        Returns:
            bool: The job's min script timeout in seconds.
        """
        return self._data.statusTimeoutScriptEnable

    @JobEnableTimeoutsForScriptTasks.setter
    def JobEnableTimeoutsForScriptTasks(self, value: bool):
        self._data.statusTimeoutScriptEnable = value

    @property
    def JobEnableAutoTimeout(self):
        """The Auto Task Timeout feature is based on the Auto Job Timeout
        Settings in the Repository Options. The timeout is based on the
        render times of the tasks that have already finished for this job,
        so this option should only be used if the frames for the job have
        consistent render times.
        Args:
            value (bool): The auto timeout state.
        Returns:
            bool: The auto timeout state.
        """
        return self._data.statusTimeoutAutoEnable

    @JobEnableAutoTimeout.setter
    def JobEnableAutoTimeout(self, value: bool):
        self._data.statusTimeoutAutoEnable = value

    @property
    def JobEnableFrameTimeouts(self):
        """If the timeouts are Frame based instead of Task based.
        Args:
            value (bool): The frame-based timeout enable state.
        Returns:
            bool: The frame-based timeout enable state.
        """
        return self._data.statusTimeoutFrameBasedEnable

    @JobEnableFrameTimeouts.setter
    def JobEnableFrameTimeouts(self, value: bool):
        self._data.statusTimeoutFrameBasedEnable = value

    @property
    def JobOnJobComplete(self):
        """What the job should do when it completes.
        The options are "Archive", "Delete", or "Nothing".
        Args:
            value (JobCompleteAction): See enum for possible values.
        Returns:
            JobCompleteAction: The enum value.
        """
        return self._data.onJobComplete

    @JobOnJobComplete.setter
    def JobOnJobComplete(self, value: str):
        self._data.onJobComplete = JobCompleteAction(value)

    @property
    def JobOnTaskTimeout(self):
        """What to do when a task times out.
        The options are "Error", "Notify", or "Both".
        Args:
            value (TaskOnTimeout): See enum for possible values.
        Returns:
            TaskOnTimeout: The enum value.
        """
        return self._data.onTaskTimeout

    @JobOnTaskTimeout.setter
    def JobOnTaskTimeout(self, value: TaskOnTimeout):
        self._data.onTaskTimeout = value

    # Job Tasks
    @property
    def JobOverrideTaskExtraInfoNames(self):
        """Whether this job overrides the task extra info names.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.taskInfoExtraNameOverrideEnable

    @JobOverrideTaskExtraInfoNames.setter
    def JobOverrideTaskExtraInfoNames(self, value: bool):
        self._data.taskInfoExtraNameOverrideEnable = value

    @property
    def JobTaskExtraInfoName0(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(0)

    @JobTaskExtraInfoName0.setter
    def JobTaskExtraInfoName0(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(0, value)

    @property
    def JobTaskExtraInfoName1(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(1)

    @JobTaskExtraInfoName1.setter
    def JobTaskExtraInfoName1(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(1, value)

    @property
    def JobTaskExtraInfoName2(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(2)

    @JobTaskExtraInfoName2.setter
    def JobTaskExtraInfoName2(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(2, value)

    @property
    def JobTaskExtraInfoName3(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(3)

    @JobTaskExtraInfoName3.setter
    def JobTaskExtraInfoName3(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(3, value)

    @property
    def JobTaskExtraInfoName4(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(4)

    @JobTaskExtraInfoName4.setter
    def JobTaskExtraInfoName4(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(4, value)

    @property
    def JobTaskExtraInfoName5(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(5)

    @JobTaskExtraInfoName5.setter
    def JobTaskExtraInfoName5(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(5, value)

    @property
    def JobTaskExtraInfoName6(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(6)

    @JobTaskExtraInfoName6.setter
    def JobTaskExtraInfoName6(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(6, value)

    @property
    def JobTaskExtraInfoName7(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(7)

    @JobTaskExtraInfoName7.setter
    def JobTaskExtraInfoName7(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(7, value)

    @property
    def JobTaskExtraInfoName8(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(8)

    @JobTaskExtraInfoName8.setter
    def JobTaskExtraInfoName8(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(8, value)

    @property
    def JobTaskExtraInfoName9(self):
        """One of the Task's ten Extra Info names.
        Args:
            value (str): The extra info name.
        Returns:
            str: The extra info name.
        """
        return self._GetJobTaskExtraInfoNameIndex(9)

    @JobTaskExtraInfoName9.setter
    def JobTaskExtraInfoName9(self, value: str):
        self._SetJobTaskExtraInfoNameIndex(9, value)

    # Job Plugin
    @property
    def JobPlugin(self):
        """The name of the Deadline plugin the job uses.
        Args:
            value (str): The plugin name.
        Returns:
            str: The plugin name.
        """
        return self._data.plugin

    @JobPlugin.setter
    def JobPlugin(self, value: str):
        self._data.plugin = value

    def GetJobPluginInfoKeys(self):
        """Gets the keys for the job's plugin info entries.
        Returns:
            list[str]: The value of the env var.
        """
        return self._data.pluginInfo.keys()

    def GetJobPluginInfoKeyValue(self, key: str):
        """Gets the plugin info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """
        return self._data.pluginInfo.get(key, None)

    def SetJobPluginInfoKeyValue(self, key: str, value: str):
        """Sets the plugin info value for the given key.
        Args:
            key (str):
            value (str):
        """
        self._data.pluginInfo[key] = value

    @property
    def JobForceReloadPlugin(self):
        """Whether or not the job's plugin should be
        reloaded between tasks.
        Args:
            value (bool): The force reload state.
        Returns:
            bool: The force reload state.
        """
        return self._data.pluginForceReload

    @JobForceReloadPlugin.setter
    def JobForceReloadPlugin(self, value: bool):
        self._data.pluginForceReload = value

    @property
    def JobCustomPluginDirectory(self):
        """A custom location to load the job's plugin from.
        Args:
            value (str): The custom plugin directory path.
        Returns:
            str: The custom plugin directory path.
        """
        return self._data.pluginDirectoryCustom

    @JobCustomPluginDirectory.setter
    def JobCustomPluginDirectory(self, value: str):
        self._data.pluginDirectoryCustom = value

    # Job Event Plugins
    @property
    def JobSuppressEvents(self):
        """Whether or not this Job should suppress Events plugins.
        Args:
            value (bool): The suppress state.
        Returns:
            bool: The suppress state.
        """
        return self._data.eventSuppress

    @JobSuppressEvents.setter
    def JobSuppressEvents(self, value: bool):
        self._data.eventSuppress = value

    @property
    def JobCustomEventPluginDirectory(self):
        """A custom location to load the job's event plugin from.
        Args:
            value (str): The custom event plugin directory path.
        Returns:
            str: The custom event plugin directory path.
        """
        return self._data.eventDirectoryCustom

    @JobCustomEventPluginDirectory.setter
    def JobCustomEventPluginDirectory(self, value: str):
        self._data.eventDirectoryCustom = value

    # Job Pre/Post (Task) Scripts
    @property
    def JobPreJobScript(self):
        """The script to execute before the job starts.
        > Originals docs: Read Only. Use RepositoryUtils.SetPreJobScript and RepositoryUtils.DeletePreJobScript.
        Args:
            value (str): The job pre script file path.
        Returns:
            str: The job pre script file path.
        """
        return self._data.scriptPreJob

    @JobPreJobScript.setter
    def JobPreJobScript(self, value):
        self._data.scriptPreJob = value

    @property
    def JobPostJobScript(self):
        """The script to execute after the Job finishes. 
        > Originals docs: Read Only. Use RepositoryUtils.SetPostJobScript and RepositoryUtils.DeletePostJobScript.
        Args:
            value (str): The job post script file path.
        Returns:
            str: The job post script file path.
        """
        return self._data.scriptPostJob

    @JobPostJobScript.setter
    def JobPostJobScript(self, value):
        self._data.scriptPostJob = value

    @property
    def JobPreTaskScript(self):
        """The script to execute before a job task starts.
        Args:
            value (str): The task pre script file path.
        Returns:
            str: The task pre script file path.
        """
        return self._data.scriptPreTask

    @JobPreTaskScript.setter
    def JobPreTaskScript(self, value: str):
        self._data.scriptPreTask = value

    @property
    def JobPostTaskScript(self):
        """The script to execute when a job task is complete.
        Args:
            value (str): The task post script file path.
        Returns:
            str: The task post script file path.
        """
        return self._data.scriptPostTask

    @JobPostTaskScript.setter
    def JobPostTaskScript(self, value: str):
        self._data.scriptPostTask = value

    # Job Dependencies
    @property
    def JobResumeOnCompleteDependencies(self):
        """If the job should resume on complete dependencies.
        Args:
            value (bool): The resume state.
        Returns:
            bool: The resume state.
        """
        return self._data.dependencyResumeOnCompleted

    @JobResumeOnCompleteDependencies.setter
    def JobResumeOnCompleteDependencies(self, value: bool):
        self._data.dependencyResumeOnCompleted = value

    @property
    def JobResumeOnDeletedDependencies(self):
        """If the job should resume on deleted dependencies.
        Args:
            value (bool): The resume state.
        Returns:
            bool: The resume state.
        """
        return self._data.dependencyResumeOnDeleted

    @JobResumeOnDeletedDependencies.setter
    def JobResumeOnDeletedDependencies(self, value: bool):
        self._data.dependencyResumeOnDeleted = value

    @property
    def JobResumeOnFailedDependencies(self):
        """If the job should resume on failed dependencies.
        Args:
            value (bool): The resume state.
        Returns:
            bool: The resume state.
        """
        return self._data.dependencyResumeOnFailed

    @JobResumeOnFailedDependencies.setter
    def JobResumeOnFailedDependencies(self, value: bool):
        self._data.dependencyResumeOnFailed = value

    @property
    def JobDependencyPercentageValue(self):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Args:
            value (float): The percentage when dependencies can already resume.
        Returns:
            float: The percentage when dependencies can already resume.
        """
        return self._data.dependencyResumePendingPercentageValue

    @JobDependencyPercentageValue.setter
    def JobDependencyPercentageValue(self, value: float):
        self._data.dependencyResumePendingPercentageValue = value

    @property
    def JobIsFrameDependent(self):
        """If the job is frame dependent.
        Args:
            value (bool): The frame dependent state.
        Returns:
            bool: The frame dependent state.
        """
        return self._data.dependencyFrameEnabled

    @JobIsFrameDependent.setter
    def JobIsFrameDependent(self, value: bool):
        self._data.dependencyFrameEnabled = value

    @property
    def JobFrameDependencyOffsetStart(self):
        """The start offset for frame dependencies.
        Args:
            value (int): The start offset.
        Returns:
            int: The start offset.
        """
        return self._data.dependencyFrameOffsetStart

    @JobFrameDependencyOffsetStart.setter
    def JobFrameDependencyOffsetStart(self, value: int):
        self._data.dependencyFrameOffsetStart = value

    @property
    def JobFrameDependencyOffsetEnd(self):
        """The end offset for frame depenencies.
        Args:
            value (int): The end offset.
        Returns:
            int: The end offset.
        """
        return self._data.dependencyFrameOffsetEnd

    @JobFrameDependencyOffsetEnd.setter
    def JobFrameDependencyOffsetEnd(self, value: int):
        self._data.dependencyFrameOffsetEnd = value

    @property
    def JobDependencyIDs(self):
        """The ids of the jobs that this job is dependent on.
        Returns:
            list[str]: The dependant job ids.
        """
        return self._data.dependencyJobs

    def SetJobDependencyIDs(self, jobIds: list[int]):
        """Sets the IDs of the jobs that this job is dependent on.
        Args:
            jobIds (list[int]): The dependant job ids.
        """
        self._data.dependencyJobs = jobIds

    @property
    def JobRequiredAssets(self):
        """The assets that are required in order to render this job.
        The assets should contain absolute paths. More...
        Returns:
            list[AssetDependency]: The asset dependencies.
        """
        return self._data.dependencyAssets

    def SetJobRequiredAssets(self, assets: list[AssetDependency]):
        """Sets the assets that are required in order to render this job. The assets should contain absolute paths.
        Args:
            assets (list[Asset]): The asset dependencies.
        """
        self._data.dependencyAssets = assets

    @property
    def JobScriptDependencies(self):
        """The scripts that must return True in order to render this job.
        Returns:
            list[ScriptDependency]: The script dependencies.
        """
        return self._data.dependencyScripts

    def SetScriptDependencies(self, scripts: list[ScriptDependency]):
        """Sets the scripts that must return True in order to render this job.
        Args:
            scripts (list[Script]): The script dependencies.
        """
        self._data.dependencyScripts = scripts

    # Job Cleanup
    @property
    def JobOverrideAutoJobCleanup(self):
        """If the job overrides the automatic job cleanup
        in the Repository Options.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.cleanupAutomaticOverrideEnable

    @JobOverrideAutoJobCleanup.setter
    def JobOverrideAutoJobCleanup(self, value: bool):
        self._data.cleanupAutomaticOverrideEnable = value

    @property
    def AutoJobCleanupType(self):
        """The job cleanup mode. Only relevant if
        the override is set.
        Args:
            value (AutoJobCleanupType): See enum for possible values.
        Returns:
            AutoJobCleanupType: The enum value.
        """
        return self._data.cleanupAutomaticType

    @AutoJobCleanupType.setter
    def AutoJobCleanupType(self, value: AutoJobCleanupType):
        self._data.cleanupAutomaticType = value

    @property
    def JobOverrideJobCleanup(self):
        """If the job overrides the amount of days
        before its cleaned up.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.cleanupOverrideEnable

    @JobOverrideJobCleanup.setter
    def JobOverrideJobCleanup(self, value: bool):
        self._data.cleanupOverrideEnable = value

    @property
    def JobOverrideJobCleanupDays(self):
        """The number of days before this job will be
        cleaned up after it is completed. Only relevant
        if the override is set.
        Args:
            value (int): The amount of days.
        Returns:
            int: The amount of days.
        """
        return self._data.cleanupOverrideDays

    @JobOverrideJobCleanupDays.setter
    def JobOverrideJobCleanupDays(self, value: int):
        self._data.cleanupOverrideDays = value

    # Job Stats
    @property
    def JobSubmitMachine(self):
        """This is the machine that the job was submitted from.
        Args:
            value (str): The submission machine name.
        Returns:
            str: The submission machine name.
        """
        return self._data.statsJobSubmissionMachine

    @JobSubmitMachine.setter
    def JobSubmitMachine(self):
        return self._data.statsJobSubmissionMachine

    @property
    def JobSubmitDateTime(self):
        """The date/time at which the job was submitted.
        Returns:
            DateTime: The submit date time.
        """
        return self._data.statsJobSubmissionDateTime

    @property
    def JobStartedDateTime(self):
        """The date/time at which the job started rendering.
        Returns:
            DateTime: The start date time.
        """
        return self._data.statsJobStartedDateTime

    @property
    def JobCompletedDateTime(self):
        """The date/time at which the job finished rendering.
        Returns:
            DateTime: The end date time.
        """
        return self._data.statsJobCompletedDateTime

    @property
    def JobTaskCount(self):
        """The number of tasks the job has.
        Returns:
            int: The task count.
        """
        # When the job is not on the farm, calculate the
        # task count.
        if self._data.statsTasksCount == -1:
            return len(self.JobFramesList)
        return self._data.statsTasksCount

    @property
    def JobQueuedTasks(self):
        """The number of tasks in the queued state.
        Returns:
            int: The queued task count.
        """
        return self._data.statsTasksQueued

    @property
    def JobRenderingTasks(self):
        """The number of tasks in the active state.
        Returns:
            int: The active task count.
        """
        return self._data.statsTasksRendering

    @property
    def JobPendingTasks(self):
        """The number of tasks in the pending state.
        Returns:
            int: The pending task count.
        """
        return self._data.statsTasksPending

    @property
    def JobCompletedTasks(self):
        """The number of tasks in the completed state.
        Returns:
            int: The completed task count.
        """
        return self._data.statsTasksCompleted

    @property
    def JobSuspendedTasks(self):
        """The number of tasks in the suspended state.
        Returns:
            int: The suspended task count.
        """
        return self._data.statsTasksSuspended

    @property
    def JobFailedTasks(self):
        """The number of tasks in the failed state.
        Returns:
            int: The failed task count.
        """
        return self._data.statsTasksFailed

    # Job Notifications
    @property
    def JobOverrideNotificationMethod(self):
        """If the user's notification method should be ignored.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.notificationMethodOverrideEnable

    @JobOverrideNotificationMethod.setter
    def JobOverrideNotificationMethod(self, value: bool):
        self._data.notificationMethodOverrideEnable = value

    @property
    def JobNotificationTargets(self):
        """The list of users that are to be
        notified when this job is complete.
        Returns:
            list[str]: The users to notify.
        """
        return self._data.notificationTargets

    def SetJobNotificationTargets(self, userNames: list[str]):
        """Sets the list of users that are to be notified when this job is complete.
        Args:
            userNames (list[str]): The users to notify.
        """
        self._data.notificationTargets = userNames

    @property
    def JobPopupNotification(self):
        """If overriding the user's notification method,
        whether to use send a popup notification.
        Args:
            value (bool): The popup show state.
        Returns:
            bool: The popup show state.
        """
        return self._data.notificationPopupEnable

    @JobPopupNotification.setter
    def JobPopupNotification(self, value: bool):
        self._data.notificationPopupEnable = value

    @property
    def JobEmailNotification(self):
        """If overriding the user's notification method, whether to use email notification.
        Args:
            value (bool): The override state.
        Returns:
            bool: The override state.
        """
        return self._data.notificationEmailEnable

    @JobEmailNotification.setter
    def JobEmailNotification(self, value: bool):
        self._data.notificationEmailEnable = value

    @property
    def JobNotificationEmails(self):
        """Arbitrary email addresses to send notifications
        to when this job is complete.
        Returns:
            list[str]: The email addresses to notify.
        """
        return self._data.notificationEmails

    def SetJobNotificationEmails(self, emails: list[str]):
        """Sets the arbitrary email addresses to send notifications to when this job is complete.
        Args:
            jobIds (list[int]): The email addresses to notify.
        """
        self._data.notificationEmails = emails

    @property
    def JobNotificationNote(self):
        """A note to append to the notification email
        sent out when the job is complete.
        Args:
            value (str): The note.
        Returns:
            str: The note.
        """
        return self._data.notificationNote

    @JobNotificationNote.setter
    def JobNotificationNote(self, value: str):
        self._data.notificationNote = value

    # Job Maintenance
    @property
    def JobMaintenanceJob(self):
        """If this is a maintenance job.
        Args:
            value (bool): The maintenance state.
        Returns:
            bool: The maintenance state.
        """
        return self._data.maintenanceJobEnable

    @JobMaintenanceJob.setter
    def JobMaintenanceJob(self, value):
        self._data.maintenanceJobEnable = value

    @property
    def JobMaintenanceJobStartFrame(self):
        """The start frame for a maintenance job.
        Args:
            value (int): The frame.
        Returns:
            int: The frame.
        """
        return self._data.maintenanceJobStartFrame

    @JobMaintenanceJobStartFrame.setter
    def JobMaintenanceJobStartFrame(self, value):
        self._data.maintenanceJobStartFrame = value

    @property
    def JobMaintenanceJobEndFrame(self):
        """The end frame for a maintenance job.
        Args:
            value (int): The frame.
        Returns:
            int: The frame.
        """
        return self._data.maintenanceJobEndFrame

    @JobMaintenanceJobEndFrame.setter
    def JobMaintenanceJobEndFrame(self, value):
        self._data.maintenanceJobEndFrame = value

    # Job Time Schedule
    @property
    def JobScheduledType(self):
        """The scheduling mode for this job.
        The options are "None", "Once", "Daily". or "Custom".
        Args:
            value (str): See enum for possible values.
        Returns:
            str: The enum value.
        """
        return self._data.scheduledType

    @JobScheduledType.setter
    def JobScheduledType(self, value: JobScheduledType):
        self._data.scheduledType = JobScheduledType(value)

    @property
    def JobScheduledDays(self):
        """The day interval for daily scheduled jobs.
        Args:
            value (int): The interval.
        Returns:
            int: The interval.
        """
        return self._data.scheduledDayInterval

    @JobScheduledDays.setter
    def JobScheduledDays(self, value: int):
        self._data.scheduledDayInterval = value

    @property
    def JobScheduledStartDateTime(self):
        """The start date/time at which the scheduled job should start.
        Args:
            value (DateTime): The date time.
        Returns:
            DateTime: The date time.
        """
        return self._data.scheduledDayTimeStart

    @JobScheduledStartDateTime.setter
    def JobScheduledStartDateTime(self, value: DateTime):
        self._data.scheduledDayTimeStart = value

    @property
    def JobScheduledStopDateTime(self):
        """The stop date/time at which the job should stop if it's still active.
        Args:
            value (DateTime): The date time.
        Returns:
            DateTime: The date time.
        """
        return self._data.scheduledDayTimeEnd

    @JobScheduledStopDateTime.setter
    def JobScheduledStopDateTime(self, value: DateTime):
        self._data.scheduledDayTimeEnd = value

    @property
    def DisabledScheduleTime(self):
        """Represents a disabled scheduled time for custom job scheduling settings.
        Returns:
            TimeSpan: Defaults to TimeSpan.MinValue
        """
        return self._data.scheduledDayTimeDisabled

    @property
    def JobMondayStartTime(self):
        """Gets or sets Monday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayMondayTimeStart

    @JobMondayStartTime.setter
    def JobMondayStartTime(self, value: TimeSpan):
        self._data.scheduledDayMondayTimeStart = value

    @property
    def JobMondayStopTime(self):
        """Gets or sets Monday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayMondayTimeEnd

    @JobMondayStopTime.setter
    def JobMondayStopTime(self, value: TimeSpan):
        self._data.scheduledDayMondayTimeEnd = value

    @property
    def JobTuesdayStartTime(self):
        """Gets or sets Tuesday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayTuesdayTimeStart

    @JobTuesdayStartTime.setter
    def JobTuesdayStartTime(self, value: TimeSpan):
        self._data.scheduledDayTuesdayTimeStart = value

    @property
    def JobTuesdayStopTime(self):
        """Gets or sets Tuesday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayTuesdayTimeEnd

    @JobTuesdayStopTime.setter
    def JobTuesdayStopTime(self, value: TimeSpan):
        self._data.scheduledDayTuesdayTimeEnd = value

    @property
    def JobWednesdayStartTime(self):
        """Gets or sets Wednesday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayWednesdayTimeStart

    @JobWednesdayStartTime.setter
    def JobWednesdayStartTime(self, value: TimeSpan):
        self._data.scheduledDayWednesdayTimeStart = value

    @property
    def JobWednesdayStopTime(self):
        """Gets or sets Wednesday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayWednesdayTimeEnd

    @JobWednesdayStopTime.setter
    def JobWednesdayStopTime(self, value: TimeSpan):
        self._data.scheduledDayWednesdayTimeEnd = value

    @property
    def JobThursdayStartTime(self):
        """Gets or sets Thursday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayThursdayTimeStart

    @JobThursdayStartTime.setter
    def JobThursdayStartTime(self, value: TimeSpan):
        self._data.scheduledDayThursdayTimeStart = value

    @property
    def JobThursdayStopTime(self):
        """Gets or sets Thursday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayThursdayTimeEnd

    @JobThursdayStartTime.setter
    def JobThursdayStopTime(self, value: TimeSpan):
        self._data.scheduledDayThursdayTimeEnd = value

    @property
    def JobFridayStartTime(self):
        """Gets or sets Friday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayFridayTimeStart

    @JobFridayStartTime.setter
    def JobFridayStartTime(self, value: TimeSpan):
        self._data.scheduledDayFridayTimeStart = value

    @property
    def JobFridayStopTime(self):
        """Gets or sets Friday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDayFridayTimeEnd

    @JobFridayStopTime.setter
    def JobFridayStopTime(self, value: TimeSpan):
        self._data.scheduledDayFridayTimeEnd = value

    @property
    def JobSaturdayStartTime(self):
        """Gets or sets Saturday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDaySaturdayTimeStart

    @JobSaturdayStartTime.setter
    def JobSaturdayStartTime(self, value: TimeSpan):
        self._data.scheduledDaySaturdayTimeStart = value

    @property
    def JobSaturdayStopTime(self):
        """Gets or sets Saturday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDaySaturdayTimeEnd

    @JobSaturdayStopTime.setter
    def JobSaturdayStopTime(self, value: TimeSpan):
        self._data.scheduledDaySaturdayTimeEnd = value

    @property
    def JobSundayStartTime(self):
        """Gets or sets Sunday's start time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDaySundayTimeStart

    @JobSundayStartTime.setter
    def JobSundayStartTime(self, value: TimeSpan):
        self._data.scheduledDaySundayTimeStart = value

    @property
    def JobSundayStopTime(self):
        """Gets or sets Sunday's stop time.
        Args:
            value (TimeSpan): The time.
        Returns:
            TimeSpan: The time.
        """
        return self._data.scheduledDaySundayTimeEnd

    @JobSundayStopTime.setter
    def JobSundayStopTime(self, value: TimeSpan):
        self._data.scheduledDaySundayTimeEnd = value

    # Job Tile Rendering
    @property
    def JobTileJob(self):
        """If this job is a tile job.
        Args:
            value (bool): The state.
        Returns:
            bool: The state.
        """
        return self._data.tileEnable

    @JobTileJob.setter
    def JobTileJob(self, value):
        self._data.tileEnable = value

    @property
    def JobTileJobFrame(self):
        """The frame that the tile job is rendering.
        Returns:
            int: The frame.
        """
        return self._data.tileFrame

    @property
    def JobOutputTileFileNames(self):
        """The list of output filenames for tile jobs.
        Args:
            value (list[str]): The output file names.
        Returns:
            list[str]: The output file names.
        """
        self._data.tileOutputFileNames = []

    @JobOutputTileFileNames.setter
    def JobOutputTileFileNames(self, value: list[str]):
        self._data.tileOutputFileNames = []

    @property
    def JobTileJobTileCount(self):
        """The number of tiles in a tile job.
        Returns:
            int: The tile count.
        """
        return self._data.tileTilesCount

    @property
    def JobTileJobTilesInX(self):
        """The number of tiles in X for a tile job.
        This is deprecated, and is only here for backwards
        compatibility.
        Returns:
            int: The number of tiles in x.
        """
        raise DeprecationWarning

    @property
    def JobTileJobTilesInY(self):
        """The number of tiles in Y for a tile job.
        This is deprecated, and is only here for backwards compatibility.
        Returns:
            int: The number of tiles in y.
        """
        raise DeprecationWarning
