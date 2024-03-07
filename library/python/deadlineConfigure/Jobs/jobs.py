
# Job Dict Ref
{
    "Props": {
        "Name": "Example - Command",
        "Batch": "",
        "User": "lucsch",
        "Region": "",
        "Cmmt": "",
        "Dept": "",
        "Frames": "1001-1010",
        "Chunk": 1,
        "Tasks": 10,
        "Grp": "none",
        "Pool": "none",
        "SecPool": "",
        "Pri": 50,
        "ReqAss": [],
        "ScrDep": [
            {
                "FileName": "/opt/Thinkbox/DeadlineRepository10/custom/library/python/deadlineConfigure/tools/jobDependencies/pendingReviewRelease.py",
                "Notes": "",
                "IgnoreFrameOffsets": false
            }
        ],
        "Conc": 1,
        "ConcLimt": true,
        "AuxSync": false,
        "Int": false,
        "IntPer": 100,
        "RemTmT": 0,
        "Seq": false,
        "Reload": false,
        "NoEvnt": false,
        "OnComp": 2,
        "Protect": false,
        "PathMap": [],
        "AutoTime": false,
        "TimeScrpt": false,
        "MinTime": 0,
        "MaxTime": 0,
        "Timeout": 1,
        "FrameTimeout": false,
        "StartTime": 0,
        "InitializePluginTime": 0,
        "Dep": [],
        "DepFrame": true,
        "DepFrameStart": 0,
        "DepFrameEnd": 0,
        "DepComp": true,
        "DepDel": false,
        "DepFail": false,
        "DepPer": -1.0,
        "NoBad": false,
        "OverAutoClean": false,
        "OverClean": false,
        "OverCleanDays": 0,
        "OverCleanType": 1,
        "JobFailOvr": false,
        "JobFailErr": 0,
        "TskFailOvr": false,
        "TskFailErr": 0,
        "SndWarn": true,
        "NotOvr": false,
        "SndEmail": false,
        "SndPopup": false,
        "NotEmail": [],
        "NotUser": [
            "lucsch"
        ],
        "NotNote": "",
        "Limits": [],
        "ListedSlaves": [],
        "White": false,
        "MachLmt": 0,
        "MachLmtProg": -1.0,
        "PrJobScrp": "",
        "PoJobScrp": "",
        "PrTskScrp": "",
        "PoTskScrp": "",
        "Schd": 0,
        "SchdDays": 1,
        "SchdDate": "2024-02-25T23:28:42.657-08:00",
        "SchdStop": "0001-01-01T00:00:00Z",
        "MonStart": "-10675199.02:48:05.4775808",
        "MonStop": "-10675199.02:48:05.4775808",
        "TueStart": "-10675199.02:48:05.4775808",
        "TueStop": "-10675199.02:48:05.4775808",
        "WedStart": "-10675199.02:48:05.4775808",
        "WedStop": "-10675199.02:48:05.4775808",
        "ThuStart": "-10675199.02:48:05.4775808",
        "ThuStop": "-10675199.02:48:05.4775808",
        "FriStart": "-10675199.02:48:05.4775808",
        "FriStop": "-10675199.02:48:05.4775808",
        "SatStart": "-10675199.02:48:05.4775808",
        "SatStop": "-10675199.02:48:05.4775808",
        "SunStart": "-10675199.02:48:05.4775808",
        "SunStop": "-10675199.02:48:05.4775808",
        "PlugInfo": {
            "Command": "python /mnt/data/PROJECT/VFX-FlowpipeDeadline/reference/debug.py <FRAME_START> <FRAME_END> <FRAME_INCREMENT>"
        },
        "Env": {
            "EXAMPLE_ENV_KEY": "EXAMPLE_ENV_VALUE",
            "DL_JOB_PENDING_REVIEW_RELEASE_STATE": "False",
            "DL_JOB_PENDING_REVIEW_RELEASE_INCREMENT": "5"
        },
        "EnvOnly": false,
        "PlugDir": "",
        "EventDir": "",
        "OptIns": {},
        "EventOI": [],
        "AWSPortalAssets": [],
        "AWSPortalAssetFileWhitelist": [],
        "Ex0": "False",
        "Ex1": "",
        "Ex2": "",
        "Ex3": "",
        "Ex4": "",
        "Ex5": "",
        "Ex6": "",
        "Ex7": "",
        "Ex8": "",
        "Ex9": "",
        "ExDic": {},
        "OvrTaskEINames": false,
        "TaskEx0": "",
        "TaskEx1": "",
        "TaskEx2": "",
        "TaskEx3": "",
        "TaskEx4": "",
        "TaskEx5": "",
        "TaskEx6": "",
        "TaskEx7": "",
        "TaskEx8": "",
        "TaskEx9": ""
    },
    "ComFra": 0,
    "IsSub": true,
    "Purged": false,
    "Mach": "station1-hydra-home",
    "Date": "2024-02-25T23:28:42.657-08:00",
    "DateStart": "0001-01-01T00:00:00Z",
    "DateComp": "0001-01-01T00:00:00Z",
    "Plug": "Command",
    "OutDir": [],
    "OutFile": [],
    "TileFile": [],
    "Main": false,
    "MainStart": 0,
    "MainEnd": 0,
    "Tile": false,
    "TileFrame": 0,
    "TileCount": 0,
    "TileX": 0,
    "TileY": 0,
    "Stat": 1,
    "Aux": [],
    "Bad": [],
    "CompletedChunks": 0,
    "QueuedChunks": 10,
    "SuspendedChunks": 0,
    "RenderingChunks": 0,
    "FailedChunks": 0,
    "PendingChunks": 0,
    "SnglTskPrg": "0 %",
    "Errs": 0,
    "DataSize": -1,
    "ConcurrencyToken": null,
    "_id": "65dc3daaa34cc12b6e5102e4",
    "ExtraElements": null
}

