from __future__ import annotations
import enum
import copy
from dataclasses import dataclass
from datetime import datetime
import getpass
import re
#########################################
# Deadline Scripting API
# This is a 1:1 Jobs Enum compatibility layer.
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

class Asset():
    pass

@dataclass
class Script():
    FileName: str
    Notes: str
    IgnoreFrameOffsets: bool
          
class DateTime(datetime):
    pass

class TimeSpan():
    pass


class FrameList():
    @staticmethod
    def convertFrameListToFrameString(frameList):
        """Convert the frame list into a frame string.
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
                            frameString.append("{}-{}x{}".format(frameStack[0], frameStack[-2], framePreviousInterval))
                        else:
                            frameString.append("{}-{}x{}".format(frameStack[0], frameStack[-1], framePreviousInterval))
                    else:
                        frameString.extend([str(f) for f in frameStack[:-1]])
                        frameString.append(str(frameStack[-1]))
                else:
                    if frameIter != len(frameList):
                        frameString.append("{}-{}".format(frameStack[0], frameStack[-2]))
                    else:
                        frameString.append("{}-{}".format(frameStack[0], frameStack[-1]))
            else:
                frameString.extend([str(f) for f in frameStack[:-1]])
            frameStack = frameStack[-1:]
            frameIntervals.clear()
            framePreviousInterval = -1
        return ",".join(frameString)
    
    @staticmethod
    def convertFrameStringToFrameList(frameStr):
        """Convert the frame list into a frame string.
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
                frameList.extend(range(int(frameStart), int(frameEnd)+1, int(frameStep)))
            elif frameItem.count("-") == 1 and (frameItem.count(":") == 1 or frameItem.count("x") == 1):
                frameRange, frameStep = re.split(":|x", frameItem)
                frameStart, frameEnd = frameRange.split("-")
                if frameEnd < frameStart:
                    frameRange = reversed(range(int(frameEnd), int(frameStart)+1, int(frameStep)))
                else:
                    frameRange = range(int(frameStart), int(frameEnd)+1, int(frameStep))
                frameList.extend(frameRange)
            elif frameItem.count("-") == 1:
                frameStart, frameEnd = frameItem.split("-")
                if frameEnd < frameStart:
                    frameRange = reversed(range(int(frameEnd), int(frameStart)+1))
                else:
                    frameRange = range(int(frameStart), int(frameEnd)+1)
                frameList.extend(frameRange)
            else:
                frameList.append(int(frameItem))

        return frameList
    

#########################################
# Deadline Scripting API
# This is a 1:1 Job Class compatibility layer.
#########################################

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

        # Job General
        self.id = ""
        self.name = "JobName"
        self.batchName = "JobBatchName"
        self.priority = 0
        self.protected = False
        self.userName = getpass.getuser()
        self.department = "pipeline"
        self.comment = ""
        self.frames = []
        self.frames_per_task = 1
        self.sequential = False
        self.onJobComplete = JobCompleteAction.Nothing
        # Job Environment
        self.env = {}
        self.useJobEnvironmentOnly = False
        # Job Info
        self.info = {}
        self.extraInfo = {}
        self.extraInfoIndexed = {idx: "" for idx in range(0,10)}
        # Job Files
        self.outputDirectories = []
        self.outputFileNames = []
        self.auxiliarySubmissionFileNames = []
        self.auxiliarySyncAllFiles = False
        self.network_root = ""
        # Job Limits/Groups/Pools/Machines
        self.pool = ""
        self.secondary_pool = ""
        self.group = ""
        self.limitGroups = []
        self.whitelistFlag = False
        self.listedSlaves = []
        self.machineLimit = 0
        self.machineLimitProgress = 100.0
        self.remainingTimeThreshold = 0
        # Job State
        self.status = JobStatus.Unknown
        self.sendJobErrorWarning = False
        self.overrideJobFailureDetection = False
        self.failureDetectionJobErrors = 0
        self.interruptable = False
        self.interruptablePercentage = 100
        self.minRenderTimeSeconds = 0
        self.enableAutoTimeout = False
        self.enableFrameTimeouts = False
        self.failureDetectionTaskErrors = 0
        self.ignore_bad_slave_detection = False
        self.override_task_failure_detection = False
        self.start_job_timeout_seconds = 0
        self.initialize_plugin_timeout_seconds = 0
        self.task_timeout_seconds = 0
        self.on_task_timeout = TaskOnTimeout.Error
        # Job Tasks
        self.concurrent_tasks = 10
        self.limit_tasks_to_number_of_cpus = True
        self.override_task_extra_info_names = False
        self.taskExtraInfoNameIndex = {idx: "" for idx in range(0,10)}
        self.plugin = ""
        self.plugin_info = {}
        self.force_reload_plugin = False
        self.custom_plugin_directory = ""
        # Job Event Plugins
        self.event_opt_ins = []
        self.suppress_events = False
        self.custom_event_plugin_directory = ""
        # Job Pre/Post (Task) Scripts
        self.pre_job_script = ""
        self.post_job_script = ""
        self.pre_task_script = ""
        self.post_task_script = ""
        self.enable_script_tasks_timeouts = True
        # Job Dependencies
        self.resume_on_complete_dependencies = True
        self.resume_on_deleted_dependencies = False
        self.resume_on_failed_dependencies = False
        self.dependency_percentage_value = 100.0
        self.is_frame_dependent = True
        self.frame_dependency_offset_start = 0
        self.frame_dependency_offset_end = 0
        self.dependency_ids = []
        self.required_assets = []
        self.script_dependencies = []
        # Job Cleanup
        self.override_auto_job_cleanup = False
        self.auto_job_cleanup_type = AutoJobCleanupType.DeleteJobs
        self.override_job_cleanup = False
        self.override_job_cleanup_days = 0
        # Job Stats
        self.submit_date_time = None
        self.submit_machine = ""
        self.started_date_time = None
        self.completed_date_time = None
        self.task_count = -1
        self.queued_tasks = -1
        self.rendering_tasks = -1
        self.pending_tasks = -1
        self.completed_tasks = -1
        self.suspended_tasks = -1
        self.failed_tasks = -1
        # Job Notifications
        self.override_notification_method = False
        self.notification_targets = []
        self.email_notification = False
        self.notification_emails = []
        self.notification_note = ""
        self.notification_popup = False
        # Job Maintenance
        self.maintenance_job = False
        self.maintenance_job_start_frame = 0
        self.maintenance_job_end_frame = 0
        # Job Time Schedule
        self.scheduled_type = JobScheduledType.None_
        self.scheduled_days = 3
        self.scheduled_start_date_time = None
        self.scheduled_end_date_time = None
        self.disabled_schedule_time = None
        self.scheduled_day_monday_start_time_span = None
        self.scheduled_day_monday_end_time_span = None
        self.scheduled_day_tuesday_start_time_span = None
        self.scheduled_day_tuesday_end_time_span = None
        self.scheduled_day_wednesday_start_time_span = None
        self.scheduled_day_wednesday_end_time_span = None
        self.scheduled_day_thursday_start_time_span = None
        self.scheduled_day_thursday_end_time_span = None
        self.scheduled_day_friday_start_time_span = None
        self.scheduled_day_friday_end_time_span = None
        self.scheduled_day_saturday_start_time_span = None
        self.scheduled_day_saturday_end_time_span = None
        self.scheduled_day_sunday_start_time_span = None
        self.scheduled_day_sunday_end_time_span = None
        # Job Tile Rendering
        self.tile_job = False
        self.tile_job_frame = -1
        self.tile_job_tile_count = -1
        self.output_tile_file_names = []
        self.tile_job_tiles_in_x = 0
        self.tile_job_tiles_in_y = 0

    def resetChangeTracker(self):
        self._changeSet.clear()

