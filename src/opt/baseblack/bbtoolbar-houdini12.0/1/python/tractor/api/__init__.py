from tasktree import Job, Task, RemoteCmd, Cmd
from serialize import Serializer

def getSpoolDirectory(*args, **kwargs):
    """Multiple arguments may be passed.

       1) A Job object is passed. The user is taken from the job task tree
       2) kwarg 'user' is set. This is used for the user.
       3) kwarg 'timestamp' is set. This is used for the timestamp and directory name.
          it should be an epoch based integer.
    """

    import time, getpass
    import tractor
    from tractor.api import Job

    if 'refresh' not in kwargs:
        # An early out, allowing us to reuse an existing path.
        # This may/not be useful for spooling multiple jobs
        # in the same session.
        if hasattr(tractor, '_currentSpoolDirectory'):
            return tractor._currentSpoolDirectory

    elif kwargs['refresh'] == False:
        # Refresh has been set, but to False. We are to reuse an
        # existing path (if it exists).
        if hasattr(tractor, '_currentSpoolDirectory'):
            return tractor._currentSpoolDirectory

    # Next we ensure that any arguments we're looking out for have set
    # variables within the local scope to build into the spool path.
    for arg in args:
        if isinstance( arg, Job ):
            # hey, found a job in the args list
            # a user is by default added to the job task tree.
            user = arg.user

    if 'user' in kwargs:
        user = kwargs['user']

    if 'timestamp' in kwargs:
        timestamp = kwargs['timestamp']

    # Sanity Checking. Should a variable not have been set then we'll
    # set it. Its the kinda thing that I'm always torn between the savings
    # in not doing user/time lookups for each call vs the performance of
    # putting them inside conditionals.
    if 'timestamp' not in locals():
        timestamp = int(time.time())
    if 'user' not in locals():
        user = getpass.getuser()

    datestr = time.strftime( "%Y/%m/%d/%H%M%S", time.localtime(timestamp) )
    tractor._currentSpoolDirectory = "{0}/spool/{1}/{2}".format( tractor.SPOOL_ROOT, user, datestr )
    return tractor._currentSpoolDirectory

__all__ =   [
        'Job',
        'Task',
        'RemoteCmd',
        'Cmd',
        'Serializer',
        'getSpoolDirectory',
        ]