import enum

class AutoJobCleanupType(enum.Enum):
    DeleteJobs = "DeleteJobs"
    ArchiveJobs = "ArchiveJobs"

class JobCompleteAction(enum.Enum):
    Archive = "Archive"
    Delete = "Delete"
    Nothing = "Nothing"

class JobStatus(enum.Enum):
    Unknown = 0
    Active = 1
    Suspended = 2
    Completed = 3
    Failed = 4
    Pending = 6

class TaskOnTimeout(enum.Enum):
    ErrorAndNotify = "ErrorAndNotify"
    Error = "Error"
    Notify = "Notify"
    Complete = "Complete"
    RequeueAndNotify = "RequeueAndNotify"
    Requeue = "Requeue"
    FailAndNotify = "FailAndNotify"
    Fail = "Fail"

class JobScheduledType(enum.Enum):
    None_ = 0
    NotScheduled = None
    Once = 1
    Daily = 2
    Custom = 3

class JobInternalData(dict):
    """Instead of storing nested dicts, we store the
    configuration state as a flat dict, so that we
    can easily track the changeset."""

    def __init__(self) -> None:
        self.setupInternals()

    def setupInternals(self) -> None:
        """This defines the job defaults."""

        # Job General
        self.id = ""
        self.name = ""
        self.batch_name = ""
        self.priority = 0
        self.protected = False
        self.user_name = ""
        self.department = ""
        self.comment = ""
        self.frames = []
        self.frames_per_task = 1
        self.sequential = False
        self.on_job_complete = JobCompleteAction.Nothing
        # Job Environment
        self.env = {}
        self.use_job_environment_only = True
        # Job Info
        self.info = {}
        self.extra_info = {}
        self.extra_info_indexed = {}
        # Job Files
        self.output_directories = []
        self.output_file_names = []
        self.auxiliary_submission_file_names = []
        self.auxiliary_sync_all_files = False
        # Job Limits/Groups/Pools/Machines
        self.pool = ""
        self.secondary_pool = ""
        self.group = ""
        self.limit_groups = []
        self.whitelist_flag = False
        self.listed_slaves = []
        self.machine_limit = 0
        self.machine_limit_progress = 100.0
        self.remaining_time_threshold = 0
        # Job State
        self.status = JobStatus.Unknown
        self.send_job_error_warning = False
        self.override_job_failure_detection = False
        self.failure_detection_job_errors = 0
        self.interruptable = False
        self.interruptable_percentage = 100
        self.min_render_time_seconds = 0
        self.enable_auto_timeout = False
        self.enable_frame_timeouts = False
        self.failure_detection_task_errors = 0
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
        self.task_extra_info_name_index = {}
        self.plugin = ""
        self.plugin_info = {}
        self.force_reload_plugin = False
        self.custom_plugin_directory = ""
        # Job Event Plugins
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
        self.maintenance_job_end_frame = 1
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

