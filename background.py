from threading import Timer
import time
from shutil import copyfile
import datetime
import os
import subprocess
import sys

#Initial Variables
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) #https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/7675014#7675014
FilePath = os.path.abspath(__file__)
FilePathList = base_path.split("\\")
C_UserPath = FilePathList[0]+"\\"+FilePathList[1]+"\\"+FilePathList[2]
#StoragePath = "C:\Program Files\Windows Video Editor"
StoragePath = C_UserPath+"\documents\Sketchy"
BlockDataPath = StoragePath+"\\block data.txt"
BlockedApplicationsPath = StoragePath+"\\blocked applications.txt"
BlockedWebsitesPath = StoragePath+"\\blocked websites.txt"

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags = startupinfo.dwFlags | subprocess.STARTF_USESHOWWINDOW
try:
    SettingsFile = open(StoragePath+"\Settings","r")
    print("readable")
    SettingsFile.close()
except:
    SettingsFile = open(StoragePath+"\Settings","w+")
    print("not readable")
    SettingsFile.close()
    
IsScriptActive = None
CurrentTime = datetime.datetime.now()
CurrentHour = CurrentTime.hour
CurrentMinute = CurrentTime.minute
TomorrowTimer = None
NextBlockTimer = None

"""COPYPASTE"""

#C:\Windows\System32\drivers\etc
HostFilePath = r"C:\Windows\System32\drivers\etc\hosts" #remember to use the find and replace func later.
CopiedHostsFilePath = StoragePath+"\HostsCopy"


try: #! WE CAN REMOVE THIS
    CopyofHostsData = open(CopiedHostsFilePath,"r")
    print("Theres a copy!")
    CopyofHostsData.close()
except:
    copyfile(HostFilePath,CopiedHostsFilePath)
    print("failed, trying again")

break_time_seconds = 0
BreakTimePath = StoragePath+r"\breaktime.txt"

try: #work
    BreakTimeFile = open(BreakTimePath,"r")
    break_time_string = BreakTimeFile.readline()
    BreakTimeFile.close()
    converted_break_time = datetime.datetime.strptime(break_time_string,r"%Y-%m-%d %H:%M:%S.%f")
    time_difference = converted_break_time-datetime.datetime.now()
    if time_difference > datetime.timedelta(seconds=0):
        break_time_seconds = time_difference.seconds
    else:
        BreakTimeFile = open(BreakTimePath,"w")
        BreakTimeFile.close()
except:
    print("no break")


TasksListFilePath = StoragePath+"\RunningProcesses"

ProtectedAppsList = ['smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe', 'fontdrvhost.exe', 'winlogon.exe', 'WUDFHost.exe', 'dwm.exe', 'spoolsv.exe', 'AdAppMgrSvc.exe', 'sqlwriter.exe', 'LogiRegistryService.exe', 'MsMpEng.exe', 'dasHost.exe', 'NisSrv.exe', 'dllhost.exe', 'sihost.exe', 'taskhostw.exe', 'ctfmon.exe', 'hidfind.exe', 'conhost.exe', 'RuntimeBroker.exe', 'SearchUI.exe', 'SearchIndexer.exe', 'SettingSyncHost.exe', 'SecurityHealthSystray.exe', 'igfxpers.exe', 'ICCProxy.exe', 'ApplicationFrameHost.exe', 'SgrmBroker.exe', 'ShellExperienceHost.exe', 'SystemSettingsBroker.exe', 'SearchProtocolHost.exe', 'WmiPrvSE.exe','dllhost.exe']



CurrentWeekDay = str(datetime.datetime.today().weekday() + 1) 



print("Program intiated at:",str(CurrentHour)+":"+str(CurrentMinute),",",str(CurrentWeekDay)+"th day of the week")

BTD = {}
#################################
ConvertedBTData = None
while True: #gets file data and converts into "BTD" (Block Time Data)
    try:
        BlockDataFile = open(BlockDataPath,"r")
        for line in BlockDataFile:
            LineData = line.split()
            TrueFalseList = []
            
            for character in LineData[1].lower(): 
                if character == "t":
                    TrueFalseList.append(True)
                else:
                    TrueFalseList.append(False)
            BTD[LineData[0]] = [TrueFalseList,[int(LineData[2]),int(LineData[3]),int(LineData[4]),int(LineData[5])]]
        BlockDataFile.close()
        break
    except:
        BlockDataFile = open(BlockDataPath,"w")
        BlockDataFile.close()


BlockedWebsites = []
while True: #gets blocked websites
    try:
        BlockedWebsitesFile = open(BlockedWebsitesPath,"r")
        
        for line in BlockedWebsitesFile:
            BlockedWebsites.append(line[:line.find("\n")])
        BlockedWebsitesFile.close()
        break
    except:
        BlockedWebsitesFile = open(BlockedWebsitesPath,"w")
        BlockedWebsitesFile.close()
