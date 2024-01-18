from pathlib import Path #Recommended way to approach anything related to FS

import os
from datetime import datetime
import shutil
from time import time
import Logging


src = Path("/Users/ShubhamKhandelwal/Box Sync/Sabre BLR Dev team/NewBees/OPA_Test_Files/UpdateFilesTesting/Box")
dest = Path('/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/UpdateFileTesting')

# def list_all_files():
#     l = []
#     for f in source_dir.glob('**/*'):
#         if f.is_file():
#             l.append(f)
#     return l
  

# def get_relative_path(f: Path, from_dir: Path = source_dir):
#     return os.path.relpath(f, from_dir)


def get_modified_time(path):
    timestamp = os.path.getmtime(path)
    datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y")
    # timestamp = datetime.fromtimestamp(timestamp)
    return timestamp

def checkModifiedDate(filePath, destPath, updateFlag):
    BoxModTime = get_modified_time(filePath)
    appModTime = get_modified_time(destPath) 
    # if(BoxModTime != appModTime):
    #     updateFlag = True
    if((BoxModTime - appModTime)>0):
        updateFlag = True
        
    return updateFlag



def updateFiles():
    # files = list_all_files()

    # updateFlag = False
    # for file in files:                  #file = C:/Users/SG0314857/Documents/BoxTest/AppTest/test.txt
    #     rel = get_relative_path(file)    #cleanPath - path from parent directory   rel = test.txt
    #     destFull = destination_dir.joinpath(rel)          #destFull = C:/Users/SG0314857/Documents/ApplicationTest/AppTest/test.txt

    #     if(destFull.exists()):
    #         updateFlag = checkModifiedDate(file, destFull, updateFlag)
    #         if(updateFlag == True):
    #             Logging.logger("Updating Box file = " + str(file) + " to Application file = " + str(destFull))
    #             print("Updating Box file = " + str(file) + " to Application file = " + str(destFull))
    #             shutil.copyfile(file, destFull)
    #         else:
    #             continue
    #     else:
    #         print(str(destFull) + "doesn't exist in destination folder")
    #         print("Downloading file in our system")
    #         open(file, "a")
    #         Logging.logger("Downloading Box file = " + str(file) + " to Application file = " + str(destFull))
    #         shutil.copyfile(file, destFull)

    updateFlag = False

    for leaf in src.glob('**/*'):
        if not leaf.is_file():
            continue
        relative_path = os.path.relpath(leaf, src)
        dest_file = dest.joinpath(relative_path)

        # dest_file.parent.mkdir(exist_ok=True)
        # dest_file.touch(exist_ok=True)
        # shutil.copy(leaf, dest_file)

        if(dest_file.exists()):
            updateFlag = checkModifiedDate(leaf, dest_file, updateFlag)
            if(updateFlag == True):
                Logging.logger("Updating Box file = " + str(leaf) + " to Application file = " + str(dest_file))
                # dest_file.parent.mkdir(exist_ok=True)
                # dest_file.touch(exist_ok=True)
                shutil.copy(leaf, dest_file)
        else:
            dest_file.parent.mkdir(exist_ok=True)
            dest_file.touch(exist_ok=True)
            Logging.logger("Downloading Box file = " + str(leaf) + " to Application file = " + str(dest_file))
            shutil.copy(leaf, dest_file)


        
        