import os
from os import path


def rm(filename):
    if path.isfile(filename):
        os.remove(filename)


class RemovalService(object):
    """
    A service for removing objects from the filesystem.
    """

    def rm(self, filename):
        """
        Tries to remove file. Returns `True` in case file was removed, otherwise, `False.`
        """
        if not path.isfile(filename):
            return False
        os.remove(filename)
        return True


class UploadService(object):
    
    def __init__(self, removal_service):
        self.removal_service = removal_service
        
    def upload_complete(self, filename):
        self.removal_service.rm(filename)
