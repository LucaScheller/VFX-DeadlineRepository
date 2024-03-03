class Job(object):

    def DeleteJobEnvironmentKey(key: str):
        """Deletes the environment variable for the given key.
        Args:
            key (str): The key to delete.
        Returns:
            void
        """

    def DeleteJobExtraInfoKey(key: str):
        """Deletes the extra info for the given key.
        Args:
            key (str): The key to delete.
        Returns:
            void
        """

    def GetJobEnvironmentKeys():
        """Gets the keys for the job's environment variable entries.
        Returns:
            list[str]: A list of keys
        """

    def GetJobEnvironmentKeyValue(key: str):
        """Gets the environment variable value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def GetJobExtraInfoKeys():
        """Gets the keys for the job's extra info entries.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobExtraInfoKeyValue(key: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def GetJobExtraInfoKeyValueWithDefault(key: str, defaultValue: str):
        """Gets the extra info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def GetJobInfoKeys():
        """Gets the job info keys.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobInfoKeyValue(key: str):
        """Get the job infor value for the provided key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def GetJobPluginInfoKeys():
        """Gets the keys for the job's plugin info entries.
        Returns:
            list[str]: The value of the env var.
        """

    def GetJobPluginInfoKeyValue(key: str):
        """Gets the plugin info value for the given key.
        Args:
            key (str): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def SetJobDependencyIDs(jobIds: list[int]):
        """Sets the IDs of the jobs that this job is dependent on.
        Args:
            jobIds (list[int]): The key to get.
        Returns:
            str | None: The value of the env var.
        """

    def SetJobEnvironmentKeyValue(key: str, value: str):
        """Sets the environment variable value for the given key.
        Args:
            key (str):
            value (str):
        """

    def SetJobExtraInfoKeyValue(key: str, value: str):
        """Sets the extra info value for the given key.
        Args:
            jobIds (list[int]): The key to get.
        """

    def SetJobLimitGroups(limitGroups: list[str]):
        """Sets the limit groups the job requires.
        Args:
            jobIds (list[int]): The key to get.
        """

    def SetJobNotificationEmails(emails: list[str]):
        """Sets the arbitrary email addresses to send notifications to when this job is complete.
        Args:
            jobIds (list[int]):
        """

    def SetJobNotificationTargets(userNames: list[str]):
        """Sets the list of users that are to be notified when this job is complete.
        Args:
            userNames (list[str]):
        """

    def SetJobPluginInfoKeyValue(key: str, value: str):
        """Sets the plugin info value for the given key.
        Args:
            key (str):
            value (str):
        """

    def SetJobRequiredAssets(assets: list[Assets]):
        """Sets the assets that are required in order to render this job. The assets should contain absolute paths.
        Args:
            assets (list[Asset]):
        """

    def SetScriptDependencies(scripts: list[Script]):
        """Sets the scripts that must return True in order to render this job.
        Args:
            scripts (list[Script]):
        """

    def SetScriptDependencies(scripts: list[Script]):
        """Sets the scripts that must return True in order to render this job.
        Args:
            scripts (list[Script]):
        """

    ### Public
    @property
    def DisabledScheduleTime():
        """Represents a disabled scheduled time for custom job scheduling settings.
        Returns:
            TimeSpan: Defaults to TimeSpan.MinValue
        """

    @property
    def JobAuxiliarySubmissionFileNames():
        """The auxiliary files submitted with the job.
        Returns:
            list[str]: Defaults to TimeSpan.MinValue
        """

    @property
    def JobBatchName():
        """The name of the Batch that this job belongs to.
        Returns:
            str:
        """

    @JobBatchName.setter
    def JobBatchName(value):
        """The name of the Batch that this job belongs to."""

    @property
    def JobComment():
        """A brief comment about the job.
        Returns:
            str:
        """

    @JobComment.setter
    def JobComment(value):
        """A brief comment about the job."""

    @property
    def JobCompletedDateTime():
        """The date/time at which the job finished rendering.
        Returns:
            DateTime:
        """

    @property
    def JobCompletedTasks():
        """The number of tasks in the completed state.
        Returns:
            int:
        """

    @property
    def JobConcurrentTasks():
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Returns:
            int:
        """

    @JobConcurrentTasks.setter
    def JobConcurrentTasks(value: int):
        """The maximum number of concurrent tasks a Worker can dequeue
        for this job at a time. The value must be between 1 and 16 inclusive.
        Args:
            value (int)
        """

    @property
    def JobCustomEventPluginDirectory():
        """A custom location to load the job's event plugin from.
        Returns:
            str:
        """

    @JobCustomEventPluginDirectory.setter
    def JobCustomEventPluginDirectory(value: str):
        """A custom location to load the job's event plugin from.
        Args:
            value (str)
        """

    @property
    def JobCustomPluginDirectory():
        """A custom location to load the job's plugin from.
        Returns:
            str:
        """

    @JobCustomPluginDirectory.setter
    def JobCustomPluginDirectory(value: str):
        """A custom location to load the job's plugin from.
        Args:
            value (str)
        """

    @property
    def JobDepartment():
        """A custom location to load the job's plugin from.
        Returns:
            str:
        """

    @JobDepartment.setter
    def JobDepartment(value: str):
        """The department to which the job's user belongs to.
        Args:
            value (str)
        """

    @property
    def JobDependencyIDs():
        """The ids of the jobs that this job is dependent on.
        Returns:
            list[str]:
        """

    @property
    def JobDependencyPercentageValue():
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Returns:
            float:
        """

    @JobDependencyPercentageValue.setter
    def JobDependencyPercentageValue(value: float):
        """This job will resume when its dependencies have completed this percentage of their tasks.
        Args:
            value (float)
        """

    @property
    def JobEmailNotification():
        """If overriding the user's notification method, whether to use email notification.
        Returns:
            bool:
        """

    @JobEmailNotification.setter
    def JobEmailNotification(value: bool):
        """If overriding the user's notification method, whether to use email notification.
        Args:
            value (bool)
        """

    @property
    def JobEnableAutoTimeout():
        """The Auto Task Timeout feature is based on the Auto Job Timeout
        Settings in the Repository Options. The timeout is based on the
        render times of the tasks that have already finished for this job,
        so this option should only be used if the frames for the job have
        consistent render times.

        Returns:
            bool:
        """

    @JobEnableAutoTimeout.setter
    def JobEnableAutoTimeout(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobEnableFrameTimeouts():
        """If the timeouts are Frame based instead of Task based.
        Returns:
            bool:
        """

    @JobEnableFrameTimeouts.setter
    def JobEnableFrameTimeouts(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobEnableTimeoutsForScriptTasks():
        """If the timeouts should apply to pre/post job script tasks.
        Returns:
            bool:
        """

    @JobEnableTimeoutsForScriptTasks.setter
    def JobEnableTimeoutsForScriptTasks(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobExtraInfo0():
        """One of the Job's ten Extra Info fields.
        Returns:
            bool:
        """

    @JobExtraInfo0.setter
    def JobExtraInfo0(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobFailedTasks():
        """The number of tasks in the failed state.
        Returns:
            int:
        """

    @property
    def JobFailureDetectionJobErrors():
        """If JobOverrideJobFailureDetection is enabled,
        this is the number of errors it takes to trigger
        a job failure.
        Returns:
            int:
        """

    @JobFailureDetectionJobErrors.setter
    def JobFailureDetectionJobErrors(value: int):
        """See getter.
        Args:
            value (int)
        """

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
    def JobForceReloadPlugin():
        """Whether or not the job's plugin should be
        reloaded between tasks.
        Returns:
            bool:
        """

    @JobForceReloadPlugin.setter
    def JobForceReloadPlugin(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobFrameDependencyOffsetEnd():
        """The end offset for frame depenencies.
        Returns:
            int:
        """

    @JobFrameDependencyOffsetEnd.setter
    def JobFrameDependencyOffsetEnd(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobFrameDependencyOffsetStart():
        """The start offset for frame depenencies.
        Returns:
            int:
        """

    @JobFrameDependencyOffsetStart.setter
    def JobFrameDependencyOffsetStart(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobFrames():
        """The job's frame list as a string.
        Returns:
            str:
        """

    @property
    def JobFramesList():
        """The job's frame list as an array.
        Returns:
            str:
        """

    @JobFramesList.setter
    def JobFramesList(value: list[int]):
        """See getter.
        Args:
            value (list[int])
        """

    @property
    def JobFramesPerTask():
        """The number of frames per task.
        Returns:
            int:
        """

    @property
    def JobFridayStartTime():
        """Gets or sets Friday's start time.
        Returns:
            TimeSpan:
        """

    @JobFridayStartTime.setter
    def JobFridayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobFridayStopTime():
        """Gets or sets Friday's stop time.
        Returns:
            TimeSpan:
        """

    @JobFridayStopTime.setter
    def JobFridayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobGroup():
        """The job's group.
        Returns:
            str:
        """

    @JobGroup.setter
    def JobGroup(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobId():
        """The job's ID.
        Returns:
            str:
        """

    @property
    def JobIgnoreBadSlaveDetection():
        """Whether or not this job overrides the Bad Worker Detection settings in the Repository Options.
        Returns:
            bool:
        """

    @JobIgnoreBadSlaveDetection.setter
    def JobIgnoreBadSlaveDetection(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobInitializePluginTimeoutSeconds():
        """The timespan a job's task has to start before a timeout occurs.
        Returns:
            int:
        """

    @JobInitializePluginTimeoutSeconds.setter
    def JobInitializePluginTimeoutSeconds(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobInterruptible():
        """If the job is interruptible, which causes it
        to be canceled when a job with higher priority comes along.
        Returns:
            bool:
        """

    @JobInterruptible.setter
    def JobInterruptible(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobInterruptiblePercentage():
        """The completion percentage that this Job must
        be less than in order to be interruptible.
        Returns:
            int:
        """

    @JobInterruptiblePercentage.setter
    def JobInterruptiblePercentage(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobIsFrameDependent():
        """If the job is frame dependent.
        Returns:
            bool:
        """

    @JobIsFrameDependent.setter
    def JobIsFrameDependent(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobLimitGroups():
        """The limit groups the job requires.
        Returns:
            list[str]:
        """

    @property
    def JobLimitTasksToNumberOfCpus():
        """Whether or not the number of concurrent tasks
        a Worker can dequeue for this job should be limited
        to the number of CPUs the Worker has.
        Returns:
            bool:
        """

    @JobLimitTasksToNumberOfCpus.setter
    def JobLimitTasksToNumberOfCpus(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobListedSlaves():
        """The list of Workers in allow or deny list for
        the job. Use JobWhitelistFlag to determine if the
        list is a deny list or an allow list.

        Returns:
            list[str]:
        """

    @property
    def JobMachineLimit():
        """The machine limit for the job.
        Returns:
            int:
        """

    @property
    def JobMachineLimitProgress():
        """When the Worker reaches this progress for
        the job's task, it will release the limit group.
        Returns:
            double:
        """

    @property
    def JobMaintenanceJob():
        """If this is a maintenance job.
        Returns:
            bool:
        """

    @property
    def JobMaintenanceJobEndFrame():
        """The start frame for a maintenance job.
        Returns:
            int:
        """

    @property
    def JobMaintenanceJobStartFrame():
        """The start frame for a maintenance job.
        Returns:
            int:
        """

    @property
    def JobMinRenderTimeSeconds():
        """The minimum number of seconds a job must run
        to be considered successful.
        Returns:
            int:
        """

    @JobMinRenderTimeSeconds.setter
    def JobMinRenderTimeSeconds(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobMondayStartTime():
        """Gets or sets Monday's start time.
        Returns:
            TimeSpan:
        """

    @JobMondayStartTime.setter
    def JobMondayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobMondayStopTime():
        """Gets or sets Monday's stop time.
        Returns:
            TimeSpan:
        """

    @JobMondayStopTime.setter
    def JobMondayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobName():
        """The job's name.
        Returns:
            str:
        """

    @JobName.setter
    def JobName(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobNotificationEmails():
        """Arbitrary email addresses to send notifications
        to when this job is complete.
        Returns:
            list[str]:
        """

    @property
    def JobNotificationNote():
        """A note to append to the notification email
        sent out when the job is complete.
        Returns:
            str:
        """

    @JobNotificationNote.setter
    def JobNotificationNote(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobNotificationTargets():
        """The list of users that are to be
        notified when this job is complete.
        Returns:
            list[str]:
        """

    @property
    def JobOnJobComplete():
        """What the job should do when it completes.
        The options are "Archive", "Delete", or "Nothing".
        Returns:
            str:
        """

    @JobOnJobComplete.setter
    def JobOnJobComplete(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobOnTaskTimeout():
        """What to do when a task times out.
        The options are "Error", "Notify", or "Both".
        Returns:
            str:
        """

    @JobOnTaskTimeout.setter
    def JobOnTaskTimeout(value: str):
        """See getter.
        Args:
            value (str)
        """

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
    def JobOutputTileFileNames():
        """The list of output filenames for tile jobs.
        Returns:
            list[str]:
        """

    @property
    def JobOverrideAutoJobCleanup():
        """If the job overrides the automatic job cleanup
        in the Repository Options.
        Returns:
            bool:
        """

    @JobOverrideAutoJobCleanup.setter
    def JobOverrideAutoJobCleanup(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobOverrideJobCleanup():
        """If the job overrides the amount of days
        before its cleaned up.
        Returns:
            bool:
        """

    @JobOverrideJobCleanup.setter
    def JobOverrideJobCleanup(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobOverrideJobCleanupDays():
        """The number of days before this job will be
        cleaned up after it is completed. Only relevant
        if the override is set.
        Returns:
            int:
        """

    @JobOverrideJobCleanupDays.setter
    def JobOverrideJobCleanupDays(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def AutoJobCleanupType():
        """The job cleanup mode. Only relevant if
        the override is set.
        Returns:
            str:
        """

    @AutoJobCleanupType.setter
    def AutoJobCleanupType(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobOverrideJobFailureDetection():
        """Whether or not this job overrides the Job
        Failure Detection settings in the Repository Options.
        Returns:
            bool:
        """

    @JobOverrideJobFailureDetection.setter
    def JobOverrideJobFailureDetection(value: bool):
        """See getter.
        Args:
            value (bool)
        """

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
    def JobOverrideTaskExtraInfoNames():
        """Whether this job overrides the task extra info names.
        Returns:
            bool:
        """

    @JobOverrideTaskExtraInfoNames.setter
    def JobOverrideTaskExtraInfoNames(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobOverrideTaskFailureDetection():
        """Whether or not this job overrides the Task Failure
        Detection settings in the Repository Options.
        Returns:
            bool:
        """

    @JobOverrideTaskFailureDetection.setter
    def JobOverrideTaskFailureDetection(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobPendingTasks():
        """The number of tasks in the pending state.
        Returns:
            int:
        """

    @property
    def JobPlugin():
        """The name of the Deadline plugin the job uses.
        Returns:
            str:
        """

    @JobPlugin.setter
    def JobPlugin(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobPool():
        """The job's pool.
        Returns:
            str:
        """

    @JobPool.setter
    def JobPool(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobPopupNotification():
        """If overriding the user's notification method,
        whether to use send a popup notification.
        Returns:
            bool:
        """

    @JobPopupNotification.setter
    def JobPopupNotification(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobPostJobScript():
        """The script to execute after the Job finishes. Read Only.
        Use RepositoryUtils.SetPostJobScript and RepositoryUtils.DeletePostJobScript.

        Returns:
            string:
        """

    @property
    def JobPostTaskScript():
        """The script to execute when a job task is complete.
        Returns:
            str:
        """

    @JobPostTaskScript.setter
    def JobPostTaskScript(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobPreJobScript():
        """The script to execute before the job starts. Read Only.
        Use RepositoryUtils.SetPreJobScript and RepositoryUtils.DeletePreJobScript.
        Returns:
            str:
        """

    @property
    def JobPreTaskScript():
        """The script to execute before a job task starts.
        Returns:
            str:
        """

    @JobPreTaskScript.setter
    def JobPreTaskScript(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobPriority():
        """The job's priority (0 is the lowest).
        Returns:
            int:
        """

    @JobPriority.setter
    def JobPriority(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobProtected():
        """If set to True, the job can only be deleted or
        archived by the job's user, or by someone who has
        permissions to handle protected jobs.

        Returns:
            bool:
        """

    @JobProtected.setter
    def JobProtected(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobQueuedTasks():
        """The number of tasks in the queued state.
        Returns:
            int:
        """

    @property
    def JobRenderingTasks():
        """The number of tasks in the active state.
        Returns:
            int:
        """

    @JobRenderingTasks.setter
    def JobRenderingTasks(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobRequiredAssets():
        """The assets that are required in order to render this job.
        The assets should contain absolute paths. More...

        Returns:
            list[AssetDependency]:
        """

    @property
    def JobResumeOnCompleteDependencies():
        """If the job should resume on complete dependencies.
        Returns:
            bool:
        """

    @JobResumeOnCompleteDependencies.setter
    def JobResumeOnCompleteDependencies(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobResumeOnDeletedDependencies():
        """If the job should resume on deleted dependencies.
        Returns:
            bool:
        """

    @JobResumeOnDeletedDependencies.setter
    def JobResumeOnDeletedDependencies(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobResumeOnFailedDependencies():
        """If the job should resume on failed dependencies.
        Returns:
            bool:
        """

    @JobResumeOnFailedDependencies.setter
    def JobResumeOnFailedDependencies(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobSaturdayStartTime():
        """Gets or sets Saturday's start time.
        Returns:
            TimeSpan:
        """

    @JobSaturdayStartTime.setter
    def JobSaturdayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSaturdayStopTime():
        """Gets or sets Saturday's stop time.
        Returns:
            TimeSpan:
        """

    @JobSaturdayStopTime.setter
    def JobSaturdayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobScheduledDays():
        """The day interval for daily scheduled jobs.
        Returns:
            int:
        """

    @JobScheduledDays.setter
    def JobScheduledDays(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobSheduledStartDateTime():
        """The start date/time at which the scheduled job should start.
        Returns:
            DateTime:
        """

    @JobSheduledStartDateTime.setter
    def JobSheduledStartDateTime(value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """

    @property
    def JobScheduledStopDateTime():
        """The stop date/time at which the job should stop if it's still active.
        Returns:
            DateTime:
        """

    @JobScheduledStopDateTime.setter
    def JobScheduledStopDateTime(value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """

    @property
    def JobScheduledType():
        """The scheduling mode for this job. The options are "None", "Once", "Daily". or "Custom".
        Returns:
            string:
        """

    @JobScheduledType.setter
    def JobScheduledType(value: string):
        """See getter.
        Args:
            value (string)
        """

    @property
    def JobScriptDependencies():
        """The scripts that must return True in order to render this job.
        Returns:
            list[ScriptDependency]:
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
    def JobSendJobErrorWarning():
        """If the job should send warning notifications when it
        reaches a certain number of errors.
        Returns:
            bool:
        """

    @JobSendJobErrorWarning.setter
    def JobSendJobErrorWarning(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobSequentialJob():
        """If the job is a sequential job, which ensures
        its tasks only render in ascending order.
        Returns:
            bool:
        """

    @JobSequentialJob.setter
    def JobSequentialJob(value: bool):
        """See getter.
        Args:
            value (bool)
        """

    @property
    def JobStartedDateTime():
        """The date/time at which the job started rendering.
        Returns:
            DateTime:
        """

    @JobStartedDateTime.setter
    def JobStartedDateTime(value: DateTime):
        """See getter.
        Args:
            value (DateTime)
        """

    @property
    def JobStartJobTimeoutSeconds():
        """The timespan a job's task has to start before a timeout occurs.
        Returns:
            int:
        """

    @JobStartJobTimeoutSeconds.setter
    def JobStartJobTimeoutSeconds(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobStartJobTimeoutSeconds():
        """The job's current state.
        Returns:
            str:
        """

    @property
    def JobSubmitDateTime():
        """The date/time at which the job was submitted.
        Returns:
            DateTime:
        """

    @property
    def JobSubmitMachine():
        """This is the machine that the job was submitted from.
        Returns:
            str:
        """

    @property
    def JobSundayStartTime():
        """Gets or sets Sunday's start time.
        Returns:
            TimeSpan:
        """

    @JobSundayStartTime.setter
    def JobSundayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobSundayStopTime():
        """Gets or sets Sunday's stop time.
        Returns:
            TimeSpan:
        """

    @JobSundayStopTime.setter
    def JobSundayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

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
    def JobSuspendedTasks():
        """The number of tasks in the suspended state.
        Returns:
            int:
        """

    @JobSuspendedTasks.setter
    def JobSuspendedTasks(value: int):
        """See getter.
        Args:
            value (int)
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

    @property
    def JobTaskCount():
        """The number of tasks the job has.
        Returns:
            int:
        """

    @JobTaskCount.setter
    def JobTaskCount(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobTaskExtraInfoName0():
        """One of the Task's ten Extra Info names.
        Returns:
            str:
        """

    @JobTaskExtraInfoName0.setter
    def JobTaskExtraInfoName0(value: str):
        """See getter.
        Args:
            value (str)
        """

    @property
    def JobTaskTimeoutSeconds():
        """The timespan a job's task has to render before
        a timeout occurs.
        Returns:
            int:
        """

    @JobTaskTimeoutSeconds.setter
    def JobTaskTimeoutSeconds(value: int):
        """See getter.
        Args:
            value (int)
        """

    @property
    def JobThursdayStartTime():
        """Gets or sets Thursday's start time.
        Returns:
            TimeSpan:
        """

    @JobThursdayStartTime.setter
    def JobThursdayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobThursdayStopTime():
        """Gets or sets Thursday's stop time.
        Returns:
            TimeSpan:
        """

    @JobThursdayStartTime.setter
    def JobThursdayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobTileJob():
        """If this job is a tile job.
        Returns:
            bool:
        """

    @property
    def JobTileJobFrame():
        """The frame that the tile job is rendering.
        Returns:
            int:
        """

    @property
    def JobTileJobTileCount():
        """The number of tiles in a tile job.
        Returns:
            int:
        """

    @property
    def JobTileJobTilesInX():
        """The number of tiles in X for a tile job.
        This is deprecated, and is only here for backwards
        compatibility.
        Returns:
            int:
        """
        raise DeprecationWarning

    @property
    def JobTileJobTilesInY():
        """The number of tiles in Y for a tile job.
        This is deprecated, and is only here for backwards compatibility.
        Returns:
            int:
        """
        raise DeprecationWarning

    @property
    def JobTuesdayStartTime():
        """Gets or sets Tuesday's start time.
        Returns:
            TimeSpan:
        """

    @JobTuesdayStartTime.setter
    def JobTuesdayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobTuesdayStopTime():
        """Gets or sets Tuesday's stop time.
        Returns:
            TimeSpan:
        """

    @JobTuesdayStopTime.setter
    def JobTuesdayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobUseJobEnvironmentOnly():
        """If only the job's environment variables should
        be used. If disabled, the job's environment will
        be merged with the current environment.
        Returns:
            bool:
        """

    @JobUseJobEnvironmentOnly.setter
    def JobUseJobEnvironmentOnly(value: bool):
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
    def JobWednesdayStartTime():
        """Gets or sets Wednesday's start time.
        Returns:
            TimeSpan:
        """

    @JobWednesdayStartTime.setter
    def JobWednesdayStartTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobWednesdayStopTime():
        """Gets or sets Wednesday's stop time.
        Returns:
            TimeSpan:
        """

    @JobWednesdayStopTime.setter
    def JobWednesdayStopTime(value: TimeSpan):
        """See getter.
        Args:
            value (TimeSpan)
        """

    @property
    def JobWhitelistFlag():
        """If the job's listed Workers are an allow
        list or a deny list.
        Returns:
            bool:
        """

    @property
    def RemTimeThreshold():
        """The remaining time (in seconds) that this Job
        must have left more than in order to be interruptible.
        Returns:
            int:
        """

    @RemTimeThreshold.setter
    def RemTimeThreshold(value: int):
        """See getter.
        Args:
            value (int)
        """
