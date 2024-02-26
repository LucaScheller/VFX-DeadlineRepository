import os

from dataclasses import dataclass

_PACKAGE_ROOT = os.path.dirname(os.path.dirname(__file__))


def env_to_bool(env):
    return env in [True, 1, "True", "true", "1", "Yes", "yes"]

def bool_to_env(value):
    return "True" if value else "False"

class EnvironmentVariables:
    JOB_PENDING_REVIEW_RELEASE_STATE = "DL_JOB_PENDING_REVIEW_RELEASE_STATE"
    JOB_PENDING_REVIEW_RELEASE_INCREMENT = "DL_JOB_PENDING_REVIEW_RELEASE_INCREMENT"


@dataclass
class JobExtraInfoEntry:
    INDEX: int
    API_NAME: str
    COMMANDLINE_NAME: str
    LABEL: str
    DEFAULT_VALUE: str

class JobExtraInfo:
    pending_review_release = JobExtraInfoEntry(0, "JobExtraInfo0", "ExtraInfo0", "Pending Review Release", "False")


class JobDependencyScripts:
    pending_review_release = os.path.join(
        _PACKAGE_ROOT, "tools", "jobDependencies", "pendingReviewRelease.py"
    )
