import os
from Deadline.Scripting import MonitorUtils, RepositoryUtils
from deadlineConfigure.etc.constants import (EnvironmentVariables,
                                             JobExtraInfo,
                                             JobDependencyScripts,
                                             bool_to_env,
                                             env_to_bool)


def __main__(*args):
    # Preflight checks
    selected_jobs = MonitorUtils.GetSelectedJobs()
    if not selected_jobs:
        return
    # Filter jobs of interest
    valid_jobs = []
    for job in selected_jobs:
        job_script_dependencies_file_paths = [os.path.realpath(s.ToString()) for s in job.JobScriptDependencies]
        if JobDependencyScripts.pending_review_release in job_script_dependencies_file_paths:
            valid_jobs.append(job)
    if not valid_jobs:
        return

    # Get collective state
    states = []
    for job in valid_jobs:
        pending_review_state = env_to_bool(job.GetJobEnvironmentKeyValue(EnvironmentVariables.JOB_PENDING_REVIEW_RELEASE_STATE))
        states.append(pending_review_state)

    # Set collective state
    pending_review_state = bool_to_env(1-all(states))
    for job in valid_jobs:
        # Update env var
        job.SetJobEnvironmentKeyValue(EnvironmentVariables.JOB_PENDING_REVIEW_RELEASE_STATE,
                                        pending_review_state)
        # Update label
        setattr(job, JobExtraInfo.pending_review_release.API_NAME, pending_review_state)
        RepositoryUtils.SaveJob(job)
