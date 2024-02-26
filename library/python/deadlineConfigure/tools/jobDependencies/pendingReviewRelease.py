"""
# -----------------------------------------------------------------------------
#
# Render Release
#
# -----------------------------------------------------------------------------

This renders only every x-th task depending on what is configured in the job
environment. Once the job environment is updated to "release", all tasks
will be rendered. This can be used to preview render a sub-range to check
if the submission is valid and to then release the whole range.
"""

from Deadline.Scripting import RepositoryUtils

from deadlineConfigure.etc.constants import EnvironmentVariables, env_to_bool


def check_for_pending_review_release(job_id, task_ids=None):
    job = RepositoryUtils.GetJob(job_id, True)

    # Handle job to job dependencies
    job_pending_review_release_state = env_to_bool(job.GetJobEnvironmentKeyValue(EnvironmentVariables.JOB_PENDING_REVIEW_RELEASE_STATE) or False)
    job_release_state = bool(1 - job_pending_review_release_state)
    if not task_ids:
        return job_release_state
    
    # Handle task dependencies
    job_frames = job.JobFramesList
    job_tasks = list(range(len(job_frames)))
    if job_release_state:
        return [str(t) for t in job_tasks]

    job_release_task_increment = job.GetJobEnvironmentKeyValue(EnvironmentVariables.JOB_PENDING_REVIEW_RELEASE_INCREMENT) or None
    if job_release_task_increment is None:
        return []
    job_release_task_increment = max(1, int(job_release_task_increment))

    job_release_task_range = [job_tasks[0], job_tasks[-1]]
    job_release_task_range.extend(job_tasks[::job_release_task_increment])
    return [str(t) for t in job_release_task_range]


def __main__(job_id, task_ids=None):
    return check_for_pending_review_release(job_id, task_ids=task_ids)
