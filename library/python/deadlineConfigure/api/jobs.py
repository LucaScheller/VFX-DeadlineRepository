
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


class JobInternalData(dict):
    """Instead of storing nested dicts, we store the
    configuration state as a flat dict, so that we
    can easily track the changeset."""

    def __init__(self) -> None:
        pass


class Job(object):
    def __init__(self) -> None:
        self._data = JobInternalData()

    #########################################
    # Deadline Scripting API
    # This is a 1:1 Job Class compatibility layer.
    #########################################
    
    # Job General
    @property
    def JobId(self):
        """The job's ID.
        Returns:
            str:
        """

    @property
    def JobName(self):
        """The job's name.
        Returns:
            str:
        """

    @JobName.setter
    def JobName(self, value: str):
        """See getter.
        Args:
            value (str)
        """
    
    @property
    def JobBatchName(self):
        """The name of the Batch that this job belongs to.
        Returns:
            str:
        """

    @JobBatchName.setter
    def JobBatchName(self, value):
        """The name of the Batch that this job belongs to."""

    @property
    def JobPriority(self):
        """The job's priority (0 is the lowest).
        Returns:
            int:
        """

    @JobPriority.setter
    def JobPriority(self, value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobProtected(self):
        """If set to True, the job can only be deleted or
        archived by the job's user, or by someone who has
        permissions to handle protected jobs.

        Returns:
            bool:
        """

    @JobProtected.setter
    def JobProtected(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobUserName():
        """The user that submitted the job.
        Returns:
            str:
        """

    @JobUserName.setter
    def JobUserName(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobDepartment(self):
        """The department to which the job's user belongs to.
        Returns:
            str:
        """

    @JobDepartment.setter
    def JobDepartment(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobComment(self):
        """A brief comment about the job.
        Returns:
            str:
        """

    @JobComment.setter
    def JobComment(self, value):
        """See getter.
        Args:
            value (str)
        """
    @property
    def JobFrames(self):
        """The job's frame list as a string.
        Returns:
            str:
        """

    @property
    def JobFramesList(self):
        """The job's frame list as an array.
        Returns:
            str:
        """

    @JobFramesList.setter
    def JobFramesList(self, value: list[int]):
        """See getter.
        Args:
            value (list[int])
        """

    @property
    def JobFramesPerTask(self):
        """The number of frames per task.
        Returns:
            int:
        """

    @property
    def JobSequentialJob(self):
        """If the job is a sequential job, which ensures
        its tasks only render in ascending order.
        Returns:
            bool:
        """

    @JobSequentialJob.setter
    def JobSequentialJob(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobOnJobComplete(self):
        """What the job should do when it completes.
        The options are "Archive", "Delete", or "Nothing".
        Returns:
            str:
        """

    @JobOnJobComplete.setter
    def JobOnJobComplete(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    # Job Environment
    def GetJobEnvironmentKeys(self):
        """Gets the keys for the job's environment variable entries.
        Returns:
            list[str]: A list of keys
        """

    def GetJobEnvironmentKeyValue(self, key: str):
        """Gets the environment variable value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def SetJobEnvironmentKeyValue(self, key: str, value: str):
        """Sets the environment variable value for the given key.
        Args:
            key (str):
            value (str):
        """

    def DeleteJobEnvironmentKey(self, key: str):
        """Deletes the environment variable for the given key.
        Args:
            key (str): The key to delete.
        """

    @property
    def JobUseJobEnvironmentOnly(self):
        """If only the job's environment variables should
        be used. If disabled, the job's environment will
        be merged with the current environment.
        Returns:
            bool:
        """

    @JobUseJobEnvironmentOnly.setter
    def JobUseJobEnvironmentOnly(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    # Job Info
    def GetJobInfoKeys(self):
        """Gets the job info keys.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobInfoKeyValue(self, key: str):
        """Get the job infor value for the provided key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    # Job (Extra) Info
    def GetJobExtraInfoKeys(self):
        """Gets the keys for the job's extra info entries.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobExtraInfoKeyValue(self, key: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def GetJobExtraInfoKeyValueWithDefault(self, key: str, defaultValue: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def SetJobExtraInfoKeyValue(self, key: str, value: str):
        """Sets the extra info value for the given key.
        Args:
            jobIds (list[int]): The key to get.
        """

    def DeleteJobExtraInfoKey(self, key: str):
        """Deletes the extra info for the given key.
        Args:
            key (str): The key to delete.
        """

    @property
    def JobExtraInfo0(self):
        """One of the Job's ten Extra Info fields.
        Returns:
            bool:
        """

    @JobExtraInfo0.setter
    def JobExtraInfo0(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    # Job Files
    @property
    def JobOutputDirectories():
        """The list of output directories.
        Returns:
            list[str]:
        """

    @property
    def JobOutputFileNames():
        """The list of output filenames.
        Returns:
            list[str]:
        """

    @property
    def JobAuxiliarySubmissionFileNames():
        """The auxiliary files submitted with the job.
        Returns:
            list[str]: Defaults to TimeSpan.MinValue
        """

    @property
    def JobSynchronizeAllAuxiliaryFiles():
        """If the job's auxiliary files should be
        synced up by the Worker between tasks.
        Returns:
            bool:
        """

    @JobSynchronizeAllAuxiliaryFiles.setter
    def JobSynchronizeAllAuxiliaryFiles(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    # Job Limits/Groups/Pools - Machine
    @property
    def JobPool(self):
        """The job's pool.
        Returns:
            str:
        """

    @JobPool.setter
    def JobPool(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobSecondaryPool():
        """The Secondary Pool in which this Job belongs.
        Returns:
            string:
        """

    @JobSecondaryPool.setter
    def JobSecondaryPool(value: string):
        """See getter.
        Args:
            value (string)
        """

    @property
    def JobGroup(self):
        """The job's group.
        Returns:
            str:
        """

    @JobGroup.setter
    def JobGroup(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobLimitGroups(self):
        """The limit groups the job requires.
        Returns:
            list[str]:
        """

    def SetJobLimitGroups(limitGroups: list[str]):
        """Sets the limit groups the job requires.
        Args:
            jobIds (list[int]): The key to get.
        """

    @property
    def JobWhitelistFlag(self):
        """If the job's listed Workers are an allow
        list or a deny list.
        Returns:
            bool:
        """

    @property
    def JobListedSlaves(self):
        """The list of Workers in allow or deny list for
        the job. Use JobWhitelistFlag to determine if the
        list is a deny list or an allow list.

        Returns:
            list[str]:
        """

    @property
    def JobMachineLimit(self):
        """The machine limit for the job.
        Returns:
            int:
        """

    @property
    def JobMachineLimitProgress(self):
        """When the Worker reaches this progress for
        the job's task, it will release the limit group.
        Returns:
            double:
        """

    @property
    def RemTimeThreshold(self):
        """The remaining time (in seconds) that this Job
        must have left more than in order to be interruptible.
        Returns:
            int:
        """

    @RemTimeThreshold.setter
    def RemTimeThreshold(self, value: int):
        """See getter.
        Args:
            value (int)
        """

    # Job State
    @property
    def JobStatus(self):
        """The job's current state.
        Returns:
            str:
        """

    @property
    def JobSendJobErrorWarning(self):
        """If the job should send warning notifications when it
        reaches a certain number of errors.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobSendJobErrorWarning.setter
    def JobSendJobErrorWarning(value: bool):
        pass

    @property
    def JobOverrideJobFailureDetection(self):
        """Whether or not this job overrides the Job
        Failure Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobOverrideJobFailureDetection.setter
    def JobOverrideJobFailureDetection(self, value: bool):
        pass

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

    @JobFailureDetectionJobErrors.setter
    def JobFailureDetectionJobErrors(self, value: int):
        pass

    @property
    def JobInterruptible():
        """If the job is interruptible, which causes it
        to be canceled when a job with higher priority comes along.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobInterruptible.setter
    def JobInterruptible(value: bool):
        pass

    @property
    def JobInterruptiblePercentage():
        """The completion percentage that this Job must
        be less than in order to be interruptible.
        Args:
            value (int)
        Returns:
            int:
        """

    @JobInterruptiblePercentage.setter
    def JobInterruptiblePercentage(value: int):
        pass

    @property
    def JobMinRenderTimeSeconds():
        """The minimum number of seconds a job must run
        to be considered successful.
        Args:
            value (int)
        Returns:
            int:
        """

    @JobMinRenderTimeSeconds.setter
    def JobMinRenderTimeSeconds(value: int):
        pass

    @property
    def JobEnableAutoTimeout():
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

    @JobEnableAutoTimeout.setter
    def JobEnableAutoTimeout(value: bool):
        pass

    @property
    def JobEnableFrameTimeouts():
        """If the timeouts are Frame based instead of Task based.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobEnableFrameTimeouts.setter
    def JobEnableFrameTimeouts(value: bool):
        pass

    @property
    def JobFailureDetectionTaskErrors():
        """If JobOverrideTaskFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a task failure.
        Returns:
            int:
        """

    @JobFailureDetectionTaskErrors.setter
    def JobFailureDetectionTaskErrors(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobIgnoreBadSlaveDetection():
        """Whether or not this job overrides the Bad Worker Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobIgnoreBadSlaveDetection.setter
    def JobIgnoreBadSlaveDetection(value: bool):
        pass

    @property
    def JobOverrideTaskFailureDetection():
        """Whether or not this job overrides the Task Failure
        Detection settings in the Repository Options.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobOverrideTaskFailureDetection.setter
    def JobOverrideTaskFailureDetection(value: bool):
        pass

    @property
    def JobStartJobTimeoutSeconds(self):
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int)
        Returns:
            int:
        """

    @JobStartJobTimeoutSeconds.setter
    def JobStartJobTimeoutSeconds(self, value: int):
        pass

    @property
    def JobInitializePluginTimeoutSeconds():
        """The timespan a job's task has to start before a timeout occurs.
        Args:
            value (int)
        Returns:
            int:
        """

    @JobInitializePluginTimeoutSeconds.setter
    def JobInitializePluginTimeoutSeconds(value: int):
        pass

    @property
    def JobTaskTimeoutSeconds(self):
        """The timespan a job's task has to render before
        a timeout occurs.
        Returns:
            int:
        """

    @JobTaskTimeoutSeconds.setter
    def JobTaskTimeoutSeconds(self, value: int):
        pass

    @property
    def JobOnTaskTimeout(self):
        """What to do when a task times out.
        The options are "Error", "Notify", or "Both".
        Args:
            value (str)
        Returns:
            str:
        """

    @JobOnTaskTimeout.setter
    def JobOnTaskTimeout(self, value: str):
        pass


    # Job Tasks
    @property
    def JobConcurrentTasks(self):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Returns:
            int:
        """

    @JobConcurrentTasks.setter
    def JobConcurrentTasks(self, value: int):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Args:
            value (int)
        """

    @property
    def JobLimitTasksToNumberOfCpus(self):
        """Whether or not the number of concurrent tasks
        a Worker can dequeue for this job should be limited
        to the number of CPUs the Worker has.
        Returns:
            bool:
        """

    @JobLimitTasksToNumberOfCpus.setter
    def JobLimitTasksToNumberOfCpus(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobOverrideTaskExtraInfoNames():
        """Whether this job overrides the task extra info names.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobOverrideTaskExtraInfoNames.setter
    def JobOverrideTaskExtraInfoNames(value: bool):
        pass

    @property
    def JobTaskExtraInfoName0(self):
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """

    @JobTaskExtraInfoName0.setter
    def JobTaskExtraInfoName0(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    # Job Plugin
    @property
    def JobPlugin(self):
        """The name of the Deadline plugin the job uses.
        Returns:
            str:
        """

    @JobPlugin.setter
    def JobPlugin(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    def GetJobPluginInfoKeys(self):
        """Gets the keys for the job's plugin info entries.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobPluginInfoKeyValue(self, key: str):
        """Gets the plugin info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """
    
    def SetJobPluginInfoKeyValue(self, key: str, value: str):
        """Sets the plugin info value for the given key.
        Args:
            key (str):
            value (str):
        """

    @property
    def JobForceReloadPlugin(self):
        """Whether or not the job's plugin should be
        reloaded between tasks.
        Returns:
            bool:
        """

    @JobForceReloadPlugin.setter
    def JobForceReloadPlugin(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobCustomPluginDirectory(self):
        """A custom location to load the job's plugin from.
        Returns:
            str:
        """

    @JobCustomPluginDirectory.setter
    def JobCustomPluginDirectory(self, value: str):
        """A custom location to load the job's plugin from.
        Args:
            value (str)
        """

    # Job Event Plugins
    @property
    def JobSuppressEvents():
        """Whether or not this Job should suppress Events plugins.
        Returns:
            bool:
        """

    @JobSuppressEvents.setter
    def JobSuppressEvents(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobCustomEventPluginDirectory(self):
        """A custom location to load the job's event plugin from.
        Returns:
            str:
        """

    @JobCustomEventPluginDirectory.setter
    def JobCustomEventPluginDirectory(self, value: str):
        """A custom location to load the job's event plugin from.
        Args:
            value (str)
        """

    # Job Pre/Post (Task) Scripts
    @property
    def JobPreJobScript(self):
        """The script to execute before the job starts. Read Only.
        Use RepositoryUtils.SetPreJobScript and RepositoryUtils.DeletePreJobScript.
        Returns:
            str:
        """

    @property
    def JobPostJobScript(self):
        """The script to execute after the Job finishes. Read Only.
        Use RepositoryUtils.SetPostJobScript and RepositoryUtils.DeletePostJobScript.

        Returns:
            string:
        """

    @property
    def JobPreTaskScript(self):
        """The script to execute before a job task starts.
        Returns:
            str:
        """

    @JobPreTaskScript.setter
    def JobPreTaskScript(self, value: str):
        """The script to execute before a job task starts.
        Args:
            value (str):
        """
    
    @property
    def JobPostTaskScript(self):
        """The script to execute when a job task is complete.
        Returns:
            str:
        """

    @JobPostTaskScript.setter
    def JobPostTaskScript(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobEnableTimeoutsForScriptTasks():
        """If the timeouts should apply to pre/post job script tasks.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobEnableTimeoutsForScriptTasks.setter
    def JobEnableTimeoutsForScriptTasks(value: bool):
        pass

    # Job Dependencies
    @property
    def JobResumeOnCompleteDependencies(self):
        """If the job should resume on complete dependencies.
        Returns:
            bool:
        """

    @JobResumeOnCompleteDependencies.setter
    def JobResumeOnCompleteDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobResumeOnDeletedDependencies(self):
        """If the job should resume on deleted dependencies.
        Returns:
            bool:
        """

    @JobResumeOnDeletedDependencies.setter
    def JobResumeOnDeletedDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobResumeOnFailedDependencies(self):
        """If the job should resume on failed dependencies.
        Returns:
            bool:
        """

    @JobResumeOnFailedDependencies.setter
    def JobResumeOnFailedDependencies(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobDependencyPercentageValue(self):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Returns:
            float:
        """

    @JobDependencyPercentageValue.setter
    def JobDependencyPercentageValue(self, value: float):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Args:
            value (float)
        """

    @property
    def JobIsFrameDependent(self):
        """If the job is frame dependent.
        Returns:
            bool:
        """

    @JobIsFrameDependent.setter
    def JobIsFrameDependent(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobFrameDependencyOffsetStart(self):
        """The start offset for frame depenencies.
        Returns:
            int:
        """

    @JobFrameDependencyOffsetStart.setter
    def JobFrameDependencyOffsetStart(self, value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobFrameDependencyOffsetEnd(self):
        """The end offset for frame depenencies.
        Returns:
            int:
        """

    @JobFrameDependencyOffsetEnd.setter
    def JobFrameDependencyOffsetEnd(self, value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobDependencyIDs(self):
        """The ids of the jobs that this job is dependent on.
        Returns:
            list[str]:
        """

    def SetJobDependencyIDs(self, jobIds: list[int]):
        """Sets the IDs of the jobs that this job is dependent on.
        Args:
            jobIds (list[int]): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    @property
    def JobRequiredAssets(self):
        """The assets that are required in order to render this job.
        The assets should contain absolute paths. More...

        Returns:
            list[AssetDependency]:
        """

    def SetJobRequiredAssets(self, assets: list[Assets]):
        """Sets the assets that are required in order to render this job. The assets should contain absolute paths.
        Args:
            assets (list[Asset]):
        """

    @property
    def JobScriptDependencies(self):
        """The scripts that must return True in order to render this job.
        Returns:
            list[ScriptDependency]:
        """

    def SetScriptDependencies(self, scripts: list[Script]):
        """Sets the scripts that must return True in order to render this job.
        Args:
            scripts (list[Script]):
        """

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

    @JobOverrideAutoJobCleanup.setter
    def JobOverrideAutoJobCleanup(self, value: bool):
        pass

    @property
    def AutoJobCleanupType(self):
        """The job cleanup mode. Only relevant if
        the override is set.
        Args:
            value (str)
        Returns:
            str:
        """

    @AutoJobCleanupType.setter
    def AutoJobCleanupType(self, value: str):
        pass

    @property
    def JobOverrideJobCleanup():
        """If the job overrides the amount of days
        before its cleaned up.
        Args:
            value (bool)
        Returns:
            bool:
        """

    @JobOverrideJobCleanup.setter
    def JobOverrideJobCleanup(value: bool):
        pass

    @property
    def JobOverrideJobCleanupDays():
        """The number of days before this job will be
        cleaned up after it is completed. Only relevant
        if the override is set.
        Args:
            value (int)
        Returns:
            int:
        """

    @JobOverrideJobCleanupDays.setter
    def JobOverrideJobCleanupDays(value: int):
        pass

    # Job Stats
    @property
    def JobSubmitDateTime(self):
        """The date/time at which the job was submitted.
        Returns:
            DateTime:
        """

    @property
    def JobSubmitMachine(self):
        """This is the machine that the job was submitted from.
        Returns:
            str:
        """

    @property
    def JobStartedDateTime():
        """The date/time at which the job started rendering.
        Returns:
            DateTime:
        """

    @property
    def JobCompletedDateTime():
        """The date/time at which the job finished rendering.
        Returns:
            DateTime:
        """

    @property
    def JobTaskCount(self):
        """The number of tasks the job has.
        Returns:
            int:
        """

    @property
    def JobQueuedTasks(self):
        """The number of tasks in the queued state.
        Returns:
            int:
        """

    @property
    def JobRenderingTasks(self):
        """The number of tasks in the active state.
        Returns:
            int:
        """

    @property
    def JobPendingTasks(self):
        """The number of tasks in the pending state.
        Returns:
            int:
        """

    @property
    def JobCompletedTasks(self):
        """The number of tasks in the completed state.
        Returns:
            int:
        """

    @property
    def JobSuspendedTasks(self):
        """The number of tasks in the suspended state.
        Returns:
            int:
        """

    @property
    def JobFailedTasks(self):
        """The number of tasks in the failed state.
        Returns:
            int:
        """

    # Job Notifications
    @property
    def JobOverrideNotificationMethod():
        """If the user's notification method should be ignored.
        Returns:
            bool:
        """

    @JobOverrideNotificationMethod.setter
    def JobOverrideNotificationMethod(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobNotificationTargets(self):
        """The list of users that are to be
        notified when this job is complete.
        Returns:
            list[str]:
        """

    def SetJobNotificationTargets(self, userNames: list[str]):
        """Sets the list of users that are to be notified when this job is complete.
        Args:
            userNames (list[str]):
        """

    @property
    def JobEmailNotification(self):
        """If overriding the user's notification method, whether to use email notification.
        Returns:
            bool:
        """

    @JobEmailNotification.setter
    def JobEmailNotification(self, value: bool):
        """If overriding the user's notification method, whether to use email notification.
        Args:
            value (bool)
        """

    @property
    def JobNotificationEmails(self):
        """Arbitrary email addresses to send notifications
        to when this job is complete.
        Returns:
            list[str]:
        """

    def SetJobNotificationEmails(self, emails: list[str]):
        """Sets the arbitrary email addresses to send notifications to when this job is complete.
        Args:
            jobIds (list[int]):
        """

    @property
    def JobNotificationNote(self):
        """A note to append to the notification email
        sent out when the job is complete.
        Returns:
            str:
        """

    @JobNotificationNote.setter
    def JobNotificationNote(self, value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobPopupNotification(self):
        """If overriding the user's notification method,
        whether to use send a popup notification.
        Returns:
            bool:
        """

    @JobPopupNotification.setter
    def JobPopupNotification(self, value: bool):
        """See getter.
        Args:
            value (bool)
        """

    # Job Maintenance
    @property
    def JobMaintenanceJob(self):
        """If this is a maintenance job.
        Returns:
            bool:
        """

    @property
    def JobMaintenanceJobEndFrame(self):
        """The start frame for a maintenance job.
        Returns:
            int:
        """

    @property
    def JobMaintenanceJobStartFrame(self):
        """The start frame for a maintenance job.
        Returns:
            int:
        """

    # Job Time Schedule
    @property
    def JobScheduledType(self):
        """The scheduling mode for this job.
        The options are "None", "Once", "Daily". or "Custom".
        Returns:
            string: "None", "Once", "Daily" or "Custom"
        """

    @JobScheduledType.setter
    def JobScheduledType(self, value: string):
        """See getter.
        Args:
            value (string)
        """

    @property
    def JobScheduledDays(self):
        """The day interval for daily scheduled jobs.
        Returns:
            int:
        """

    @JobScheduledDays.setter
    def JobScheduledDays(self, value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobSheduledStartDateTime(self):
        """The start date/time at which the scheduled job should start.
        Returns:
            DateTime:
        """

    @JobSheduledStartDateTime.setter
    def JobSheduledStartDateTime(self, value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """

    @property
    def JobScheduledStopDateTime(self):
        """The stop date/time at which the job should stop if it's still active.
        Returns:
            DateTime:
        """

    @JobScheduledStopDateTime.setter
    def JobScheduledStopDateTime(self, value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """

    @property
    def DisabledScheduleTime(self):
        """Represents a disabled scheduled time for custom job scheduling settings.
        Returns:
            TimeSpan: Defaults to TimeSpan.MinValue
        """

    @property
    def JobMondayStartTime(self):
        """Gets or sets Monday's start time.
        Returns:
            TimeSpan:
        """

    @JobMondayStartTime.setter
    def JobMondayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobMondayStopTime(self):
        """Gets or sets Monday's stop time.
        Returns:
            TimeSpan:
        """

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

    @JobTuesdayStartTime.setter
    def JobTuesdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobTuesdayStopTime(self):
        """Gets or sets Tuesday's stop time.
        Returns:
            TimeSpan:
        """

    @JobTuesdayStopTime.setter
    def JobTuesdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobWednesdayStartTime(self):
        """Gets or sets Wednesday's start time.
        Returns:
            TimeSpan:
        """

    @JobWednesdayStartTime.setter
    def JobWednesdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobWednesdayStopTime(self):
        """Gets or sets Wednesday's stop time.
        Returns:
            TimeSpan:
        """

    @JobWednesdayStopTime.setter
    def JobWednesdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobThursdayStartTime(self):
        """Gets or sets Thursday's start time.
        Returns:
            TimeSpan:
        """

    @JobThursdayStartTime.setter
    def JobThursdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobThursdayStopTime(self):
        """Gets or sets Thursday's stop time.
        Returns:
            TimeSpan:
        """

    @JobThursdayStartTime.setter
    def JobThursdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobFridayStartTime(self):
        """Gets or sets Friday's start time.
        Returns:
            TimeSpan:
        """

    @JobFridayStartTime.setter
    def JobFridayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobFridayStopTime(self):
        """Gets or sets Friday's stop time.
        Returns:
            TimeSpan:
        """

    @JobFridayStopTime.setter
    def JobFridayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSaturdayStartTime(self):
        """Gets or sets Saturday's start time.
        Returns:
            TimeSpan:
        """

    @JobSaturdayStartTime.setter
    def JobSaturdayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSaturdayStopTime(self):
        """Gets or sets Saturday's stop time.
        Returns:
            TimeSpan:
        """

    @JobSaturdayStopTime.setter
    def JobSaturdayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSundayStartTime(self):
        """Gets or sets Sunday's start time.
        Returns:
            TimeSpan:
        """

    @JobSundayStartTime.setter
    def JobSundayStartTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSundayStopTime(self):
        """Gets or sets Sunday's stop time.
        Returns:
            TimeSpan:
        """

    @JobSundayStopTime.setter
    def JobSundayStopTime(self, value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    # Job Tile Rendering   
    @property
    def JobTileJob(self):
        """If this job is a tile job.
        Returns:
            bool:
        """

    @property
    def JobTileJobFrame(self):
        """The frame that the tile job is rendering.
        Returns:
            int:
        """

    @property
    def JobTileJobTileCount(self):
        """The number of tiles in a tile job.
        Returns:
            int:
        """

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