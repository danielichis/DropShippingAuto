import os
from pathlib import Path
import sys
class managePaths:
    def __init__(self):
        pass
    def get_current_path(self,up_tree=0):
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)    
        new_parent=Path(application_path)
        for i in range(up_tree):
            new_parent=new_parent.parent
        return new_parent
    def get_root_path(self):
        root_path = os.getcwd()
        return root_path
    
pathsManager=managePaths()