# Deadline Repository

This repository is still work in progress, please check back at a later time.

## Setup
This repository should be placed in your \<DeadlineRepositoryInstallRoot\>/custom folder (or symlinked to be that folder).

## Features

### Deadline API (library/python/deadlineAPI)
A thin API layer wrapper around certain parts of the [Deadline Scripting Reference](https://docs.thinkboxsoftware.com/products/deadline/10.3/2_Scripting%20Reference/index.html) that:
- is 100% compatible, as it implements the same interface
- allows us to communicate with both the [Deadline Scripting Reference](https://docs.thinkboxsoftware.com/products/deadline/10.3/2_Scripting%20Reference/index.html) and the [Deadline Standalone Python Reference (Python Webservice API interface)](https://docs.thinkboxsoftware.com/products/deadline/10.3/3_Python%20Reference/index.html) simultaneously by being able to serialize our classes to either backend.
- defines our default job configuration as well as allows us to diff job configuration change sets.
- can be used to submit and modify existing jobs

Currently we wrap the following:
- Deadline.Jobs.Job
