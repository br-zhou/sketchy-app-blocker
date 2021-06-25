#INCOMPLETE
import time
import ctypes, sys
import sys
import shutil
import os

"""Requests Admin Permission"""

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, '"'+'"'.join(sys.argv)+'"', None, 1)
    sys.exit()

"""Variables"""
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) 
FilePathList = base_path.split("\\")
user_path = FilePathList[0]+"\\"+FilePathList[1]+"\\"+FilePathList[2]
HostFilePath = r"C:\Windows\System32\drivers\etc\hosts"
storage_path = user_path+"\documents\Sketchy"
folder_path = base_path[:base_path.index(FilePathList[-1])]
ExeFilePath = os.path.abspath(__file__)
FolderPath = ExeFilePath[:ExeFilePath.index(ExeFilePath.split("\\")[-1])-1]
setup_storage_path = FolderPath+"\Sketchy"
UserName = ExeFilePath.split("\\")[2]
print(FolderPath)
HostFileDuplicate = setup_storage_path+"\hosts"
start_menu_file_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
sab_main_path = storage_path+"\Sketchy App Blocker.exe"

new_hosts_file = open(HostFileDuplicate,"w+")
new_hosts_file.close()
try: os.remove(HostFilePath)
except: pass
shutil.move(HostFileDuplicate,HostFilePath) #Replaces Hosts File
shutil.copytree(setup_storage_path,storage_path)