print(BlockedWebsites)

BlockedPrograms = []
while True: #gets blocked websites
    try:
        BlockedApplicationsFile = open(BlockedApplicationsPath,"r")
        
        for line in BlockedApplicationsFile:
            BlockedPrograms.append(line[:line.find("\n")])
        BlockedApplicationsFile.close()
        break
    except:
        BlockedApplicationsFile = open(BlockedApplicationsPath,"w")
        BlockedApplicationsFile.close()
print(BlockedPrograms)

###########################################
ConvertedBTData = {"1": {},"2": {},"3": {},"4": {},"5": {},"6": {},"7": {}}
for BlockID in BTD: #Block Data Needs to be converted for "TBLOCK" (Schedule Visualizer) due to poor datamanagement.
    for day in range(7):
        if BTD[BlockID][0][day] == True:
            ConvertedBTData[str(day+1)][BlockID] = BTD[BlockID][1]

#This is a bad play for variable to be
TodaysHours = ConvertedBTData[CurrentWeekDay]

def GetRunningProcesses():
    subprocess.run(f"tasklist > {TasksListFilePath}",startupinfo=startupinfo)
    TryAttempt,TotalTries = 0,10
    RunningAppsList = []
    AppsListFilter = []
    while TryAttempt < TotalTries:
        try:
            TasksFile = open(TasksListFilePath,"r+")
            break
        except:
            print("File not found! Trying again in 1 second.",TotalTries-TryAttempt,"attempts left")
            time.sleep(1)
            TryAttempt+=1
    if TryAttempt >= TotalTries:
        print("There was an error. Please try manually importing the processes.")
    else:
        print("Successful!")
        #print(TasksFile.read())
        #TasksFile.seek(0) #goes to beginning again
        TasksFileLen = len(TasksFile.readlines())
        TasksFile.seek(0)
        StartingPointReached = False
        for DocumentLine in range(TasksFileLen):
            if not StartingPointReached:
                if "=" in TasksFile.readline():
                    StartingPointReached = True
            else:
                CurrentLine = TasksFile.readline()
                if not CurrentLine[:CurrentLine.index("   ")] in RunningAppsList:
                    RunningAppsList.append(CurrentLine[:CurrentLine.index("   ")])
                #print(CurrentLine[5:])
        TasksFile.close()
        TasksFile = open(TasksListFilePath,"w")
        TasksFile.write(str(RunningAppsList))
        TasksFile.close()
        for Application in RunningAppsList:
            #print(Application)
            if not ".exe" in Application:
                AppsListFilter.append(Application)
            elif Application in ProtectedAppsList:
                AppsListFilter.append(Application)

    RunningAppsList.sort()
    for Application in AppsListFilter:
        RunningAppsList.remove(Application)
    print(RunningAppsList)
    return RunningAppsList

def KillBlockedPrograms(List):
    for Program in List:
        subprocess.run(f"taskkill /F /IM {Program}",startupinfo=startupinfo)
        print(Program,"killed")

def SecondsUntilTomorrow():
    CurrentTime = datetime.datetime.now()
    OneDay = datetime.timedelta(days=1)
    TomorrowMorning = (CurrentTime+OneDay).replace(hour=0, minute=0, second=3, microsecond=0)
    SecondsUntilTomorrowVariable = (TomorrowMorning - CurrentTime).seconds
    return SecondsUntilTomorrowVariable


def ResetHostFile():
    copyfile(CopiedHostsFilePath,HostFilePath)


def UpdateHostsFile(List):
    ResetHostFile()
    BlockedWebsitesFile = open(HostFilePath,"r+")
    BlockedWebsitesFile.readlines() #go to end
    BlockedWebsitesFile.write("\n")
    for item in List:
        BlockedWebsitesFile.write("127.0.0.1 "+item+"\n")
    BlockedWebsitesFile.close()


