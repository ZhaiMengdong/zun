import os
from zun.common import exception

class DirDriver(object):

    @staticmethod
    def is_dir_available(directory):
        if os.path.exists(directory):
            pass
        else:
            raise exception.DirNotExisting(directory=directory)