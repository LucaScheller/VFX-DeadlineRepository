import sys

import redis
from Deadline.Events import DeadlineEventListener
from deadlineConfigure.etc.constants import (
    EnvironmentVariables,
    RedisServerConfiguration,
)


def GetDeadlineEventListener():
    return RedisEventListener()


def CleanupDeadlineEventListener(deadlinePlugin):
    deadlinePlugin.Cleanup()


class RedisEventListener(DeadlineEventListener):
    def __init__(self):
        if sys.version_info.major == 3:
            super().__init__()
        # Set up the event callbacks here
        self.OnJobDeletedCallback += self.OnJobDeleted
        self.OnJobPurgedCallback += self.OnJobPurged

    def Cleanup(self):
        del self.OnJobDeletedCallback
        del self.OnJobPurgedCallback

    def OnJobDeleted(self, job):
        mode = self.GetConfigEntry("EventKeyDelete")
        if mode == "JobDelete":
            self.DeleteKeysFromEnv(job)

    def OnJobPurged(self, job):
        mode = self.GetConfigEntry("EventKeyDelete")
        if mode == "JobPurge":
            self.DeleteKeysFromEnv(job)

    def DeleteKeysFromEnv(self, job):
        """Delete keys stored in the job env.
        Args:
            job (Job): The deadline job.
        """
        redis_keys = job.GetJobEnvironmentKeyValue(EnvironmentVariables.JOB_REDIS_KEYS)
        if not redis_keys:
            return
        redis_keys = redis_keys.split(",")

        self.LogInfo(
            "Redis Event Plugin | Deleting Keys | {}".format(", ".join(redis_keys))
        )
        # Delete keys
        redis_server_connection = redis.Redis(
            host=RedisServerConfiguration.HOST,
            port=RedisServerConfiguration.PORT,
            decode_responses=True,
        )
        for redis_key in redis_keys:
            redis_server_connection.delete(redis_key)