def SecondsUntilCheckup():
    ListofMarkedTimes = {}
    NextTimeVariable = []
    CurrentTime = datetime.datetime.now()
    for TimeInterval in TodaysHours: #Funtion Fills "ListofMarkedTimes" with all the marked times "today"
        if TodaysHours[TimeInterval][0] in ListofMarkedTimes.keys():
            ListofMarkedTimes[TodaysHours[TimeInterval][0]].append(TodaysHours[TimeInterval][1])
        elif CurrentTime.hour <= TodaysHours[TimeInterval][0]:
            ListofMarkedTimes[TodaysHours[TimeInterval][0]] = []
            ListofMarkedTimes[TodaysHours[TimeInterval][0]].append(TodaysHours[TimeInterval][1])
        if TodaysHours[TimeInterval][2] in ListofMarkedTimes.keys():
            ListofMarkedTimes[TodaysHours[TimeInterval][2]].append(TodaysHours[TimeInterval][3])
        elif CurrentTime.hour <= TodaysHours[TimeInterval][2]:
            ListofMarkedTimes[TodaysHours[TimeInterval][2]] = []
            ListofMarkedTimes[TodaysHours[TimeInterval][2]].append(TodaysHours[TimeInterval][3])
    #We need to sort the dictionary, find the value closest to time.now, then update next checkup based on that.
    for DictValue in sorted(ListofMarkedTimes):
        ListofMarkedTimes[DictValue].sort()
        for KeyValue in ListofMarkedTimes[DictValue]:
            #print(DictValue,KeyValue)
            if (DictValue == CurrentTime.hour and KeyValue > CurrentTime.minute) or DictValue > CurrentTime.hour:
                NextTimeVariable.append(DictValue)
                NextTimeVariable.append(KeyValue)
                break
        if not NextTimeVariable == []:
            break
    #LETS GOO buddy
    if NextTimeVariable == []:
        print("No more time blocks left today!")
        return None
    NextActivityCheckup = CurrentTime.replace(hour=NextTimeVariable[0], minute=NextTimeVariable[1], second=3, microsecond=0)
    SecondsUntilCheckupVariable = (NextActivityCheckup-CurrentTime).seconds
    #print("Next checkup time",str(NextTimeVariable[0])+":"+str(NextTimeVariable[1]),"("+str(SecondsUntilCheckupVariable)+" seconds)")
    print(SecondsUntilCheckupVariable,"seconds until next checkup.")
    return SecondsUntilCheckupVariable

def TimeBlockCompareFunction(H1,M1,H2,M2):
    #print(str(H1)+":"+str(M1),str(CurrentHour)+":"+str(CurrentMinute),str(H2)+":"+str(M2))
    if not CurrentHour >= H1 or not CurrentHour <= H2:
        return False
    if CurrentHour == H1 and CurrentMinute < M1:
        return False
    if CurrentHour == H2 and CurrentMinute >= M2:
        return False
    return True


def ShouldScriptRunTest():
    global CurrentHour
    global CurrentMinute
    CurrentHour = datetime.datetime.now().hour
    CurrentMinute = datetime.datetime.now().minute
    for TimeInterval in TodaysHours:
        if TimeBlockCompareFunction(TodaysHours[TimeInterval][0],TodaysHours[TimeInterval][1],TodaysHours[TimeInterval][2],TodaysHours[TimeInterval][3]):
            print(str(TodaysHours[TimeInterval][0])+":"+str(TodaysHours[TimeInterval][1]),"<",str(CurrentHour)+":"+str(CurrentMinute),"<",str(TodaysHours[TimeInterval][2])+":"+str(TodaysHours[TimeInterval][3]))
            return True
    return False

def NextBlockIsHere():
    print("Next block is here!")
    global IsScriptActive
    IsScriptActive = ShouldScriptRunTest()
    print("Script is",IsScriptActive)
    #Start timer for next blockcheckup
    if not SecondsUntilCheckup() == None:
        print("NextTimer started")
        NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
        NextBlockTimer.start()
        print(SecondsUntilCheckup,"seconds until next checkup.")
    Block() #shouldnt do anything is block is false

def TomorrowIsHere():
    print("Tomorrow is here!")
    global CurrentWeekDay
    global TodaysHours
    CurrentWeekDay = str(datetime.datetime.today().weekday() + 1) 
    TodaysHours = ConvertedBTData[CurrentWeekDay]
    TomorrowTimer = Timer(SecondsUntilTomorrow(),TomorrowIsHere)
    TomorrowTimer.start()
    NextBlockTimer.cancel()
    NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
    NextBlockTimer.start()
    Block() #shouldnt do anything is block is false


def Block():
    print("block")
    UpdateHostsFile(BlockedWebsites)
    while IsScriptActive == True or (break_time_seconds > 0 and IsScriptActive == False):
        print("Block")
        KillBlockedPrograms(BlockedPrograms)
        time.sleep(30)
    else:
        ResetHostFile()

def InitiateProgram():
    global IsScriptActive
    IsScriptActive = ShouldScriptRunTest()
    if IsScriptActive:
        print("Currently Active")
    else:
        print("Script Inactive")
    TomorrowTimer = Timer(SecondsUntilTomorrow(),TomorrowIsHere)
    TomorrowTimer.start()
    NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
    NextBlockTimer.start()
    Block() #This is needed!

def reset_break_time():
    global break_time_seconds
    break_time_seconds = 0

ResetHostFile()
if not ShouldScriptRunTest():
    timer_count = 0
    break_time_reset_timer = Timer(break_time_seconds,reset_break_time)
    break_time_reset_timer.start()
else:
    timer_count = break_time_seconds
BreakTimer = Timer(timer_count,InitiateProgram)
BreakTimer.start()
print(break_time_seconds)