class Job(object):
    def __init__(self) -> None:
        self._data = JobInternalData()

    def _GetJobExtraInfoIndex(self, idx: int):
        return self._data.extra_info_indexed.get(idx, None)

    def _SetJobExtraInfoIndex(self, idx: int, value: str):
        if value is None:
            self._data.extra_info_indexed.pop(idx, None)
        else:
            self._data.extra_info_indexed[idx] = value

    def _GetJobTaskExtraInfoNameIndex(self, idx: int):
        return self._data.task_extra_info_name_index.get(idx, None)

    def _SetJobTaskExtraInfoNameIndex(self, idx: int, value: str):
        if value is None:
            self._data.task_extra_info_name_index.pop(idx, None)
        else:
            self._data.task_extra_info_name_index[idx] = value

    #########################################
    # Deadline Scripting API
    # This is a 1:1 Job Class compatibility layer.
    # Differences:
    #   JobOnJobComplete -> Signature Enum JobCompleteAction
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
        return self._data.batch_name

    @JobBatchName.setter
    def JobBatchName(self, value):
        self._data.batch_name = value

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
        return self._data.user_name

    @JobUserName.setter
    def JobUserName(self, value: str):
        self._data.user_name = value

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
        return self._data.on_job_complete
    
    @JobOnJobComplete.setter
    def JobOnJobComplete(self, value: str):
        self._data.on_job_complete = JobCompleteAction(value)

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
        return self._data.use_job_environment_only

    @JobUseJobEnvironmentOnly.setter
    def JobUseJobEnvironmentOnly(self, value: bool):
        self._data.use_job_environment_only = value

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
        return self._data.extra_info.keys()

    def GetJobExtraInfoKeyValue(self, key: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
        Returns:
            str | None: The value.
        """
        return self._data.extra_info.get(key, None)

    def GetJobExtraInfoKeyValueWithDefault(self, key: str, defaultValue: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key name.
            defaultValue (str): The fallback value if the key doesn't exist.
        Returns:
            str: The value.
        """
        return self._data.extra_info.get(key, defaultValue)

    def SetJobExtraInfoKeyValue(self, key: str, value: str):
        """Sets the extra info value for the given key.
        Args:
            key (str): The key name.
            value (str): The value.
        """
        self._data.extra_info[key] = value

    def DeleteJobExtraInfoKey(self, key: str):
        """Deletes the extra info for the given key.
        Args:
            key (str): The key name.
        """
        self._data.extra_info.pop(key, None)

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
        return self._data.output_directories

    @property
    def JobOutputFileNames(self):
        """The list of output filenames.
        Returns:
            list[str]: A list of file names.
        """
        return self._data.output_file_names

    @property
    def JobAuxiliarySubmissionFileNames(self):
        """The auxiliary files submitted with the job.
        Returns:
            list[str]: Defaults to TimeSpan.MinValue
        """
        return self._data.auxiliary_submission_file_names

    @property
    def JobSynchronizeAllAuxiliaryFiles(self):
        """If the job's auxiliary files should be
        synced up by the Worker between tasks.
        Returns:
            bool: The sync state.
        """
        return self._data.auxiliary_sync_all_files

    @JobSynchronizeAllAuxiliaryFiles.setter
    def JobSynchronizeAllAuxiliaryFiles(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """
        self._data.auxiliary_sync_all_files = value

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
    def JobSecondaryPool(self, value: string):
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
        return self._data.limit_groups

    def SetJobLimitGroups(self, limitGroups: list[str]):
        """Sets the limit groups the job requires.
        Args:
            jobIds (list[int]): The key to get.
        """
        self._data.limit_groups = limitGroups

    @property
    def JobWhitelistFlag(self):
        """If the job's listed Workers are an allow
        list or a deny list.
        Returns:
            bool:
        """
        return self._data.whitelist_flag

    @property
    def JobListedSlaves(self):
        """The list of Workers in allow or deny list for
        the job. Use JobWhitelistFlag to determine if the
        list is a deny list or an allow list.

        Returns:
            list[str]:
        """
        return self._data.listed_slaves

    @property
    def JobMachineLimit(self):
        """The machine limit for the job.
        Returns:
            int:
        """
        return self._data.machine_limit

    @property
    def JobMachineLimitProgress(self):
        """When the Worker reaches this progress for
        the job's task, it will release the limit group.
        Returns:
            double:
        """
        return self._data.machine_limit_progress

    @property
    def RemTimeThreshold(self):
        """The remaining time (in seconds) that this Job
        must have left more than in order to be interruptable.
        Returns:
            int:
        """
        return self._data.remaining_time_threshold

    @RemTimeThreshold.setter
    def RemTimeThreshold(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.remaining_time_threshold = value

    # Job State
    @property
    def JobStatus(self):
        """The job's current state.
        Returns:
            str:
        """
        return self._data.status

    @property
    def JobSendJobErrorWarning(self):
        """If the job should send warning notifications when it
        reaches a certain number of errors.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.send_job_error_warning

    @JobSendJobErrorWarning.setter
    def JobSendJobErrorWarning(self, value: bool):
        self._data.send_job_error_warning = value

    @property
    def JobOverrideJobFailureDetection(self):
        """Whether or not this job overrides the Job
        Failure Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.override_job_failure_detection

    @JobOverrideJobFailureDetection.setter
    def JobOverrideJobFailureDetection(self, value: bool):
        self._data.override_job_failure_detection = value

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
        return self._data.failure_detection_job_errors

    @JobFailureDetectionJobErrors.setter
    def JobFailureDetectionJobErrors(self, value: int):
        self._data.failure_detection_job_errors = value

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
        return self._data.interruptable_percentage

    @JobInterruptiblePercentage.setter
    def JobInterruptiblePercentage(self, value: int):
        self._data.interruptable_percentage = value

    @property
    def JobMinRenderTimeSeconds(self):
        """The minimum number of seconds a job must run
        to be considered successful.
        Args:
            value (int)
        Returns:
            int:
        """
        return self._data.min_render_time_seconds

    @JobMinRenderTimeSeconds.setter
    def JobMinRenderTimeSeconds(self, value: int):
        self._data.min_render_time_seconds = value

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
        return self._data.enable_auto_timeout

    @JobEnableAutoTimeout.setter
    def JobEnableAutoTimeout(self, value: bool):
        self._data.enable_auto_timeout = value

    @property
    def JobEnableFrameTimeouts(self):
        """If the timeouts are Frame based instead of Task based.
        Args:
            value (bool)
        Returns:
            bool:
        """
        return self._data.enable_frame_timeouts

    @JobEnableFrameTimeouts.setter
    def JobEnableFrameTimeouts(self, value: bool):
        self._data.enable_frame_timeouts = value

    @property
    def JobFailureDetectionTaskErrors(self):
        """If JobOverrideTaskFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a task failure.
        Returns:
            int:
        """
        return self._data.failure_detection_task_errors

    @JobFailureDetectionTaskErrors.setter
    def JobFailureDetectionTaskErrors(self, value: int):
        """See getter.
        Args:
            value (int)
        """
        self._data.failure_detection_task_errors = value

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

    def SetJobRequiredAssets(self, assets: list[Assets]):
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
    def JobScheduledType(self, value: string):
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