class Job(object):
    def __init__(self) -> None:
        self._data = JobInternalData()
        self._unknownData = {}
    #########################################
    # Private
    #########################################

    def _GetJobExtraInfoIndex(self, idx: int):
        return self._data.extraInfoIndexed.get(idx, None)

    def _SetJobExtraInfoIndex(self, idx: int, value: str):
        if value is None:
            self._data.extraInfoIndexed.pop(idx, None)
        else:
            self._data.extraInfoIndexed[idx] = value

    def _GetJobTaskExtraInfoNameIndex(self, idx: int):
        return self._data.taskExtraInfoNameIndex.get(idx, None)

    def _SetJobTaskExtraInfoNameIndex(self, idx: int, value: str):
        if value is None:
            self._data.taskExtraInfoNameIndex.pop(idx, None)
        else:
            self._data.taskExtraInfoNameIndex[idx] = value

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
        self._data.frames = data["Props"]["Frames"]
        self._data.frames_per_task = data["Props"]["Chunk"]
        self._data.sequential = data["Props"]["Seq"]
        self._data.onJobComplete = JobCompleteAction(data["Props"]["OnComp"])
        # Job Environment
        self._data.env = data["Props"]["Env"]
        self._data.useJobEnvironmentOnly = data["Props"]["EnvOnly"]
        # Job Info
        self._data.info = None #TODO
        self._data.extraInfo = data["Props"]["ExDic"]
        self._data.extraInfoIndexed = {
            idx: data["Props"]["Ex{}".format(idx)] for idx in range(0,10)
        }
        # Job Files
        self._data.outputDirectories = data["OutDir"]
        self._data.outputFileNames = data["OutFile"]
        self._data.auxiliarySubmissionFileNames = data["Aux"]
        self._data.auxiliarySyncAllFiles = data["Props"]["AuxSync"]
        # Job Limits/Groups/Pools/Machines
        self._data.pool = data["Props"]["Pool"]
        self._data.secondary_pool = data["Props"]["SecPool"]
        self._data.group = data["Props"]["Grp"]
        self._data.limitGroups = data["Props"]["Limits"]
        self._data.whitelistFlag = data["Props"]["White"]
        self._data.listedSlaves = data["Props"]["ListedSlaves"]
        self._data.machineLimit = data["Props"]["MachLmt"]
        self._data.machineLimitProgress = data["Props"]["MachLmtProg"]
        self._data.remainingTimeThreshold = data["Props"]["RemTmT"]
        # Job State
        self._data.status = JobStatus(data["Stat"])
        self._data.sendJobErrorWarning = data["Props"]["SndWarn"]
        self._data.overrideJobFailureDetection = data["Props"]["JobFailOvr"]
        self._data.failureDetectionJobErrors = data["Props"]["JobFailErr"]
        self._data.interruptable = data["Props"]["Int"]
        self._data.interruptablePercentage = data["Props"]["IntPer"]
        self._data.minRenderTimeSeconds = data["Props"]["MinTime"]
        self._data.enableAutoTimeout = data["Props"]["Timeout"]
        self._data.enableFrameTimeouts = data["Props"]["FrameTimeout"]
        self._data.failureDetectionTaskErrors = None # TODO 
        self._data.ignore_bad_slave_detection = data["Props"]["NoBad"]
        self._data.override_task_failure_detection = data["Props"]["TskFailOvr"]
        self._data.start_job_timeout_seconds = data["Props"]["StartTime"]
        self._data.initialize_plugin_timeout_seconds = data["Props"]["InitializePluginTime"]
        self._data.task_timeout_seconds = data["Props"]["MaxTime"] # TODO
        self._data.on_task_timeout = TaskOnTimeout(data["Props"]["TskFailErr"])
        # Job Tasks
        self._data.concurrent_tasks = data["Props"]["Conc"]
        self._data.limit_tasks_to_number_of_cpus = data["Props"]["ConcLimt"]
        self._data.override_task_extra_info_names = data["Props"]["OvrTaskEINames"]
        self._data.taskExtraInfoNameIndex = {
            idx: data["Props"]["TaskEx{}".format(idx)] for idx in range(0,10)
        }
        # Job Plugin
        self._data.plugin = data["Plug"]
        self._data.plugin_info = data["Props"]["PlugInfo"]
        self._data.force_reload_plugin = data["Props"]["Reload"]
        self._data.custom_plugin_directory = data["Props"]["PlugDir"]
        # Job Event Plugins
        self._data.suppress_events = data["Props"]["NoEvnt"]
        self._data.custom_event_plugin_directory = data["Props"]["EventDir"]
        # Job Pre/Post (Task) Scripts
        self._data.pre_job_script = data["Props"]["PrJobScrp"]
        self._data.post_job_script = data["Props"]["PoJobScrp"]
        self._data.pre_task_script = data["Props"]["PrTskScrp"]
        self._data.post_task_script = data["Props"]["PoTskScrp"]
        self._data.enable_script_tasks_timeouts = data["Props"]["TimeScrpt"]
        # Job Dependencies
        self._data.resume_on_complete_dependencies = data["Props"]["DepComp"]
        self._data.resume_on_deleted_dependencies = data["Props"]["DepDel"]
        self._data.resume_on_failed_dependencies = data["Props"]["DepFail"]
        self._data.dependency_percentage_value = data["Props"]["DepPer"]
        self._data.is_frame_dependent = data["Props"]["DepFrame"]
        self._data.frame_dependency_offset_start = data["Props"]["DepFrameStart"]
        self._data.frame_dependency_offset_end = data["Props"]["DepFrameEnd"]
        self._data.dependency_ids = data["Props"]["Dep"]
        self._data.required_assets = data["Props"]["ReqAss"]
        self._data.script_dependencies = [
            Script(FileName=s["FileName"],
                   Notes=s["Notes"],
                   IgnoreFrameOffsets=s["IgnoreFrameOffsets"]) for s in data["Props"]["ScrDep"]
        ]
        # Job Cleanup
        self._data.override_auto_job_cleanup = data["Props"]["OverAutoClean"]
        self._data.auto_job_cleanup_type = AutoJobCleanupType(data["Props"]["OverCleanType"])
        self._data.override_job_cleanup = data["Props"]["OverClean"]
        self._data.override_job_cleanup_days = data["Props"]["OverCleanDays"]
        # Job Stats
        self._data.submit_date_time = data["Date"]
        self._data.submit_machine = data["Mach"]
        self._data.started_date_time = data["DateStart"]
        self._data.completed_date_time = data["DateComp"]
        self._data.task_count = data["Props"]["Tasks"]
        self._data.queued_tasks = data["QueuedChunks"]
        self._data.rendering_tasks = data["RenderingChunks"]
        self._data.pending_tasks = data["PendingChunks"]
        self._data.completed_tasks = data["CompletedChunks"]
        self._data.suspended_tasks = data["SuspendedChunks"]
        self._data.failed_tasks = data["FailedChunks"]
        # Job Notifications
        self._data.override_notification_method = data["Props"]["NotOvr"]
        self._data.notification_targets = data["Props"]["NotUser"]
        self._data.email_notification = data["Props"]["SndEmail"]
        self._data.notification_emails = data["Props"]["NotEmail"]
        self._data.notification_note = data["Props"]["NotNote"]
        self._data.notification_popup = data["Props"]["SndPopup"]
        # Job Maintenance
        self._data.maintenance_job = data["Main"]
        self._data.maintenance_job_start_frame = data["MainStart"]
        self._data.maintenance_job_end_frame = data["MainEnd"]
        # Job Time Schedule
        self._data.scheduled_type = JobScheduledType(data["Props"]["Schd"])
        self._data.scheduled_days = data["Props"]["SchdDays"]
        self._data.scheduled_start_date_time = data["Props"]["SchdDate"]
        self._data.scheduled_end_date_time = data["Props"]["SchdStop"]
        self._data.disabled_schedule_time = False # TODO
        self._data.scheduled_day_monday_start_time_span = data["Props"]["MonStart"]
        self._data.scheduled_day_monday_end_time_span = data["Props"]["MonStop"]
        self._data.scheduled_day_tuesday_start_time_span = data["Props"]["TueStart"]
        self._data.scheduled_day_tuesday_end_time_span = data["Props"]["TueStop"]
        self._data.scheduled_day_wednesday_start_time_span = data["Props"]["WedStart"]
        self._data.scheduled_day_wednesday_end_time_span = data["Props"]["WedStop"]
        self._data.scheduled_day_thursday_start_time_span = data["Props"]["ThuStart"]
        self._data.scheduled_day_thursday_end_time_span = data["Props"]["ThuStop"]
        self._data.scheduled_day_friday_start_time_span = data["Props"]["FriStart"]
        self._data.scheduled_day_friday_end_time_span = data["Props"]["FriStop"]
        self._data.scheduled_day_saturday_start_time_span = data["Props"]["SatStart"]
        self._data.scheduled_day_saturday_end_time_span = data["Props"]["SatStop"]
        self._data.scheduled_day_sunday_start_time_span = data["Props"]["SunStart"]
        self._data.scheduled_day_sunday_end_time_span = data["Props"]["SunStop"]
        # Job Tile Rendering
        self._data.tile_job = data["Tile"]
        self._data.tile_job_frame = data["TileFrame"]
        self._data.tile_job_tile_count = data["TileCount"]
        self._data.output_tile_file_names = data["TileFile"]
        self.tile_job_tiles_in_x = data["TileX"]
        self.tile_job_tiles_in_y = data["TileY"]

        self._unknownData = {
            "Props": {
                "Region": "",
                "PathMap": [],
                "AutoTime": False,
                "OptIns": {},
                "AWSPortalAssets": [],
                "AWSPortalAssetFileWhitelist": [],
            },
            "ComFra": 0,
            "IsSub": True,
            "Purged": False,
            "Bad": [],
            "SnglTskPrg": "0 %",
            "Errs": 0,
            "DataSize": -1,
            "ConcurrencyToken": None,
            "ExtraElements": None
        }

    def serializeWebAPI(self) -> dict:
        """Serialize this class to the Web API compatible format.
        Returns:
            dict: The serialized job object. 
        """
        data = {"Props": {}}
        data.update(self._unknownData)
        # Job General
        data["_id"] = self._data.id
        data["Props"]["Name"] = self._data.name
        data["Props"]["Batch"] = self._data.batchName
        data["Props"]["Pri"] = self._data.priority
        data["Props"]["Protect"] = self._data.protected
        data["Props"]["User"] = self._data.userName
        data["Props"]["Dept"] = self._data.department
        data["Props"]["Cmmt"] = self._data.comment
        data["Props"]["Frames"] = self._data.frames
        data["Props"]["Chunk"] = self._data.frames_per_task
        data["Props"]["Seq"] = self._data.sequential
        data["Props"]["OnComp"] = self._data.onJobComplete.value
        # Job Environment
        data["Props"]["Env"] = self._data.env
        data["Props"]["EnvOnly"] = self._data.useJobEnvironmentOnly
        # Job Info
        # self._data.info = None #TODO
        data["Props"]["ExDic"] = self._data.extraInfo
        for key, value in self._data.extraInfoIndexed.items():
            data["Props"]["Ex{}".format(key)] = value
        # Job Files
        data["OutDir"] = self._data.outputDirectories
        data["OutFile"] = self._data.outputFileNames
        data["Aux"] = self._data.auxiliarySubmissionFileNames
        data["Props"]["AuxSync"] = self._data.auxiliarySyncAllFiles
        # Job Limits/Groups/Pools/Machines
        data["Props"]["Pool"] = self._data.pool
        data["Props"]["SecPool"] = self._data.secondary_pool 
        data["Props"]["Grp"] = self._data.group
        data["Props"]["Limits"] = self._data.limitGroups
        data["Props"]["White"] = self._data.whitelistFlag
        data["Props"]["ListedSlaves"] = self._data.listedSlaves
        data["Props"]["MachLmt"] = self._data.machineLimit
        data["Props"]["MachLmtProg"] = self._data.machineLimitProgress
        # Job State
        data["Stat"] = self._data.status.value
        data["Props"]["SndWarn"] = self._data.sendJobErrorWarning
        data["Props"]["JobFailOvr"] = self._data.overrideJobFailureDetection
        data["Props"]["JobFailErr"] = self._data.failureDetectionJobErrors
        data["Props"]["Int"] = self._data.interruptable
        data["Props"]["IntPer"] = self._data.interruptablePercentage
        data["Props"]["MinTime"] = self._data.minRenderTimeSeconds
        data["Props"]["Timeout"] = self._data.enableAutoTimeout
        data["Props"]["FrameTimeout"] = self._data.enableFrameTimeouts
        data["Props"]["RemTmT"] = self._data.remainingTimeThreshold
        # self._data.failure_detection_task_errors = None # TODO 
        data["Props"]["NoBad"] = self._data.ignore_bad_slave_detection
        data["Props"]["TskFailOvr"] = self._data.override_task_failure_detection
        data["Props"]["StartTime"] = self._data.start_job_timeout_seconds
        data["Props"]["InitializePluginTime"] = self._data.initialize_plugin_timeout_seconds
        data["Props"]["MaxTime"] = self._data.task_timeout_seconds # TODO
        data["Props"]["TskFailErr"] = self._data.on_task_timeout.value # TODO
        # Job Tasks
        data["Props"]["Conc"] = self._data.concurrent_tasks
        data["Props"]["ConcLimt"] = self._data.limit_tasks_to_number_of_cpus
        data["Props"]["OvrTaskEINames"] = self._data.override_task_extra_info_names
        for idx in range(0, 10):
            data["Props"]["TaskEx{}".format(idx)] = self._data.taskExtraInfoNameIndex[idx]
        # Job Plugin
        data["Plug"] = self._data.plugin
        data["Props"]["PlugInfo"] = self._data.plugin_info
        data["Props"]["Reload"] = self._data.force_reload_plugin
        data["Props"]["PlugDir"] = self._data.custom_plugin_directory
        # Job Event Plugins
        data["Props"]["EventOI"] = ",".join(self._data.event_opt_ins)
        data["Props"]["NoEvnt"] = self._data.suppress_events
        data["Props"]["EventDir"] = self._data.custom_event_plugin_directory
        # Job Pre/Post (Task) Scripts
        data["Props"]["PrJobScrp"] = self._data.pre_job_script
        data["Props"]["PoJobScrp"] = self._data.post_job_script
        data["Props"]["PrTskScrp"] = self._data.pre_task_script
        data["Props"]["PoTskScrp"] = self._data.post_task_script
        data["Props"]["TimeScrpt"] = self._data.enable_script_tasks_timeouts
        # Job Dependencies
        data["Props"]["DepComp"] = self._data.resume_on_complete_dependencies
        data["Props"]["DepDel"] = self._data.resume_on_deleted_dependencies
        data["Props"]["DepFail"] = self._data.resume_on_failed_dependencies
        data["Props"]["DepPer"] = self._data.dependency_percentage_value
        data["Props"]["DepFrame"] = self._data.is_frame_dependent
        data["Props"]["DepFrameStart"] = self._data.frame_dependency_offset_start
        data["Props"]["DepFrameEnd"] = self._data.frame_dependency_offset_end
        data["Props"]["Dep"] = self._data.dependency_ids
        data["Props"]["ReqAss"] = self._data.required_assets
        data["Props"]["ScrDep"] = []
        for script in self._data.script_dependencies:
            data["Props"]["ScrDep"].append(
                {
                    "FileName": script.FileName,
                    "Notes": script.Notes,
                    "IgnoreFrameOffsets": script.IgnoreFrameOffsets,
                }
            )
        # Job Cleanup
        data["Props"]["OverAutoClean"] = self._data.override_auto_job_cleanup
        data["Props"]["OverCleanType"] = self._data.auto_job_cleanup_type.value
        data["Props"]["OverClean"] = self._data.override_job_cleanup
        data["Props"]["OverCleanDays"] = self._data.override_job_cleanup_days
        # Job Stats
        data["Date"] = self._data.submit_date_time
        data["Mach"] = self._data.submit_machine
        data["DateStart"] = self._data.started_date_time
        data["DateComp"] = self._data.completed_date_time
        data["Props"]["Tasks"] = self._data.task_count 
        data["QueuedChunks"] = self._data.queued_tasks
        data["RenderingChunks"] = self._data.rendering_tasks
        data["PendingChunks"] = self._data.pending_tasks
        data["CompletedChunks"] = self._data.completed_tasks
        data["SuspendedChunks"] = self._data.suspended_tasks
        data["FailedChunks"] = self._data.failed_tasks 
        # Job Notifications
        data["Props"]["NotOvr"] = self._data.override_notification_method
        data["Props"]["NotUser"] = self._data.notification_targets
        data["Props"]["SndEmail"] = self._data.email_notification
        data["Props"]["NotEmail"] = self._data.notification_emails
        data["Props"]["NotNote"] = self._data.notification_note
        data["Props"]["SndPopup"] = self._data.notification_popup
        # Job Maintenance
        data["Main"] = self._data.maintenance_job
        data["MainStart"] = self._data.maintenance_job_start_frame
        data["MainEnd"] = self._data.maintenance_job_end_frame
        # Job Time Schedule
        data["Props"]["Schd"] = self._data.scheduled_type.value
        data["Props"]["SchdDays"] = self._data.scheduled_days
        data["Props"]["SchdDate"] = self._data.scheduled_start_date_time
        data["Props"]["SchdStop"] = self._data.scheduled_end_date_time
        # self._data.disabled_schedule_time = False # TODO
        data["Props"]["MonStart"] = self._data.scheduled_day_monday_start_time_span
        data["Props"]["MonStop"] = self._data.scheduled_day_monday_end_time_span
        data["Props"]["TueStart"] = self._data.scheduled_day_tuesday_start_time_span
        data["Props"]["TueStop"] = self._data.scheduled_day_tuesday_end_time_span
        data["Props"]["WedStart"] = self._data.scheduled_day_wednesday_start_time_span
        data["Props"]["WedStop"] = self._data.scheduled_day_wednesday_end_time_span
        data["Props"]["ThuStart"] = self._data.scheduled_day_thursday_start_time_span
        data["Props"]["ThuStop"] = self._data.scheduled_day_thursday_end_time_span
        data["Props"]["FriStart"] = self._data.scheduled_day_friday_start_time_span
        data["Props"]["FriStop"] = self._data.scheduled_day_friday_end_time_span
        data["Props"]["SatStart"] = self._data.scheduled_day_saturday_start_time_span
        data["Props"]["SatStop"] = self._data.scheduled_day_saturday_end_time_span
        data["Props"]["SunStart"] = self._data.scheduled_day_sunday_start_time_span
        data["Props"]["SunStop"] = self._data.scheduled_day_sunday_end_time_span
        # Job Tile Rendering
        data["Tile"] = self._data.tile_job
        data["TileFrame"] = self._data.tile_job_frame
        data["TileCount"] = self._data.tile_job_tile_count
        data["TileFile"] = self._data.output_tile_file_names
        data["TileX"] = self.tile_job_tiles_in_x
        data["TileY"] = self.tile_job_tiles_in_y

        return data

    def serializeSubmissionCommandFiles(self, job_file_path: str, plugin_file_path: str):
        """Serialize this class to the deadlinecommand submission files.
        Args:
            job_file_path (str): The job submission data file path.
            plugin_file_path (str): The plugin submission data file path.
        Returns:
            list[str]: A list of args to pass to deadlinecommand.
        """
        job_data = {}
        plugin_data = {}
        args = [job_file_path, plugin_file_path]

        # Job General
        job_data["Name"] = self._data.name
        job_data["BatchName"] = self._data.batchName
        job_data["Priority"] = self._data.priority
        job_data["Protected"] = self._data.protected
        job_data["UserName"] = self._data.userName
        job_data["Department"] = self._data.department
        job_data["Comment"] = self._data.comment
        job_data["Frames"] = '1001-1010' # TODO self._data.frames
        job_data["ChunkSize"] = self._data.frames_per_task
        job_data["Sequential"] = self._data.sequential
        job_data["OnJobComplete"] = self._data.onJobComplete.name
        # Job Environment
        env_idx = -1
        for key, value in self._data.env:
            env_idx +=1 
            job_data["EnvironmentKeyValue{}".format(env_idx)] = "{}={}".format(key, value)
        job_data["UseJobEnvironmentOnly"] = self._data.useJobEnvironmentOnly
        # TODO IncludeEnvironment
        # Job Info
        # self._data.info = None #TODO
        extra_info_idx = -1
        for key, value in self._data.extraInfo.items():
            extra_info_idx +=1 
            job_data["ExtraInfoKeyValue{}".format(extra_info_idx)] = "{}={}".format(key, value)
        for key, value in self._data.extraInfoIndexed.items():
            job_data["ExtraInfo{}".format(key)] = value
        # Job Files
        for idx, output_directory in enumerate(self._data.outputDirectories):
            job_data["OutputDirectory{}".format(idx)] = output_directory
        if not self._data.tile_job:
            for idx, output_file_name in enumerate(self._data.outputFileNames):
                job_data["OutputFilename{}".format(idx)] = output_file_name
        for auxiliary_submission_file_name in self._data.auxiliarySubmissionFileNames:
            args.append(auxiliary_submission_file_name)
        job_data["SynchronizeAllAuxiliaryFiles"] = self._data.auxiliarySyncAllFiles
        if self._data.network_root:
            job_data["NetworkRoot"] = self._data.network_root
        # Job Limits/Groups/Pools/Machines
        job_data["Pool"] = self._data.pool
        job_data["SecondaryPool"] = self._data.secondary_pool 
        job_data["Group"] = self._data.group
        job_data["LimitGroups"] = ",".join(self._data.limitGroups)
        if self._data.whitelistFlag:
            job_data["Allowlist"] = self._data.listedSlaves
        else:
            job_data["Denylist"] = self._data.listedSlaves
        job_data["MachineLimit"] = self._data.machineLimit
        job_data["MachineLimitProgress"] = self._data.machineLimitProgress
        # Job State
        job_data["InitialStatus"] = self._data.status.name
        job_data["SendJobErrorWarning"] = self._data.sendJobErrorWarning
        job_data["OverrideJobFailureDetection"] = self._data.overrideJobFailureDetection
        job_data["FailureDetectionJobErrors"] = self._data.failureDetectionJobErrors
        job_data["Interruptible"] = self._data.interruptable
        job_data["InterruptiblePercentage"] = self._data.interruptablePercentage
        job_data["MinRenderTimeSeconds"] = self._data.minRenderTimeSeconds
        job_data["EnableAutoTimeout"] = self._data.enableAutoTimeout
        job_data["EnableFrameTimeouts"] = self._data.enableFrameTimeouts
        job_data["RemTimeThreshold"] = self._data.remainingTimeThreshold
        job_data["FailureDetectionTaskErrors"] = self._data.failureDetectionTaskErrors
        job_data["IgnoreBadJobDetection"] = self._data.ignore_bad_slave_detection
        job_data["OverrideTaskFailureDetection"] = self._data.override_task_failure_detection
        job_data["StartJobTimeoutSeconds"] = self._data.start_job_timeout_seconds
        job_data["InitializePluginTimeoutSeconds"] = self._data.initialize_plugin_timeout_seconds
        job_data["TaskTimeoutSeconds"] = self._data.task_timeout_seconds
        # data["Props"]["TskFailErr"] = self._data.on_task_timeout.value # TODO
        # TODO OnTaskTimeout
        # Job Tasks
        job_data["ConcurrentTasks"] = self._data.concurrent_tasks
        job_data["LimitConcurrentTasksToNumberOfCpus"] = self._data.limit_tasks_to_number_of_cpus
        job_data["OverrideTaskExtraInfoNames"] = self._data.override_task_extra_info_names
        for key, value in self._data.taskExtraInfoNameIndex.items():
            job_data["TaskExtraInfoName{}".format(key)] = value
        # Job Plugin
        job_data["Plugin"] = self._data.plugin
        for key, value in self._data.plugin_info.items():
            plugin_data[key] = value
        job_data["ForceReloadPlugin"] = self._data.force_reload_plugin
        job_data["CustomPluginDirectory"] = self._data.custom_plugin_directory
        # Job Event Plugins
        job_data["SuppressEvents"] = self._data.suppress_events
        # TODO data["Props"]["EventDir"] = self._data.custom_event_plugin_directory
        job_data["EventOptIns"] = ",".join(self._data.event_opt_ins)
        # Job Pre/Post (Task) Scripts
        job_data["PreJobScript"] = self._data.pre_job_script
        job_data["PostJobScript"] = self._data.post_job_script
        job_data["PreTaskScript"] = self._data.pre_task_script
        job_data["PostTaskScript"] = self._data.post_task_script
        job_data["EnableTimeoutsForScriptTasks"] = self._data.enable_script_tasks_timeouts
        # Job Dependencies
        job_data["ResumeOnCompleteDependencies"] = self._data.resume_on_complete_dependencies
        job_data["ResumeOnDeletedDependencies"] = self._data.resume_on_deleted_dependencies
        job_data["ResumeOnFailedDependencies"] = self._data.resume_on_failed_dependencies
        job_data["JobDependencyPercentage"] = self._data.dependency_percentage_value
        job_data["IsFrameDependent"] = self._data.is_frame_dependent
        job_data["FrameDependencyOffsetStart"] = self._data.frame_dependency_offset_start
        job_data["FrameDependencyOffsetEnd"] = self._data.frame_dependency_offset_end
        job_data["JobDependencies"] = ",".join(self._data.dependency_ids)
        job_data["RequiredAssets"] = self._data.required_assets
        job_data["ScriptDependencies"] = ",".join(
            [script.FileName for script in self._data.script_dependencies]
        )
        # Job Cleanup
        job_data["OverrideAutoJobCleanup"] = self._data.override_auto_job_cleanup
        job_data["OverrideJobCleanupType"] = self._data.auto_job_cleanup_type.name
        job_data["OverrideJobCleanup"] = self._data.override_job_cleanup
        job_data["JobCleanupDays"] = self._data.override_job_cleanup_days
        # Job Stats
        job_data["MachineName"] = self._data.submit_machine
        # Job Notifications
        job_data["OverrideNotificationMethod"] = self._data.override_notification_method
        job_data["NotificationTargets"] = ",".join(self._data.notification_targets)
        job_data["EmailNotification"] = self._data.email_notification
        job_data["NotificationEmails"] = ",".join(self._data.notification_emails)
        job_data["NotificationNote"] = self._data.notification_note
        job_data["PopupNotification"] = self._data.notification_popup
        # Job Maintenance
        job_data["MaintenanceJob"] = self._data.maintenance_job
        job_data["MaintenanceJobStartFrame"] = self._data.maintenance_job_start_frame
        job_data["MaintenanceJobEndFrame"] = self._data.maintenance_job_end_frame
        # Job Time Schedule
        scheduled_type = self._data.scheduled_type.name
        scheduled_type = scheduled_type if scheduled_type != "None_" else "None"
        job_data["ScheduledType"] = scheduled_type
        if self._data.scheduled_type != JobScheduledType.None_:
            job_data["ScheduledDays"] = self._data.scheduled_days
            job_data["ScheduledStartDateTime"] = self._data.scheduled_start_date_time
            # self._data.disabled_schedule_time = False # TODO
            if self._data.scheduled_type == JobScheduledType.Custom:
                job_data["ScheduledMondayStartTime"] = self._data.scheduled_day_monday_start_time_span
                job_data["ScheduledMondayStopTime"] = self._data.scheduled_day_monday_end_time_span
                job_data["ScheduledTuesdayStartTime"] = self._data.scheduled_day_tuesday_start_time_span
                job_data["ScheduledTuesdayStopTime"] = self._data.scheduled_day_tuesday_end_time_span
                job_data["ScheduledWednesdayStartTime"] = self._data.scheduled_day_wednesday_start_time_span
                job_data["ScheduledWednesdayStopTime"] = self._data.scheduled_day_wednesday_end_time_span
                job_data["ScheduledThursdayStartTime"] = self._data.scheduled_day_thursday_start_time_span
                job_data["ScheduledThursdayStopTime"] = self._data.scheduled_day_thursday_end_time_span
                job_data["ScheduledFridayStartTime"] = self._data.scheduled_day_friday_start_time_span
                job_data["ScheduledFridayStopTime"] = self._data.scheduled_day_friday_end_time_span
                job_data["ScheduledSaturdayStartTime"] = self._data.scheduled_day_saturday_start_time_span
                job_data["ScheduledSaturdayStopTime"] = self._data.scheduled_day_saturday_end_time_span
                job_data["ScheduledSundayStartTime"] = self._data.scheduled_day_sunday_start_time_span
                job_data["ScheduledSundayStopTime"] = self._data.scheduled_day_sunday_end_time_span
        # Job Tile Rendering
        job_data["TileJob"] = self._data.tile_job
        if self._data.tile_job:
            job_data["TileJobFrame"] = self._data.tile_job_frame
            job_data["TileJobTileCount"] = self._data.tile_job_tile_count
            job_data["TileJobTilesInX"] = self._data.tile_job_tiles_in_x
            job_data["TileJobTilesInY"] = self._data.tile_job_tiles_in_y
            output_tile_idx = -1
            for output_tile_file_name in self._data.output_tile_file_names:
                output_tile_idx += 1
                job_data["OutputFilename{}Tile?".format(output_tile_idx)] = output_tile_file_name

        # Write job submission file
        with open(job_file_path, "w") as job_file:
            for key, value in sorted(job_data.items()):
                if isinstance(value, bool):
                    value = "true" if value else "false"
                job_file.write("{}={}\n".format(key, value))

        # Write plugin submission file
        with open(plugin_file_path, "w") as plugin_file:
            for key, value in sorted(plugin_data.items()):
                if isinstance(bool, value):
                    value = "true" if value else "false"
                plugin_file.write("{}={}\n".format(key, value))

        return args

    #########################################
    # Deadline Scripting API
    # This is a 1:1 Job Class compatibility layer.
    # As we can use this class to construct jobs
    # additional setters have been added.
    # Differences:
    #   JobStatus -> Signature Enum JobStatus
    #             -> Added Property Setter 
    #   JobOnJobComplete -> Signature Enum JobCompleteAction
    #   JobAuxiliarySubmissionFileNames -> Added Property Setter

    #########################################
    
    # Job General
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
        Returns:
            str: The frame list string.
        """
        # TODO Add serialize
        return ",".join(self._data.frames)

    @property
    def JobFramesList(self):
        """The job's frame list as an array.
        Args:
            value (list[int])
        Returns:
            str: The frame list array.
        """
        return self._data.frames

    @property
    def JobFramesPerTask(self):
        """The number of frames per task.
        Returns:
            int: Frames per task.
        """
        return self._data.frames_per_task

    @property
    def JobSequentialJob(self):
        """If the job is a sequential job, which ensures
        its tasks only render in ascending order.
        Args:
            value (bool): The sequential state.
        Returns:
            bool: The sequential state.
        """
        return self._data.sequential

    @JobSequentialJob.setter
    def JobSequentialJob(self, value: bool):
        self._data.sequential = value

    @property
    def JobOnJobComplete(self):
        """What the job should do when it completes.
        The options are "Archive", "Delete", or "Nothing".
        Args:
            value (str): "Archive", "Delete", or "Nothing".
        Returns:
            str: The action name.
        """
        return self._data.onJobComplete
    
    @JobOnJobComplete.setter
    def JobOnJobComplete(self, value: str):
        self._data.onJobComplete = JobCompleteAction(value)

    # Job Environment
    def GetJobEnvironmentKeys(self):
        """Gets the keys for the job's environment variable entries.
        Returns:
            list[str]: A list of keys
        """
        return self._data.env.keys()

    def GetJobEnvironmentKeyValue(self, key: str):
        """Gets the environment variable value for the given key.
        Args:
            key (str): The env variable name.
        Returns:
            str | None: The value of the env variable.
        """
        return self._data.env.get(key, None)

    def SetJobEnvironmentKeyValue(self, key: str, value: str):
        """Sets the environment variable value for the given key.
        Args:
            key (str): The env variable name. 
            value (str): The env variable value.
        """
        self._data.env[key] = value

    def DeleteJobEnvironmentKey(self, key: str):
        """Deletes the environment variable for the given key.
        Args:
            key (str): The env variable name.
        """
        self._data.env.pop(key, None)

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
        return self._data.useJobEnvironmentOnly

    @JobUseJobEnvironmentOnly.setter
    def JobUseJobEnvironmentOnly(self, value: bool):
        self._data.useJobEnvironmentOnly = value

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
        return self._data.extraInfo.keys()

    def GetJobExtraInfoKeyValue(self, key: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
        Returns:
            str | None: The value.
        """
        return self._data.extraInfo.get(key, None)

    def GetJobExtraInfoKeyValueWithDefault(self, key: str, defaultValue: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
            defaultValue (str): The fallback value if the key doesn't exist.
        Returns:
            str: The value.
        """
        return self._data.extraInfo.get(key, defaultValue)

    def SetJobExtraInfoKeyValue(self, key: str, value: str):
        """Sets the extra info value for the given key.
        Args:
            key (str): The key name.
            value (str): The value.
        """
        self._data.extraInfo[key] = value

    def DeleteJobExtraInfoKey(self, key: str):
        """Deletes the extra info for the given key.
        Args:
            key (str): The key name.
        """
        self._data.extraInfo.pop(key, None)

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
    def JobOutputDirectories(self):
        """The list of output directories.
        Returns:
            list[str]: A list of directory paths.
        """
        return self._data.outputDirectories

    @property
    def JobOutputFileNames(self):
        """The list of output filenames.
        Returns:
            list[str]: A list of file names.
        """
        return self._data.outputFileNames

    @property
    def JobAuxiliarySubmissionFileNames(self):
        """The auxiliary files submitted with the job.
        Returns:
            list[str]: Defaults to TimeSpan.MinValue
        """
        return self._data.auxiliarySubmissionFileNames

    @JobAuxiliarySubmissionFileNames.setter
    def JobAuxiliarySubmissionFileNames(self, value: list[str]):
        self._data.auxiliarySubmissionFileNames = value

    @property
    def JobSynchronizeAllAuxiliaryFiles(self):
        """If the job's auxiliary files should be
        synced up by the Worker between tasks.
        Returns:
            bool: The sync state.
        """
        return self._data.auxiliarySyncAllFiles

    @JobSynchronizeAllAuxiliaryFiles.setter
    def JobSynchronizeAllAuxiliaryFiles(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.auxiliarySyncAllFiles = value

    # Job Limits/Groups/Pools/Machines
    @property
    def JobPool(self):
        """The job's pool.
        Returns:
            str:
        """
        return self._data.pool

    @JobPool.setter
    def JobPool(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._data.pool = value

    @property
    def JobSecondaryPool(self):
        """The Secondary Pool in which this Job belongs.
        Returns:
            string:
        """
        return self._data.secondary_pool

    @JobSecondaryPool.setter
    def JobSecondaryPool(self, value: str):
        """See getter.
        Args:
            value (string)
        """
        self._data.secondary_pool = value

    @property
    def JobGroup(self):
        """The job's group.
        Returns:
            str:
        """
        return self._data.group

    @JobGroup.setter
    def JobGroup(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._data.group = value

    @property
    def JobLimitGroups(self):
        """The limit groups the job requires.
        Returns:
            list[str]:
        """
        return self._data.limitGroups

    def SetJobLimitGroups(self, limitGroups: list[str]):
        """Sets the limit groups the job requires.
        Args:
            jobIds (list[int]): The key to get.
        """
        self._data.limitGroups = limitGroups

    @property
    def JobWhitelistFlag(self):
        """If the job's listed Workers are an allow
        list or a deny list.
        Returns:
            bool:
        """
        return self._data.whitelistFlag

    @property
    def JobListedSlaves(self):
        """The list of Workers in allow or deny list for
        the job. Use JobWhitelistFlag to determine if the
        list is a deny list or an allow list.

        Returns:
            list[str]:
        """
        return self._data.listedSlaves

    @property
    def JobMachineLimit(self):
        """The machine limit for the job.
        Returns:
            int:
        """
        return self._data.machineLimit

    @property
    def JobMachineLimitProgress(self):
        """When the Worker reaches this progress for
        the job's task, it will release the limit group.
        Returns:
            double:
        """
        return self._data.machineLimitProgress

    @property
    def RemTimeThreshold(self):
        """The remaining time (in seconds) that this Job
        must have left more than in order to be interruptable.
        Returns:
            int:
        """
        return self._data.remainingTimeThreshold

    @RemTimeThreshold.setter
    def RemTimeThreshold(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.remainingTimeThreshold = value

    # Job State
    @property
    def JobStatus(self):
        """The job's current state.
        Returns:
            str:
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
            value (bool)
        Returns:
            bool:
        """
        return self._data.sendJobErrorWarning

    @JobSendJobErrorWarning.setter
    def JobSendJobErrorWarning(self, value: bool):
        self._data.sendJobErrorWarning = value

    @property
    def JobOverrideJobFailureDetection(self):
        """Whether or not this job overrides the Job
        Failure Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.overrideJobFailureDetection

    @JobOverrideJobFailureDetection.setter
    def JobOverrideJobFailureDetection(self, value: bool):
        self._data.overrideJobFailureDetection = value

    @property
    def JobFailureDetectionJobErrors(self):
        """If JobOverrideJobFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a job failure.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.failureDetectionJobErrors

    @JobFailureDetectionJobErrors.setter
    def JobFailureDetectionJobErrors(self, value: int):
        self._data.failureDetectionJobErrors = value

    @property
    def JobInterruptible(self):
        """If the job is interruptible, which causes it
        to be canceled when a job with higher priority comes along.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.interruptable

    @JobInterruptible.setter
    def JobInterruptible(self, value: bool):
        self._data.interruptable = value

    @property
    def JobInterruptiblePercentage(self):
        """The completion percentage that this Job must
        be less than in order to be interruptible.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.interruptablePercentage

    @JobInterruptiblePercentage.setter
    def JobInterruptiblePercentage(self, value: int):
        self._data.interruptablePercentage = value

    @property
    def JobMinRenderTimeSeconds(self):
        """The minimum number of seconds a job must run
        to be considered successful.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.minRenderTimeSeconds

    @JobMinRenderTimeSeconds.setter
    def JobMinRenderTimeSeconds(self, value: int):
        self._data.minRenderTimeSeconds = value

    @property
    def JobEnableAutoTimeout(self):
        """The Auto Task Timeout feature is based on the Auto Job Timeout
        Settings in the Repository Options. The timeout is based on the
        render times of the tasks that have already finished for this job,
        so this option should only be used if the frames for the job have
        consistent render times.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.enableAutoTimeout

    @JobEnableAutoTimeout.setter
    def JobEnableAutoTimeout(self, value: bool):
        self._data.enableAutoTimeout = value

    @property
    def JobEnableFrameTimeouts(self):
        """If the timeouts are Frame based instead of Task based.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.enableFrameTimeouts

    @JobEnableFrameTimeouts.setter
    def JobEnableFrameTimeouts(self, value: bool):
        self._data.enableFrameTimeouts = value

    @property
    def JobFailureDetectionTaskErrors(self):
        """If JobOverrideTaskFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a task failure.
        Returns:
            int:
        """
        return self._data.failureDetectionTaskErrors

    @JobFailureDetectionTaskErrors.setter
    def JobFailureDetectionTaskErrors(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.failureDetectionTaskErrors = value

    @property
    def JobIgnoreBadSlaveDetection(self):
        """Whether or not this job overrides the Bad Worker Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.ignore_bad_slave_detection

    @JobIgnoreBadSlaveDetection.setter
    def JobIgnoreBadSlaveDetection(self, value: bool):
        self._data.ignore_bad_slave_detection = value

    @property
    def JobOverrideTaskFailureDetection(self):
        """Whether or not this job overrides the Task Failure
        Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.override_task_failure_detection

    @JobOverrideTaskFailureDetection.setter
    def JobOverrideTaskFailureDetection(self, value: bool):
        self._data.override_task_failure_detection = value

    @property
    def JobStartJobTimeoutSeconds(self):
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.start_job_timeout_seconds

    @JobStartJobTimeoutSeconds.setter
    def JobStartJobTimeoutSeconds(self, value: int):
        self._data.start_job_timeout_seconds = value

    @property
    def JobInitializePluginTimeoutSeconds(self):
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.initialize_plugin_timeout_seconds

    @JobInitializePluginTimeoutSeconds.setter
    def JobInitializePluginTimeoutSeconds(self, value: int):
        self._data.initialize_plugin_timeout_seconds = value

    @property
    def JobTaskTimeoutSeconds(self):
        """The timespan a job's task has to render before
        a timeout occurs.
        Returns:
            int:
        """
        return self._data.task_timeout_seconds

    @JobTaskTimeoutSeconds.setter
    def JobTaskTimeoutSeconds(self, value: int):
        self._data.task_timeout_seconds = value

    @property
    def JobOnTaskTimeout(self):
        """What to do when a task times out.
        The options are "Error", "Notify", or "Both".
        Args:
            value (str)
        Returns:
            str:
        """
        return self._data.on_task_timeout

    @JobOnTaskTimeout.setter
    def JobOnTaskTimeout(self, value: str):
        self._data.on_task_timeout = value


    # Job Tasks
    @property
    def JobConcurrentTasks(self):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Returns:
            int:
        """
        return self._data.concurrent_tasks

    @JobConcurrentTasks.setter
    def JobConcurrentTasks(self, value: int):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Args:
            value (int)
        """
        self._data.concurrent_tasks = value

    @property
    def JobLimitTasksToNumberOfCpus(self):
        """Whether or not the number of concurrent tasks
        a Worker can dequeue for this job should be limited
        to the number of CPUs the Worker has.
        Returns:
            bool:
        """
        return self._data.limit_tasks_to_number_of_cpus

    @JobLimitTasksToNumberOfCpus.setter
    def JobLimitTasksToNumberOfCpus(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.limit_tasks_to_number_of_cpus = value

    @property
    def JobOverrideTaskExtraInfoNames(self):
        """Whether this job overrides the task extra info names.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.override_task_extra_info_names


    @JobOverrideTaskExtraInfoNames.setter
    def JobOverrideTaskExtraInfoNames(self, value: bool):
        self._data.override_task_extra_info_names = value

    @property
    def JobTaskExtraInfoName0(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(0)

    @JobTaskExtraInfoName0.setter
    def JobTaskExtraInfoName0(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(0, value)

    @property
    def JobTaskExtraInfoName1(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(1)

    @JobTaskExtraInfoName1.setter
    def JobTaskExtraInfoName1(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(1, value)

    @property
    def JobTaskExtraInfoName2(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(2)

    @JobTaskExtraInfoName2.setter
    def JobTaskExtraInfoName2(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(2, value)

    @property
    def JobTaskExtraInfoName3(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(3)

    @JobTaskExtraInfoName3.setter
    def JobTaskExtraInfoName3(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(3, value)

    @property
    def JobTaskExtraInfoName4(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(4)

    @JobTaskExtraInfoName4.setter
    def JobTaskExtraInfoName4(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(4, value)

    @property
    def JobTaskExtraInfoName5(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(5)

    @JobTaskExtraInfoName5.setter
    def JobTaskExtraInfoName5(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(5, value)

    @property
    def JobTaskExtraInfoName6(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(6)

    @JobTaskExtraInfoName6.setter
    def JobTaskExtraInfoName6(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(6, value)

    @property
    def JobTaskExtraInfoName7(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(7)

    @JobTaskExtraInfoName7.setter
    def JobTaskExtraInfoName7(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(7, value)

    @property
    def JobTaskExtraInfoName8(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(8)

    @JobTaskExtraInfoName8.setter
    def JobTaskExtraInfoName8(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(8, value)

    @property
    def JobTaskExtraInfoName9(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """
        return self._GetJobTaskExtraInfoNameIndex(9)

    @JobTaskExtraInfoName9.setter
    def JobTaskExtraInfoName9(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._SetJobTaskExtraInfoNameIndex(9, value)


    # Job Plugin
    @property
    def JobPlugin(self):
        """The name of the Deadline plugin the job uses.
        Returns:
            str:
        """
        return self._data.plugin

    @JobPlugin.setter
    def JobPlugin(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._data.plugin = value

    def GetJobPluginInfoKeys(self):
        """Gets the keys for the job's plugin info entries.
        Returns:
            list[str]: The value of the env var.
        """
        return self._data.plugin_info.keys()

    def GetJobPluginInfoKeyValue(self, key: str):
        """Gets the plugin info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """
        return self._data.plugin_info.get(key, None)
    
    def SetJobPluginInfoKeyValue(self, key: str, value: str):
        """Sets the plugin info value for the given key.
        Args:
            key (str):
            value (str):
        """
        self._data.plugin_info[key] = value

    @property
    def JobForceReloadPlugin(self):
        """Whether or not the job's plugin should be
        reloaded between tasks.
        Returns:
            bool:
        """
        return self._data.force_reload_plugin

    @JobForceReloadPlugin.setter
    def JobForceReloadPlugin(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.force_reload_plugin = value

    @property
    def JobCustomPluginDirectory(self):
        """A custom location to load the job's plugin from.
        Returns:
            str:
        """
        return self._data.custom_plugin_directory

    @JobCustomPluginDirectory.setter
    def JobCustomPluginDirectory(self, value: str):
        """A custom location to load the job's plugin from.
        Args:
            value (str)
        """
        self._data.custom_plugin_directory = value

    # Job Event Plugins
    @property
    def JobSuppressEvents(self):
        """Whether or not this Job should suppress Events plugins.
        Returns:
            bool:
        """
        return self._data.suppress_events

    @JobSuppressEvents.setter
    def JobSuppressEvents(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.suppress_events = value

    @property
    def JobCustomEventPluginDirectory(self):
        """A custom location to load the job's event plugin from.
        Returns:
            str:
        """
        return self._data.custom_event_plugin_directory

    @JobCustomEventPluginDirectory.setter
    def JobCustomEventPluginDirectory(self, value: str):
        """A custom location to load the job's event plugin from.
        Args:
            value (str)
        """
        self._data.custom_event_plugin_directory = value

    # Job Pre/Post (Task) Scripts
    @property
    def JobPreJobScript(self):
        """The script to execute before the job starts. Read Only.
        Use RepositoryUtils.SetPreJobScript and RepositoryUtils.DeletePreJobScript.
        Returns:
            str:
        """
        return self._data.pre_job_script

    @property
    def JobPostJobScript(self):
        """The script to execute after the Job finishes. Read Only.
        Use RepositoryUtils.SetPostJobScript and RepositoryUtils.DeletePostJobScript.

        Returns:
            string:
        """
        return self._data.post_job_script

    @property
    def JobPreTaskScript(self):
        """The script to execute before a job task starts.
        Returns:
            str:
        """
        return self._data.pre_task_script

    @JobPreTaskScript.setter
    def JobPreTaskScript(self, value: str):
        """The script to execute before a job task starts.
        Args:
            value (str):
        """
        self._data.pre_task_script = value
    
    @property
    def JobPostTaskScript(self):
        """The script to execute when a job task is complete.
        Returns:
            str:
        """
        return self._data.post_task_script

    @JobPostTaskScript.setter
    def JobPostTaskScript(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._data.post_task_script = value

    @property
    def JobEnableTimeoutsForScriptTasks(self):
        """If the timeouts should apply to pre/post job script tasks.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.enable_script_tasks_timeouts

    @JobEnableTimeoutsForScriptTasks.setter
    def JobEnableTimeoutsForScriptTasks(self, value: bool):
        self._data.enable_script_tasks_timeouts = value

    # Job Dependencies
    @property
    def JobResumeOnCompleteDependencies(self):
        """If the job should resume on complete dependencies.
        Returns:
            bool:
        """
        return self._data.resume_on_complete_dependencies

    @JobResumeOnCompleteDependencies.setter
    def JobResumeOnCompleteDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.resume_on_complete_dependencies = value

    @property
    def JobResumeOnDeletedDependencies(self):
        """If the job should resume on deleted dependencies.
        Returns:
            bool:
        """
        return self._data.resume_on_deleted_dependencies

    @JobResumeOnDeletedDependencies.setter
    def JobResumeOnDeletedDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.resume_on_deleted_dependencies = value

    @property
    def JobResumeOnFailedDependencies(self):
        """If the job should resume on failed dependencies.
        Returns:
            bool:
        """
        return self._data.resume_on_failed_dependencies

    @JobResumeOnFailedDependencies.setter
    def JobResumeOnFailedDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.resume_on_failed_dependencies = value

    @property
    def JobDependencyPercentageValue(self):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Returns:
            float:
        """
        return self._data.dependency_percentage_value

    @JobDependencyPercentageValue.setter
    def JobDependencyPercentageValue(self, value: float):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Args:
            value (float)
        """
        self._data.dependency_percentage_value = value

    @property
    def JobIsFrameDependent(self):
        """If the job is frame dependent.
        Returns:
            bool:
        """
        return self._data.is_frame_dependent

    @JobIsFrameDependent.setter
    def JobIsFrameDependent(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.is_frame_dependent = value

    @property
    def JobFrameDependencyOffsetStart(self):
        """The start offset for frame depenencies.
        Returns:
            int:
        """
        return self._data.frame_dependency_offset_start

    @JobFrameDependencyOffsetStart.setter
    def JobFrameDependencyOffsetStart(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.frame_dependency_offset_start = value

    @property
    def JobFrameDependencyOffsetEnd(self):
        """The end offset for frame depenencies.
        Returns:
            int:
        """
        return self._data.frame_dependency_offset_end

    @JobFrameDependencyOffsetEnd.setter
    def JobFrameDependencyOffsetEnd(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.frame_dependency_offset_end = value

    @property
    def JobDependencyIDs(self):
        """The ids of the jobs that this job is dependent on.
        Returns:
            list[str]:
        """
        return self._data.dependency_ids

    def SetJobDependencyIDs(self, jobIds: list[int]):
        """Sets the IDs of the jobs that this job is dependent on.
        Args:
            jobIds (list[int]): The dependant job ids.
        """
        self._data.dependency_ids = jobIds

    @property
    def JobRequiredAssets(self):
        """The assets that are required in order to render this job.
        The assets should contain absolute paths. More...

        Returns:
            list[AssetDependency]:
        """
        return self._data.required_assets

    def SetJobRequiredAssets(self, assets: list[Asset]):
        """Sets the assets that are required in order to render this job. The assets should contain absolute paths.
        Args:
            assets (list[Asset]):
        """
        self._data.required_assets = assets

    @property
    def JobScriptDependencies(self):
        """The scripts that must return True in order to render this job.
        Returns:
            list[ScriptDependency]:
        """
        return self._data.script_dependencies

    def SetScriptDependencies(self, scripts: list[Script]):
        """Sets the scripts that must return True in order to render this job.
        Args:
            scripts (list[Script]):
        """
        self._data.script_dependencies = scripts

   # Job Cleanup
    @property
    def JobOverrideAutoJobCleanup(self):
        """If the job overrides the automatic job cleanup
        in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.override_auto_job_cleanup

    @JobOverrideAutoJobCleanup.setter
    def JobOverrideAutoJobCleanup(self, value: bool):
        self._data.override_auto_job_cleanup = value

    @property
    def AutoJobCleanupType(self):
        """The job cleanup mode. Only relevant if
        the override is set.
        Args:
            value (str)
        Returns:
            str:
        """
        return self._data.auto_job_cleanup_type

    @AutoJobCleanupType.setter
    def AutoJobCleanupType(self, value: str):
        self._data.auto_job_cleanup_type = value

    @property
    def JobOverrideJobCleanup(self):
        """If the job overrides the amount of days
        before its cleaned up.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.override_job_cleanup 

    @JobOverrideJobCleanup.setter
    def JobOverrideJobCleanup(self, value: bool):
        self._data.override_job_cleanup = value

    @property
    def JobOverrideJobCleanupDays(self):
        """The number of days before this job will be
        cleaned up after it is completed. Only relevant
        if the override is set.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.override_job_cleanup_days

    @JobOverrideJobCleanupDays.setter
    def JobOverrideJobCleanupDays(self, value: int):
        self._data.override_job_cleanup_days = value

    # Job Stats
    @property
    def JobSubmitDateTime(self):
        """The date/time at which the job was submitted.
        Returns:
            DateTime:
        """
        return self._data.submit_date_time

    @property
    def JobSubmitMachine(self):
        """This is the machine that the job was submitted from.
        Returns:
            str:
        """
        return self._data.submit_machine

    @property
    def JobStartedDateTime(self):
        """The date/time at which the job started rendering.
        Returns:
            DateTime:
        """
        return self._data.started_date_time

    @property
    def JobCompletedDateTime(self):
        """The date/time at which the job finished rendering.
        Returns:
            DateTime:
        """
        return self._data.completed_date_time

    @property
    def JobTaskCount(self):
        """The number of tasks the job has.
        Returns:
            int:
        """
        # When the job is not on the farm, calculate the
        # task count.
        if self._data.task_count == -1:
            return len(self.JobFramesList)
        return self._data.task_count

    @property
    def JobQueuedTasks(self):
        """The number of tasks in the queued state.
        Returns:
            int:
        """
        return self._data.queued_tasks

    @property
    def JobRenderingTasks(self):
        """The number of tasks in the active state.
        Returns:
            int:
        """
        return self._data.rendering_tasks

    @property
    def JobPendingTasks(self):
        """The number of tasks in the pending state.
        Returns:
            int:
        """
        return self._data.pending_tasks

    @property
    def JobCompletedTasks(self):
        """The number of tasks in the completed state.
        Returns:
            int:
        """
        return self._data.completed_tasks

    @property
    def JobSuspendedTasks(self):
        """The number of tasks in the suspended state.
        Returns:
            int:
        """
        return self._data.suspended_tasks

    @property
    def JobFailedTasks(self):
        """The number of tasks in the failed state.
        Returns:
            int:
        """
        return self._data.failed_tasks

    # Job Notifications
    @property
    def JobOverrideNotificationMethod(self):
        """If the user's notification method should be ignored.
        Returns:
            bool:
        """
        return self._data.override_notification_method

    @JobOverrideNotificationMethod.setter
    def JobOverrideNotificationMethod(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.override_notification_method = value

    @property
    def JobNotificationTargets(self):
        """The list of users that are to be
        notified when this job is complete.
        Returns:
            list[str]:
        """
        return self._data.notification_targets

    def SetJobNotificationTargets(self, userNames: list[str]):
        """Sets the list of users that are to be notified when this job is complete.
        Args:
            userNames (list[str]):
        """
        self._data.notification_targets = userNames

    @property
    def JobEmailNotification(self):
        """If overriding the user's notification method, whether to use email notification.
        Returns:
            bool:
        """
        return self._data.email_notification

    @JobEmailNotification.setter
    def JobEmailNotification(self, value: bool):
        """If overriding the user's notification method, whether to use email notification.
        Args:
            value (bool)
        """
        self._data.email_notification = value

    @property
    def JobNotificationEmails(self):
        """Arbitrary email addresses to send notifications
        to when this job is complete.
        Returns:
            list[str]:
        """
        return self._data.notification_emails

    def SetJobNotificationEmails(self, emails: list[str]):
        """Sets the arbitrary email addresses to send notifications to when this job is complete.
        Args:
            jobIds (list[int]):
        """
        self._data.notification_emails = emails

    @property
    def JobNotificationNote(self):
        """A note to append to the notification email
        sent out when the job is complete.
        Returns:
            str:
        """
        return self._data.notification_note

    @JobNotificationNote.setter
    def JobNotificationNote(self, value: str):
        """See getter.
        Args:
            value (str)
        """
        self._data.notification_note = value

    @property
    def JobPopupNotification(self):
        """If overriding the user's notification method,
        whether to use send a popup notification.
        Returns:
            bool:
        """
        return self._data.notification_popup

    @JobPopupNotification.setter
    def JobPopupNotification(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.notification_popup = value

    # Job Maintenance
    @property
    def JobMaintenanceJob(self):
        """If this is a maintenance job.
        Returns:
            bool:
        """
        return self._data.maintenance_job

    @property
    def JobMaintenanceJobStartFrame(self):
        """The start frame for a maintenance job.
        Returns:
            int:
        """
        return self._data.maintenance_job_start_frame

    @property
    def JobMaintenanceJobEndFrame(self):
        """The start frame for a maintenance job.
        Returns:
            int:
        """
        return self._data.maintenance_job_end_frame

    # Job Time Schedule
    @property
    def JobScheduledType(self):
        """The scheduling mode for this job.
        The options are "None", "Once", "Daily". or "Custom".
        Returns:
            string: "None", "Once", "Daily" or "Custom"
        """
        return self._data.scheduled_type

    @JobScheduledType.setter
    def JobScheduledType(self, value: str):
        """See getter.
        Args:
            value (string)
        """
        self._data.scheduled_type = JobScheduledType(value)

    @property
    def JobScheduledDays(self):
        """The day interval for daily scheduled jobs.
        Returns:
            int:
        """
        return self._data.scheduled_days

    @JobScheduledDays.setter
    def JobScheduledDays(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.scheduled_days = value

    @property
    def JobScheduledStartDateTime(self):
        """The start date/time at which the scheduled job should start.
        Returns:
            DateTime:
        """
        return self._data.scheduled_start_date_time

    @JobScheduledStartDateTime.setter
    def JobScheduledStartDateTime(self, value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """
        self._data.scheduled_start_date_time = value

    @property
    def JobScheduledStopDateTime(self):
        """The stop date/time at which the job should stop if it's still active.
        Returns:
            DateTime:
        """
        return self._data.scheduled_stop_date_time

    @JobScheduledStopDateTime.setter
    def JobScheduledStopDateTime(self, value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """
        self._data.scheduled_stop_date_time = value

    @property
    def DisabledScheduleTime(self):
        """Represents a disabled scheduled time for custom job scheduling settings.
        Returns:
            TimeSpan: Defaults to TimeSpan.MinValue
        """
        return self._data.disabled_schedule_time

    @property
    def JobMondayStartTime(self):
        """Gets or sets Monday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_monday_start_time_span

    @JobMondayStartTime.setter
    def JobMondayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_monday_start_time_span = value

    @property
    def JobMondayStopTime(self):
        """Gets or sets Monday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_monday_stop_time_span


    @JobMondayStopTime.setter
    def JobMondayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobTuesdayStartTime(self):
        """Gets or sets Tuesday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_tuesday_start_time_span


    @JobTuesdayStartTime.setter
    def JobTuesdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_tuesday_start_time_span = value

    @property
    def JobTuesdayStopTime(self):
        """Gets or sets Tuesday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_tuesday_stop_time_span

    @JobTuesdayStopTime.setter
    def JobTuesdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_tuesday_stop_time_span = value

    @property
    def JobWednesdayStartTime(self):
        """Gets or sets Wednesday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_wednesday_start_time_span

    @JobWednesdayStartTime.setter
    def JobWednesdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_wednesday_start_time_span = value

    @property
    def JobWednesdayStopTime(self):
        """Gets or sets Wednesday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_wednesday_stop_time_span

    @JobWednesdayStopTime.setter
    def JobWednesdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_wednesday_stop_time_span = value

    @property
    def JobThursdayStartTime(self):
        """Gets or sets Thursday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_thursday_start_time_span

    @JobThursdayStartTime.setter
    def JobThursdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_thursday_start_time_span = value

    @property
    def JobThursdayStopTime(self):
        """Gets or sets Thursday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_thursday_stop_time_span

    @JobThursdayStartTime.setter
    def JobThursdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_thursday_stop_time_span = value

    @property
    def JobFridayStartTime(self):
        """Gets or sets Friday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_friday_start_time_span

    @JobFridayStartTime.setter
    def JobFridayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_thursday_start_time_span = value

    @property
    def JobFridayStopTime(self):
        """Gets or sets Friday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_friday_stop_time_span

    @JobFridayStopTime.setter
    def JobFridayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_thursday_stop_time_span = value

    @property
    def JobSaturdayStartTime(self):
        """Gets or sets Saturday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_saturday_start_time_span

    @JobSaturdayStartTime.setter
    def JobSaturdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_saturday_start_time_span = value

    @property
    def JobSaturdayStopTime(self):
        """Gets or sets Saturday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_saturday_stop_time_span

    @JobSaturdayStopTime.setter
    def JobSaturdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_saturday_stop_time_span = value

    @property
    def JobSundayStartTime(self):
        """Gets or sets Sunday's start time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_sunday_start_time_span

    @JobSundayStartTime.setter
    def JobSundayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_sunday_start_time_span = value

    @property
    def JobSundayStopTime(self):
        """Gets or sets Sunday's stop time.
        Returns:
            TimeSpan:
        """
        return self._data.scheduled_day_sunday_stop_time_span

    @JobSundayStopTime.setter
    def JobSundayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """
        self._data.scheduled_day_sunday_stop_time_span = value

    # Job Tile Rendering   
    @property
    def JobTileJob(self):
        """If this job is a tile job.
        Returns:
            bool:
        """
        return self._data.tile_job

    @property
    def JobTileJobFrame(self):
        """The frame that the tile job is rendering.
        Returns:
            int:
        """
        return self._data.tile_job_frame

    @property
    def JobTileJobTileCount(self):
        """The number of tiles in a tile job.
        Returns:
            int:
        """
        return self._data.tile_job_tile_count

    @property
    def JobTileJobTilesInX(self):
        """The number of tiles in X for a tile job.
        This is deprecated, and is only here for backwards
        compatibility.
        Returns:
            int:
        """
        raise DeprecationWarning

    @property
    def JobTileJobTilesInY(self):
        """The number of tiles in Y for a tile job.
        This is deprecated, and is only here for backwards compatibility.
        Returns:
            int:
        """
        raise DeprecationWarning

    @property
    def JobOutputTileFileNames(self):
        """The list of output filenames for tile jobs.
        Returns:
            list[str]:
        """
        self._data.output_tile_file_names = []