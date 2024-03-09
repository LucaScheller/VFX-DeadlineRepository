from __future__ import absolute_import
import os
import sys
import subprocess
import logging

from Deadline.Scripting import ClientUtils

def __main__():
    """Manual call: 
    dl_client_bin_dir_path = ClientUtils.GetBinDirectory()
    command = [
        os.path.join(dl_client_bin_dir_path, "deadlinecommand"),
        "DoPendingJobScan"
    ]
    subprocess.check_call(command)
    """
    ClientUtils.LogText("Running Command | deadlinecommand DoPendingJobScan")
    ClientUtils.ExecuteCommand("DoPendingJobScan")