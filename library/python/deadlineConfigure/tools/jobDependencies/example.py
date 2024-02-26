def __main__(jobId, taskIds=None):
    if not taskIds:
        # Frame Dependencies are disabled
        releaseJob = False
        #figure out if job should be released
        return releaseJob
    else:
        # Frame Dependencies are enabled
        tasksToRelease = list(range(0,10, 5))
        #figure out which tasks should be released, and append their IDs to the array
        return [str(t) for t in tasksToRelease]
    

"""
from Deadline.Scripting import *

def __main__( jobID, taskIDs=None ):
    if taskIDs is None:
        # Frame Dependencies are therefore disabled
        job = RepositoryUtils.GetJob( jobID, False )
        
        for dependency in job.JobDependencyIDs:
            output_files = RepositoryUtils.GetJob( dependency, False ).OutputFilenames
            for file in output_files:
                if FileUtils.GetFileSize( file ) < 10: # bytes
                    return False
    
    return True
"""

"""
# Check job environment
try:
    connection = Connect.DeadlineCon('localhost', 8081)
    job_data = connection.Jobs.GetJob(job_id)
except Exception:
    # Block if database connection is not valid.
    return False

job_data["Props"]["Env"]
FrameUtils.Parse(job_data["Props"]["Frames"])
"""