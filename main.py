#Okay, I started this project when I first started learning python (overestimated the completion time by HUGE amount of time). So, this being written over the span of 6 months (mostly due me forgetting the existance of this project), the level of the code and variable naming schemes are inconsistant. That's why you might see chunks of inefficient spaghetti code in some places.

from threading import Timer
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import os
import sys
import datetime
import webbrowser
import time
from shutil import copyfile
import subprocess

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) 
FilePath = os.path.abspath(__file__)
#print(FilePath)
FilePathList = base_path.split("\\")
C_UserPath = FilePathList[0]+"\\"+FilePathList[1]+"\\"+FilePathList[2]
FolderPath = FilePath[:FilePath.find(f"\\{FilePathList[-1]}")]
StoragePath = C_UserPath+"\documents\Sketchy"
ImagesPath = StoragePath+"\images"
TasksListFilePath = StoragePath+"\RunningProcesses.txt"
BlockDataPath = StoragePath+"\\block data.txt"
BlockedApplicationsPath = StoragePath+"\\blocked applications.txt"
BlockedWebsitesPath = StoragePath+"\\blocked websites.txt"
BlockBGHex = "#393d50" 
ColumnBGHex = "#fefefe"
Mon_Coords = [100,120]
Box_Dimensions = [60,300]
Column_spacing = 20
Text_spacing = 10
Ruler_spacing = [50,12]
CTwidth = 50
CTConstant = 10
DoWAcronymList = ["Mon","Tues","Wed","Thur","Fri","Sat","Sun"]
Unsaved = None
BTD = {}
ConvertedBTData = None
SaveModeDict = {"e":"SAVE","c":"CREATE"}
BreakTimePath = StoragePath+r"\breaktime.txt"
IsScriptActive = None
CurrentTime = datetime.datetime.now()
CurrentHour = CurrentTime.hour
CurrentMinute = CurrentTime.minute
TomorrowTimer = None
NextBlockTimer = None
sub_timer = None
CurrentWeekDay = str(datetime.datetime.today().weekday() + 1) 
TodaysHours = None
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags = startupinfo.dwFlags | subprocess.STARTF_USESHOWWINDOW



settings_file_path = StoragePath+"\settings.csv"
settings_file = open(settings_file_path,"r")
settings_file_data = settings_file.readlines()
#print(settings_file_data)
settings = {}
for line in settings_file_data:
    line_data = line.replace("\n","").split(",")
    settings[line_data[0]] = line_data[1]
settings_file.close()
#print(settings)

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
        try:
            BlockDataFile = open(BlockDataPath,"w")
            BlockDataFile.close()
        except:
            break





BlockedWebsitesList = []
while True: #gets blocked websites
    try:
        BlockedWebsitesFile = open(BlockedWebsitesPath,"r")
        
        for line in BlockedWebsitesFile:
            BlockedWebsitesList.append(line[:line.find("\n")])
        BlockedWebsitesFile.close()
        break
    except:
        try:
            BlockedWebsitesFile = open(BlockedWebsitesPath,"w")
            BlockedWebsitesFile.close()
        except:
            break
#print(BlockedWebsitesList)

BlockedApplicationsList = []
while True: #gets blocked websites
    try:
        BlockedApplicationsFile = open(BlockedApplicationsPath,"r")
        
        for line in BlockedApplicationsFile:
            BlockedApplicationsList.append(line[:line.find("\n")])
        BlockedApplicationsFile.close()
        break
    except:
        try:
            BlockedApplicationsFile = open(BlockedApplicationsPath,"w")
            BlockedApplicationsFile.close()
        except:
            break
#print(BlockedApplicationsList)

def UpdateCBTD():
    global TodaysHours
    global ConvertedBTData
    ConvertedBTData = {"1": {},"2": {},"3": {},"4": {},"5": {},"6": {},"7": {}}
    for BlockID in BTD: #Block Data Needs to be converted for "TBLOCK" (Schedule Visualizer) due to poor datamanagement.
        for day in range(7):
            if BTD[BlockID][0][day] == True:
                ConvertedBTData[str(day+1)][BlockID] = BTD[BlockID][1]
    TodaysHours = ConvertedBTData[CurrentWeekDay]
UpdateCBTD()

ProtectedAppsList = ['smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe', 'fontdrvhost.exe', 'winlogon.exe', 'WUDFHost.exe', 'dwm.exe', 'spoolsv.exe', 'AdAppMgrSvc.exe', 'sqlwriter.exe', 'LogiRegistryService.exe', 'MsMpEng.exe', 'dasHost.exe', 'NisSrv.exe', 'dllhost.exe', 'sihost.exe', 'taskhostw.exe', 'ctfmon.exe', 'hidfind.exe', 'conhost.exe', 'RuntimeBroker.exe', 'SearchUI.exe', 'SearchIndexer.exe', 'SettingSyncHost.exe', 'SecurityHealthSystray.exe', 'igfxpers.exe', 'ICCProxy.exe', 'ApplicationFrameHost.exe', 'SgrmBroker.exe', 'ShellExperienceHost.exe', 'SystemSettingsBroker.exe', 'SearchProtocolHost.exe', 'WmiPrvSE.exe','dllhost.exe',"SecurityHealthService.exe","SystemSettings.exe","tasklist.exe","hkcmd.exe","cmd.exe","explorer.exe","python.exe","py.exe","UserOOBEBroker.exe","SearchFilterHost.exe","SearchApp.exe",'Cortana.exe',]

################################################################
root = Tk()
root.title("Sketchy App Blocker")
try:
    root.iconbitmap(ImagesPath+"\icon.ico")
except:
    pass
width=1000
height=500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
def closewindow():
    reset_background_file()
    Update_Settings_File()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", closewindow)

"""Setup"""


"""MAIN MENU"""

def take_break_cmd(Time):
    #print("def take break command")
    time_now = datetime.datetime.now()
    BreakTimeFile = open(BreakTimePath,"w")
    try:
        BreakTimeFile.write(str(time_now+datetime.timedelta(minutes=Time)))
    except:
        BreakTimeFile.write("")
    BreakTimeFile.close()
    reset_background_file()
    CancelTimerLoop()
    UpdateMenuLoop()

def Update_Settings_File():
    complete_settings_string = ""
    for key in settings:
        complete_settings_string += f"{key},{settings[key]}\n"
    #print(complete_settings_string)
    settings_file = open(settings_file_path,"w")
    settings_file.write(complete_settings_string)
    settings_file.close()

def reset_background_file():
    #print("---CLEARING BACKGROUND FILE---")
    #subprocess.run(f'start /min cmd.exe /c python "{FolderPath}\\Background.pyw"',startupinfo=startupinfo)
    subprocess.run(f"taskkill /F /IM sketchy_background.exe",startupinfo=startupinfo)
    tempfunc = Timer(0,run_background_file)
    tempfunc.start()

def run_background_file():
    #print("---LAUCNHING BACKGROUND FILE---")
    subprocess.run(f'"{StoragePath}\sketchy_background.exe"',startupinfo=startupinfo)
###Settings Button
SettingsButton=tk.Button(root)
try:
    SettingsImage = PhotoImage(file= ImagesPath+"\settings.png")
    SettingsButton["image"] = SettingsImage
    SettingsButton["bg"] = "#efefef"
except:
    SettingsButton["text"] = "⚙️"
    SettingsButton["font"] = ("",30)
    SettingsButton["bg"] = "#ffffff"
SettingsButton["borderwidth"] = "0px"
SettingsButton["command"] = lambda: SwitchScene("Settings","Menu")

#Images
try:
    GunSlinger = PhotoImage(file= ImagesPath+"\gunslinger.png")
    GSImageFrame = Label(image=GunSlinger)
except:
    GSImageFrame = Label(image=None)

try:
    Octous = PhotoImage(file= ImagesPath+"\octopus.png")
    OctImageFrame = Label(image=Octous)
except:
    OctImageFrame = Label(image=None)

def SE_Save_Changes_Function():
    global Unsaved
    #print("Saved!")
    #update block data file
    BlockDataFile = open(BlockDataPath,"w")
    for Data in BTD:
        TrueFalseString = ""
        for TF in BTD[Data][0]:
            if TF == True:
                TrueFalseString += "T"
            else:
                TrueFalseString += "F"
        BlockDataFile.write(f"{Data} {TrueFalseString} {BTD[Data][1][0]} {BTD[Data][1][1]} {BTD[Data][1][2]} {BTD[Data][1][3]} \n")
    BlockDataFile.close()
    #print(BTD)
    #print(ConvertedBTData)
    Unsaved = False
    SaveChangesCheck()
    BreakTimeFile = open(BreakTimePath,"w")
    BreakTimeFile.close()
    reset_background_file()

#Main Message
menu_title_text=tk.Label(root)
menu_title_text["font"] = ("", 35)
menu_title_text["fg"] = "#333333"
menu_title_text["justify"] = "center"

others_title_text=tk.Label(root)
others_title_text["font"] = ("", 25)
others_title_text["fg"] = "#333333"
others_title_text["justify"] = "center"
others_title_text["text"] = "more features soon?"
#Time Till Next Function
menu_sub_text=tk.Label(root)
menu_sub_text["font"] = ("", 10)
menu_sub_text["fg"] = "#333333"
menu_sub_text["justify"] = "center"


#Take Break
break_work_btn=tk.Button(root)
break_work_btn["activebackground"] = "#1f2949"
break_work_btn["activeforeground"] = "#ffffff"
break_work_btn["bg"] = "#393d49"
break_work_btn["borderwidth"] = "0px"
break_work_btn["font"] = ("", 13)
break_work_btn["fg"] = "#ffffff"

#Applications Button
GButton_492=tk.Button(root)
GButton_492["activebackground"] = "#1f2949"
GButton_492["activeforeground"] = "#ffffff"
GButton_492["bg"] = "#393d49"
GButton_492["borderwidth"] = "0px"
GButton_492["font"] = ("", 15)
GButton_492["fg"] = "#ffffff"
GButton_492["justify"] = "center"
GButton_492["text"] = "Applications"
GButton_492["command"] = lambda: SettingsSwitchScene("Applications")

#Websites Button
GButton_827=tk.Button(root)
GButton_827["activebackground"] = "#1f2949"
GButton_827["activeforeground"] = "#ffffff"
GButton_827["bg"] = "#393d49"
GButton_827["borderwidth"] = "0px"
GButton_827["font"] = ("", 15)
GButton_827["fg"] = "#ffffff"
GButton_827["justify"] = "center"
GButton_827["text"] = "Websites"
GButton_827["command"] = lambda: SettingsSwitchScene("Websites")

#Schedule Button
GButton_53=tk.Button(root)
GButton_53["activebackground"] = "#1f2949"
GButton_53["activeforeground"] = "#ffffff"
GButton_53["bg"] = "#393d49"
GButton_53["borderwidth"] = "0px"
GButton_53["font"] = ("", 15)
GButton_53["fg"] = "#ffffff"
GButton_53["justify"] = "center"
GButton_53["text"] = "Schedule"
GButton_53["command"] = lambda: SettingsSwitchScene("Schedule")

#Other Button
GButton_866=tk.Button(root)
GButton_866["activebackground"] = "#1f2949"
GButton_866["activeforeground"] = "#ffffff"
GButton_866["bg"] = "#393d49"
GButton_866["borderwidth"] = "0px"
GButton_866["font"] = ("", 15)
GButton_866["fg"] = "#ffffff"
GButton_866["justify"] = "center"
GButton_866["text"] = "Other"
GButton_866["command"] = lambda: SettingsSwitchScene("Other")

#Save Changes Button
Save_Button=tk.Button(root)
Save_Button["activebackground"] = "#90ee90"
Save_Button["activeforeground"] = "#ffffff"
Save_Button["anchor"] = "center"
Save_Button["bg"] = "#50c878"
Save_Button["borderwidth"] = "0px"
Save_Button["font"] = ("", 12)
Save_Button["fg"] = "#ffffff"
Save_Button["justify"] = "center"
Save_Button["text"] = "SAVE"
Save_Button["relief"] = "ridge"
Save_Button["command"] = SE_Save_Changes_Function

#Cancel Button
Cancel_Button=tk.Button(root)
Cancel_Button["activebackground"] = "#ff0303"
Cancel_Button["activeforeground"] = "#ffffff"
Cancel_Button["bg"] = "#fc5151"
Cancel_Button["borderwidth"] = "0px"
Cancel_Button["disabledforeground"] = "#ffffff"
Cancel_Button["font"] = ("", 12)
Cancel_Button["fg"] = "#ffffff"
Cancel_Button["text"] = "Cancel"
Cancel_Button["command"] = lambda: SwitchScene("Menu","Settings")

Back_Button=tk.Button(root)
Back_Button["activebackground"] = "#ffffff"
Back_Button["activeforeground"] = "#333333"
Back_Button["bg"] = "#393d49"
Back_Button["borderwidth"] = "0px"
Back_Button["font"] = ("", 12)
Back_Button["fg"] = "#ffffff"
Back_Button["text"] = "BACK"
Back_Button["command"] = lambda: SwitchScene("Menu","Settings")

"""Settings Subcategories"""

"""Applications"""

ba_frame = LabelFrame(root,text = "Ba_Frame",font = ("",12))
ba_frame["borderwidth"] = "0px"


bn_scrollbar = Scrollbar(ba_frame)
bn_scrollbar.pack(side="right",fill="y")

AppTextBox = Listbox(ba_frame,yscrollcommand = bn_scrollbar.set,width=100,height=100,font=("",15),relief=FLAT)
AppTextBox.bind("<Double 1>", lambda e: ATB_DoubleClick())
AppTextBox.bind("<Button-1>", lambda e: EditButtonToggleCheck())
AppTextBox.pack()
bn_scrollbar.config(command=AppTextBox.yview)

def ATB_DoubleClick():
    if ActiveSettingsScene == "Websites":
        WE_Command("e",AppTextBox.index(ANCHOR))
    if ActiveSettingsScene == "Applications":
        AE_Command("e",AppTextBox.index(ANCHOR))


def UpdateBlockedApplicationsData():
    #print(BlockedApplicationsList)
    BlockedApplicationsFile = open(BlockedApplicationsPath,"w")
    for Application in BlockedApplicationsList:
        BlockedApplicationsFile.write(Application+"\n")
    BlockedApplicationsFile.close()

def UpdateBlockedWebsitesData():
    #print(BlockedApplicationsList)
    BlockedWebsitesFile = open(BlockedWebsitesPath,"w")
    for Application in BlockedWebsitesList:
        BlockedWebsitesFile.write(Application+"\n")
    BlockedWebsitesFile.close()
    
   
def break_Command():
    #print("def break command, button press")
    def break_save_changes():
        Input = break_input.get()
        Input_Int = int(Input)
        if not settings["break input history"] == Input:
            settings["break input history"] = Input
            Update_Settings_File()
        take_break_cmd(Input_Int)
        break_window.destroy()

    global break_window
    try:
        if break_window.state() == "normal":
            break_window.destroy()
    except:
        pass

    break_window = Toplevel(root)
    break_window.focus()
    break_window.title("")
    break_width=500
    break_height=125
    break_alignstr = f'{break_width}x{break_height}+{(screenwidth - break_width) // 2}+{(screenheight - break_height) // 2}'
    break_window.geometry(break_alignstr)
    break_window.resizable(width=False, height=False)
    break_window.attributes("-topmost", True)
    break_savebtn=tk.Button(break_window)
    break_savebtn["activebackground"] = "#90ee90"
    break_savebtn["activeforeground"] = "#ffffff"
    break_savebtn["bg"] = "#50c878"
    break_savebtn["borderwidth"] = "0px"
    break_savebtn["font"] = ("",13)
    break_savebtn["fg"] = "#ffffff"
    break_savebtn["text"] = "Save"
    break_savebtn["command"] = break_save_changes
    break_savebtn.place(x=400,y=70,width=90,height=40)
    
    break_cancelbtn=tk.Button(break_window)
    break_cancelbtn["activebackground"] = "#ff0303"
    break_cancelbtn["activeforeground"] = "#ffffff"
    break_cancelbtn["bg"] = "#fc5151"
    break_cancelbtn["borderwidth"] = "0px"
    break_cancelbtn["font"] = ("",13)
    break_cancelbtn["fg"] = "#ffffff"
    break_cancelbtn["text"] = "CANCEL"
    break_cancelbtn["command"] = lambda: break_window.destroy()
    break_cancelbtn.place(x=300,y=70,width=90,height=40)
    
    break_input=tk.Entry(break_window)
    break_input["borderwidth"] = "1px"
    break_input["font"] = ("",15)
    break_input["fg"] = "#333333"
    break_input["borderwidth"] = "0px"
    break_input.insert(0,settings["break input history"])
    break_input.place(x=10,y=10,width=480,height=30)
    
    GenericText=tk.Label(break_window)
    GenericText["font"] = ("", 13)
    GenericText["fg"] = "#333333"
    GenericText["text"] = "how many minutes?"
    GenericText.place(x=5,y=40,width=160,height=30)    
    
    Warning_Text=tk.Label(break_window)
    Warning_Text["font"] = ("", 13)
    Warning_Text["fg"] = "#ff4f4f"
    Warning_Text["text"] = ""
    Warning_Text.place(x=10,y=90,width=170,height=30)    

def WE_Command(Mode,Index):
    #print(Index)
    try:
        SelectedItem = BlockedWebsitesList[AppTextBox.index(ANCHOR)]
    except:
        if Mode == "c":
            pass
        else:
            return
    def GetSelectedProcess(Event):
        we_input.delete(0,END)
        InsertTextTimer = Timer(.1,lambda: we_input.insert(0,awe_listbox.get(ANCHOR)))
        InsertTextTimer.start()
    
    def we_save_changes():
        #print("save")
        if Mode == "e":
            BlockedWebsitesList[Index] = we_input.get()
        else:
            BlockedWebsitesList.append(we_input.get())
        Reset_ATB()
        UpdateBlockedWebsitesData()
        reset_background_file()
        we_window.destroy()
    global we_window
    global awe_listbox
    try:
        if we_window.state() == "normal":
            we_window.destroy()
    except:
        pass

    we_window = Toplevel(root)
    we_window.focus()
    we_window.title("Blocked Websites")
    we_width=500
    we_height=125
    we_alignstr = f'{we_width}x{we_height}+{(screenwidth - we_width) // 2}+{(screenheight - we_height) // 2}'
    we_window.geometry(we_alignstr)
    we_window.resizable(width=False, height=False)
    we_window.attributes("-topmost", True)
    we_savebtn=tk.Button(we_window)
    we_savebtn["activebackground"] = "#90ee90"
    we_savebtn["activeforeground"] = "#ffffff"
    we_savebtn["bg"] = "#50c878"
    we_savebtn["borderwidth"] = "0px"
    we_savebtn["font"] = ("",13)
    we_savebtn["fg"] = "#ffffff"
    we_savebtn["text"] = SaveModeDict[Mode]
    we_savebtn["command"] = we_save_changes
    we_savebtn.place(x=400,y=70,width=90,height=40)
    
    we_cancelbtn=tk.Button(we_window)
    we_cancelbtn["activebackground"] = "#ff0303"
    we_cancelbtn["activeforeground"] = "#ffffff"
    we_cancelbtn["bg"] = "#fc5151"
    we_cancelbtn["borderwidth"] = "0px"
    we_cancelbtn["font"] = ("",13)
    we_cancelbtn["fg"] = "#ffffff"
    we_cancelbtn["text"] = "CANCEL"
    we_cancelbtn["command"] = lambda: we_window.destroy()
    we_cancelbtn.place(x=300,y=70,width=90,height=40)
    
    we_input=tk.Entry(we_window)
    we_input["borderwidth"] = "1px"
    we_input["font"] = ("",15)
    we_input["fg"] = "#333333"
    we_input["borderwidth"] = "0px"
    if Mode == "e":
        we_input.insert(0,BlockedWebsitesList[Index])
    we_input.place(x=10,y=10,width=480,height=30)
    
    GenericText=tk.Label(we_window)
    GenericText["font"] = ("", 13)
    GenericText["fg"] = "#333333"
    GenericText["text"] = "Type in a nasty website..."
    GenericText.place(x=5,y=40,width=200,height=30)
    
    bw_watchtutorial=tk.Button(we_window)
    bw_watchtutorial["bg"] = "#ffffff"
    bw_watchtutorial["borderwidth"] = "0px"
    bw_watchtutorial["font"] = ("", 10)
    bw_watchtutorial["fg"] = "#000000"
    bw_watchtutorial["text"] = "not working? click here"
    bw_watchtutorial["command"] = lambda:bwwe_func()
    bw_watchtutorial.place(x=10,y=80,width=150,height=30)
    def bwwe_func():
        bw_watchtutorial_command()
        we_window.destroy()
def AE_Command(Mode,Index):
    #print(Index)
    try:
        SelectedItem = BlockedApplicationsList[AppTextBox.index(ANCHOR)]
    except:
        if Mode == "c":
            pass
        else:
            return
    def GetSelectedProcess(Event):
        awe_input.delete(0,END)
        InsertTextTimer = Timer(.1,lambda: awe_input.insert(0,awe_listbox.get(ANCHOR)))
        InsertTextTimer.start()
    
    def awe_save_changes():
        #print("save")
        if Mode == "e":
            BlockedApplicationsList[Index] = awe_input.get()
        else:
            BlockedApplicationsList.append(awe_input.get())
        Reset_ATB()
        UpdateBlockedApplicationsData()
        reset_background_file()
        awe_window.destroy()
    global awe_window
    global awe_listbox
    try:
        if awe_window.state() == "normal":
            awe_window.destroy()
    except:
        pass

    awe_window = Toplevel(root)
    awe_window.focus()
    awe_window.title("Blocked Applications")
    awe_width=500
    awe_height=245
    awe_alignstr = f'{awe_width}x{awe_height}+{(screenwidth - awe_width) // 2}+{(screenheight - awe_height) // 2}'
    awe_window.geometry(awe_alignstr)
    awe_window.resizable(width=False, height=False)
    awe_window.attributes("-topmost", True)
    awe_savebtn=tk.Button(awe_window)
    awe_savebtn["activebackground"] = "#90ee90"
    awe_savebtn["activeforeground"] = "#ffffff"
    awe_savebtn["bg"] = "#50c878"
    awe_savebtn["borderwidth"] = "0px"
    awe_savebtn["font"] = ("",14)
    awe_savebtn["fg"] = "#ffffff"
    awe_savebtn["text"] = SaveModeDict[Mode]
    awe_savebtn["command"] = awe_save_changes
    awe_savebtn.place(x=400,y=200,width=90,height=30)
    
    awe_cancelbtn=tk.Button(awe_window)
    awe_cancelbtn["activebackground"] = "#ff0303"
    awe_cancelbtn["activeforeground"] = "#ffffff"
    awe_cancelbtn["bg"] = "#fc5151"
    awe_cancelbtn["borderwidth"] = "0px"
    awe_cancelbtn["font"] = ("",14)
    awe_cancelbtn["fg"] = "#ffffff"
    awe_cancelbtn["text"] = "Cancel"
    awe_cancelbtn["command"] = lambda: awe_window.destroy()
    awe_cancelbtn.place(x=310,y=200,width=80,height=30)
    
    awe_input=tk.Entry(awe_window)
    awe_input["borderwidth"] = "1px"
    awe_input["font"] = ("",15)
    awe_input["fg"] = "#333333"
    awe_input["borderwidth"] = "0px"
    if Mode == "e":
        awe_input.insert(0,BlockedApplicationsList[Index])
    awe_input.place(x=10,y=200,width=280,height=30)

    awe_frame = LabelFrame(awe_window,text = "Running Processes",font = ("",12))
    awe_frame["borderwidth"] = "0px"

    awe_scrollbar = Scrollbar(awe_frame)
    awe_scrollbar.pack(side="right",fill="y")

    awe_listbox = Listbox(awe_frame,yscrollcommand = awe_scrollbar.set,width=100,height=100,font=("",12),relief=FLAT,)

    awe_listbox.pack()
    awe_listbox.bind("<Button-1>", GetSelectedProcess)
    Update_Running_Processes()
    awe_frame.place(x=10,y=10,height = 175, width = 480)
    awe_scrollbar.config(command=awe_listbox.yview)





def Reset_ATB():
    #print(AppTextBox.size())
    for Index in range(AppTextBox.size()):
        AppTextBox.delete(0)
    def TempFunc():
        if ActiveSettingsScene == "Applications":
            for link in BlockedApplicationsList:
                AppTextBox.insert(END,link)
            return
            
        if ActiveSettingsScene == "Websites":
            for link in BlockedWebsitesList:
                AppTextBox.insert(END,link)
            return
    TempTime = Timer(.1,TempFunc)
    TempTime.start()

def AWE_Delete(Item):
    global BlockedApplicationsList
    #print(f"awe deleting '{Item}'")
    if ActiveSettingsScene == "Applications":
        BlockedApplicationsList.remove(Item)
        AppTextBox.delete(AppTextBox.get(0,END).index(Item))
        UpdateBlockedApplicationsData()
    if ActiveSettingsScene == "Websites":
        BlockedWebsitesList.remove(Item)
        AppTextBox.delete(AppTextBox.get(0,END).index(Item))
        UpdateBlockedWebsitesData()
    Reset_ATB()
    reset_background_file()

#one
"""Other"""
def Donate_Button_command():
    #print("DONATE")
    webbrowser.open("http://paypal.me/")

#GLabel_177=tk.Label(root)
#GLabel_177["font"] = ("", 10)
#GLabel_177["fg"] = "#333333"
#GLabel_177["justify"] = "center"
#GLabel_177["text"] = "feeling generous? "


#Donate_Button=tk.Button(root)
#Donate_Button["bg"] = "#ffffff"
#Donate_Button["borderwidth"] = "0px"
#Donate_Button["font"] = ("", 10)
#Donate_Button["fg"] = "#000000"
#Donate_Button["justify"] = "center"
#Donate_Button["text"] = 'gimmie'
#Donate_Button["command"] = #Donate_Button_command

def Uninstall_Function():
    if messagebox.askyesnocancel("Are you sure you want to uninstall?","lol this feature doesn't exist yet!"):
        print("UNISTALL!")
        #run uninstall file
Uninstall_Button=tk.Button(root)
Uninstall_Button["activebackground"] = "#000000"
Uninstall_Button["activeforeground"] = "#ffffff"
Uninstall_Button["anchor"] = "center"
Uninstall_Button["bg"] = "#fc5151"
Uninstall_Button["borderwidth"] = "0px"
Uninstall_Button["font"] = ("", 18)
Uninstall_Button["fg"] = "#ffffff"
Uninstall_Button["justify"] = "center"
Uninstall_Button["text"] = "UNINSTALL"
Uninstall_Button["relief"] = "ridge"
Uninstall_Button["command"] = Uninstall_Function

credit_text_1=tk.Label()
credit_text_1["font"] = ("", 10)
credit_text_1["fg"] = "#333333"
credit_text_1["text"] = "created by brian zhou - with much help"


def Update_Running_Processes():
    global awe_listbox
    for Index in range(awe_listbox.size()):
        awe_listbox.delete(0)
    All_Running_Apps = GetRunningProcesses()
    for Application in All_Running_Apps:
        awe_listbox.insert(END,Application)

def ba_watchtutorial_command():
    #print("app tutorial")
    webbrowser.open("http://youtube.com")

ba_watchtutorial=tk.Button(root)
ba_watchtutorial["bg"] = "#ffffff"
ba_watchtutorial["borderwidth"] = "0px"
ba_watchtutorial["font"] = ("", 10)
ba_watchtutorial["fg"] = "#000000"
ba_watchtutorial["text"] = "click here to watch tutorial"
ba_watchtutorial["command"] = ba_watchtutorial_command

"""Websites"""
def bw_watchtutorial_command():
    #print("web tutorial")
    webbrowser.open("http://youtube.com")


bw_watchtutorial=tk.Button(root)
bw_watchtutorial["bg"] = "#ffffff"
bw_watchtutorial["borderwidth"] = "0px"
bw_watchtutorial["font"] = ("", 10)
bw_watchtutorial["fg"] = "#000000"
bw_watchtutorial["text"] = "website not working? click here to watch tutorial"
bw_watchtutorial["command"] = bw_watchtutorial_command


"""Schedule"""

bn_frame = LabelFrame(root,text = "Block Nodes",font = ("",10))
bn_frame["borderwidth"] = "0px"

bn_scrollbar = Scrollbar(bn_frame)
bn_scrollbar.pack(side="right",fill="y")

bn_tree = ttk.Treeview(bn_frame,yscrollcommand = bn_scrollbar.set)
bn_tree["columns"] = ("Time","Days")
bn_tree.column("#0", width=0, stretch=NO)
bn_tree.column("Time",anchor=W,width=115,minwidth=50)
bn_tree.column("Days",anchor=W,width=115,minwidth=50)

bn_tree.heading("#0",text="",anchor=W)
bn_tree.heading("Time",text="Time",anchor=W)
bn_tree.heading("Days",text="Days",anchor=W)

bn_tree.pack()

bn_scrollbar.config(command=bn_tree.yview)

def AMPMConverter(H,M):
    if H >= 12:
        return "{}:{:02d} pm".format(H-12,M)
    else:
        return "{}:{:02d} am".format(H,M)
def Update_bn_tree():
    for record in bn_tree.get_children():
            bn_tree.delete(record)
    for ID in BTD:
        def DOW_Str(Input):
            #print(Input)
            AllDays = True
            FinalString = ""
            Running = False
            DateLength = 1
            for Date in range(7):
                if Input[Date] == False: AllDays = False
                
                if Input[Date] == True and Running == False:
                    if not FinalString == "":
                        FinalString += ","
                    FinalString += DoWAcronymList[Date][:1]
                    Running = True
                elif Input[Date] == False and Running == True:
                    if DateLength > 2:
                        FinalString += "-"+DoWAcronymList[Date-1][:1]+""
                    elif DateLength == 2:
                        FinalString += ","+DoWAcronymList[Date-1][:1]+""
                    Running = False
                elif Date == 6 and Input[Date] == True and Running == True:
                    if DateLength > 1:
                        FinalString += "-"+DoWAcronymList[Date][:1]+""
                    elif DateLength > 0:
                        FinalString += ","+DoWAcronymList[Date][:1]+""
                else:
                    DateLength += 1
            if AllDays == True:
                return "all"
            #print(FinalString)
            return FinalString
        bn_tree.insert(parent='',index=END,iid=ID,text="", values = (f"{AMPMConverter(BTD[ID][1][0],BTD[ID][1][1])} - {AMPMConverter(BTD[ID][1][2],BTD[ID][1][3])}",DOW_Str(BTD[ID][0])),tags = ID)
Update_bn_tree()


def EditButtonToggleCheck():
    def TempFunc():
        CanEdit = False
        if ActiveSettingsScene == "Schedule":
            try:
                item_values = bn_tree.item(bn_tree.focus(), 'values')
                item_tags = bn_tree.item(bn_tree.focus(), 'tags')[0]
                CanEdit = True
            except: pass

        if not AppTextBox.size() == AppTextBox.index(ANCHOR):
            CanEdit = True

        #print(CanEdit)
        if CanEdit == True:
            Edit_Button["bg"] = "#fada5e"
            Edit_Button["activebackground"] = "#ffb700"
            Edit_Button["activeforeground"] = "#ffffff"
            Edit_Button["fg"] = "#3a3b3c"
        else:
            Edit_Button["bg"] = "#808080"
            Edit_Button["activebackground"] = "#808080"
            Edit_Button["fg"] = "#ffffff"
    TempTime = Timer(.2,TempFunc)
    TempTime.start()

Edit_Button=tk.Button(root)
Edit_Button["activeforeground"] = "#ffffff"
Edit_Button["borderwidth"] = "0px"
Edit_Button["disabledforeground"] = "#ffffff"
Edit_Button["font"] = ("", 12)
Edit_Button["text"] = "Edit"
Edit_Button["command"] = lambda: Edit_Button_CMD()

def Edit_Button_CMD():
    #print("edit")
    if ActiveSettingsScene == "Websites":
        WE_Command("e",AppTextBox.index(ANCHOR))
        return
    if ActiveSettingsScene == "Applications":
        AE_Command("e",AppTextBox.index(ANCHOR))
        return
    if ActiveSettingsScene == "Schedule":
        TreeDoubleClick(None)
        return
New_Button=tk.Button(root)
New_Button["activebackground"] =  "#ffb700"
New_Button["activeforeground"] = "#ffffff"
New_Button["bg"] = "#fada5e"
New_Button["borderwidth"] = "0px"
New_Button["disabledforeground"] = "#ffffff"
New_Button["font"] = ("", 12)
New_Button["fg"] = "#3a3b3c"
New_Button["text"] = "New"
New_Button["command"] = lambda: New_Button_CMD()

def New_Button_CMD():
    if ActiveSettingsScene == "Websites":
        WE_Command("c",None)
        return
    if ActiveSettingsScene == "Applications":
        AE_Command("c",None)
        return
    if ActiveSettingsScene == "Schedule":
        SEtk_Command("c",None)
        return

def Delete_Block_Command(Block):
    global BTD
    #print(Block)
    try:
        del BTD[Block]
        UpdateSchedulePage()
        SE_Save_Changes_Function()
    except:
        pass
    

def UpdateSchedulePage():
    global Unsaved
    UpdateCBTD()
    Update_bn_tree()
    Update_TBlocks()
    EditButtonToggleCheck()
    Unsaved = True
    SaveChangesCheck()

Delete_Button=tk.Button(root)
Delete_Button["activebackground"] = "#000000"
Delete_Button["activeforeground"] = "#ffffff"
Delete_Button["bg"] = "#4b4b4b"
Delete_Button["borderwidth"] = "0px"
Delete_Button["disabledforeground"] = "#ffffff"
Delete_Button["font"] = ("", 12)
Delete_Button["fg"] = "#ffffff"
Delete_Button["command"] = lambda: Delete_Button_CMD()
Delete_Button["text"] = "Delete"

def Delete_Button_CMD():
    if ActiveSettingsScene == "Schedule":
        Delete_Block_Command(bn_tree.item(bn_tree.focus(), 'tags')[0])
    else:
        AWE_Delete(AppTextBox.get(ANCHOR))

def TreeDoubleClick(Event):
    try:
        item_values = bn_tree.item(bn_tree.focus(), 'values')
        item_tags = bn_tree.item(bn_tree.focus(), 'tags')[0]
        #print("edit!")
        SEtk_Command("e",item_tags)
    except:
        print("No item to edit")


bn_tree.bind("<Double 1>", TreeDoubleClick)
bn_tree.bind("<Button-1>", lambda e: EditButtonToggleCheck())


def SEtk_Command(Mode,Number):
    #MODES: "c": Create, "e": Edit
    global se_window
    global IB_From
    global IB_Until
    def se_save_button():
        T1 = TimeInputInterpreter(IB_From.get())
        T2 = TimeInputInterpreter(IB_Until.get())
        if T1 == None or T2 == None:
            Error_Txt["text"] = "Error: Unable to convert input into time"
        elif datetime.timedelta(hours=T1[0],minutes = T1[1]) >= datetime.timedelta(hours=T2[0],minutes = T2[1]):
            Error_Txt["text"] = "Error: 'FROM' must be less than 'UNTIL'"
        else:
            #print(type(T1))
            if Mode == "e":
                BTD[Number] = ([AffectedDates,[T1[0],T1[1],T2[0],T2[1]]])
            if Mode == "c":
                for ID in range(100):
                    if str(ID+1) in BTD:
                        continue
                    BTD[str(ID+1)] = ([AffectedDates,[T1[0],T1[1],T2[0],T2[1]]]) ##Glitch?
                    break
            #print(BTD)
            UpdateSchedulePage()
            reset_background_file()
            se_window.destroy()
            #print(T1,T2,AffectedDates)
            SE_Save_Changes_Function()
    try:
        if se_window.state() == "normal":
            se_window.destroy()
    except:
        pass
    
    global AffectedDates
    AffectedDates = [False,False,False,False,False,False,False]
    if Mode == "c" and type(Number) == int:
        AffectedDates[Number] = True
    elif Mode == "e":
        AffectedDates = BTD[Number][0]
    se_window = Toplevel(root)
    se_window.focus()
    se_window.title("Schedule Editor")
    se_width=500
    se_height=245
    se_alignstr = '%dx%d+%d+%d' % (se_width, se_height, (screenwidth - se_width) / 2, (screenheight - se_height) / 2)
    se_window.geometry(se_alignstr)
    se_window.resizable(width=False, height=False)
    se_window.attributes("-topmost", True)
    MBox_Coords = [40,20]
    Cube_Dimensions = [50,50]
    Cube_spacing = 10
    for Num in range(7):
        Cube_Block=tk.Button(se_window)
        Cube_Block["activebackground"] = "#ffffff"
        Cube_Block["fg"] = "#00000"+str(Num)
        Cube_Block["bg"] = "#ffffff"
        UpdatedDateValue = int(AffectedDates[Num])
        Cube_Block["bg"] = CubeBGColors[UpdatedDateValue]
        Cube_Block["border"] = "0px"
        Cube_Block["font"] = ("", 20)
        Cube_Block["text"] = DoWAcronymList[Num][:1]
        Cube_Block["command"] = lambda p = Num: SquareButton_command(p)
        Cube_Block.place(x=MBox_Coords[0]+(Cube_Dimensions[0]+Cube_spacing)*Num,y=MBox_Coords[1],width=Cube_Dimensions[0],height=Cube_Dimensions[1])
    se_savebtn=tk.Button(se_window)
    se_savebtn["activebackground"] = "#90ee90"
    se_savebtn["activeforeground"] = "#ffffff"
    se_savebtn["bg"] = "#50c878"
    se_savebtn["borderwidth"] = "0px"
    se_savebtn["font"] = ("",14)
    se_savebtn["fg"] = "#ffffff"
    se_savebtn["text"] = SaveModeDict[Mode]
    se_savebtn["command"] = lambda: se_save_button()
    se_savebtn.place(x=400,y=200,width=90,height=30)
    
    se_cancelbtn=tk.Button(se_window)
    se_cancelbtn["activebackground"] = "#ff0303"
    se_cancelbtn["activeforeground"] = "#ffffff"
    se_cancelbtn["bg"] = "#fc5151"
    se_cancelbtn["borderwidth"] = "0px"
    se_cancelbtn["font"] = ("",14)
    se_cancelbtn["fg"] = "#ffffff"
    se_cancelbtn["text"] = "Cancel"
    se_cancelbtn["command"] = lambda: se_window.destroy()
    se_cancelbtn.place(x=310,y=200,width=80,height=30)
    
    Error_Txt=tk.Label(se_window)
    Error_Txt["font"] = ("",10)
    Error_Txt["fg"] = "#ff0000"
    Error_Txt["text"] = ""
    Error_Txt.place(x=10,y=205,width=300,height=25)

    From_Txt=tk.Label(se_window)
    From_Txt["font"] = ("",10)
    From_Txt["fg"] = "#333333"
    From_Txt["justify"] = "left"
    From_Txt["text"] = "FROM"
    From_Txt.place(x=50,y=90,width=100,height=25)
    
    IB_From=tk.Entry(se_window)
    IB_From["borderwidth"] = "1px"
    IB_From["font"] = ("",15)
    IB_From["fg"] = "#333333"
    IB_From["justify"] = "center"
    IB_From.place(x=50,y=120,width=100,height=30)
    
    Until_Txt=tk.Label(se_window)
    Until_Txt["font"] = ("",10)
    Until_Txt["fg"] = "#333333"
    Until_Txt["text"] = "UNTIL"
    Until_Txt.place(x=350,y=90,width=100,height=25)

    IB_Until=tk.Entry(se_window)
    IB_Until["borderwidth"] = "1px"
    IB_Until["font"] = ("",15)
    IB_Until["fg"] = "#333333"
    IB_Until["justify"] = "center"
    IB_Until.place(x=350,y=120,width=100,height=30)
    
    if Mode == "e":
        AffectedTimes = BTD[Number][1]
        IB_From.insert(0,AMPMConverter(AffectedTimes[0],AffectedTimes[1]))
        IB_Until.insert(0,AMPMConverter(AffectedTimes[2],AffectedTimes[3]))




CubeBGColors = ["#ffffff","#d0f0c0"]

def SquareButton_command(Input):
    TargetFGValue = "#00000"+str(Input)
    for widget in se_window.winfo_children(): 
        if widget["fg"] == TargetFGValue:
            AffectedDates[Input] = not AffectedDates[Input]
            UpdatedDateValue = int(AffectedDates[Input])
            #print(UpdatedDateValue)
            widget["bg"] = CubeBGColors[UpdatedDateValue]
        

"""TBLOCK"""

oclock_0=tk.Label(root)
oclock_0["font"] = ("", 12)
oclock_0["text"] = "0:00"

oclock_6=tk.Label(root)
oclock_6["font"] = ("", 12)
oclock_6["text"] = "6:00"

oclock_12=tk.Label(root)
oclock_12["font"] = ("", 12)
oclock_12["text"] = "12:00"

oclock_18=tk.Label(root)
oclock_18["font"] = ("", 12)
oclock_18["text"] = "18:00"

oclock_24=tk.Label(root)
oclock_24["font"] = ("", 12)
oclock_24["text"] = "24:00"


ActiveSettingsScene = None
def SettingsSwitchScene(Target):
    global ActiveSettingsScene
    
    #Clear Scnene
    if Target == None or ActiveSettingsScene != Target:
        #Erase
        if ActiveSettingsScene == "Applications":
            ba_frame.place_forget()
            #GButton_177.place_forget()
            ba_watchtutorial.place_forget()
            Edit_Button.place_forget()
            New_Button.place_forget()
            Delete_Button.place_forget()
            GSImageFrame.place_forget()
            
        if ActiveSettingsScene == "Schedule":
            for widget in root.winfo_children(): #Removes all tblocks
                if widget["bg"] == BlockBGHex or widget["bg"] == ColumnBGHex:
                    widget.place_forget()
                try:
                    for Day in DoWAcronymList:
                        if widget["text"] == Day:
                            widget.place_forget()
                except:
                    pass
            oclock_0.place_forget()
            oclock_6.place_forget()
            oclock_12.place_forget()
            oclock_18.place_forget()
            oclock_24.place_forget()
            bn_frame.place_forget()
            Edit_Button.place_forget()
            New_Button.place_forget()
            Delete_Button.place_forget()
        
        if ActiveSettingsScene == "Websites":
            ba_frame.place_forget()
            bw_watchtutorial.place_forget()
            Edit_Button.place_forget()
            New_Button.place_forget()
            Delete_Button.place_forget()
            OctImageFrame.place_forget()
        if ActiveSettingsScene == "Other":
            #GLabel_177.place_forget()
            #Donate_Button.place_forget()
            Uninstall_Button.place_forget()
            credit_text_1.place_forget()
            others_title_text.place_forget()
            #GSImageFrame.place_forget()
            #print("erase")

    #Set Scene
    #Draw
    ba_frame["text"]= f"Blocked {Target}"
    if Target == "Applications":
        ba_frame.place(x=80,y=100,height = 280, width = 550)
        #GButton_177.place(x=80,y=400,width=200,height=30)
        ba_watchtutorial.place(x=433,y=400,width=200,height=30)
        Edit_Button.place(x=860,y=340,width=110,height=30)
        New_Button.place(x=740,y=340,width=110,height=30)
        Delete_Button.place(x=780,y=380,width=150,height=30)
        GSImageFrame.place(x=730,y=90)
        EditButtonToggleCheck()
        Reset_ATB()

    if Target == "Websites":
        ba_frame.place(x=80,y=100,height = 280, width = 550)
        AppTextBox.delete(0,END)
        for link in BlockedWebsitesList:
            AppTextBox.insert(END,link+"\n")
        bw_watchtutorial.place(x=333,y=400,width=300,height=30)
        Edit_Button.place(x=860,y=340,width=110,height=30)
        New_Button.place(x=740,y=340,width=110,height=30)
        Delete_Button.place(x=780,y=380,width=150,height=30)
        OctImageFrame.place(x=720,y=100) 
        EditButtonToggleCheck()
        Reset_ATB()
    if Target == "Schedule":
        #Column Maker
        Edit_Button.place(x=860,y=340,width=110,height=30)
        New_Button.place(x=740,y=340,width=110,height=30)
        Delete_Button.place(x=780,y=380,width=150,height=30)
        bn_frame.place(x=740,y=120,height = 200, width = 230)
        for Num in range(7):
            TColumn=tk.Button(root)
            TColumn["activebackground"] = "#ffffff"
            TColumn["bg"] = ColumnBGHex
            TColumn["font"] = ("", 10)
            TColumn["text"] = ""
            TColumn["command"] = lambda p = Num: SEtk_Command("c",p)
            TColumn.place(x=Mon_Coords[0]+(Box_Dimensions[0]+Column_spacing)*Num,y=Mon_Coords[1],width=Box_Dimensions[0],height=Box_Dimensions[1])
            
            Column_Text=tk.Label(root)
            Column_Text["font"] = ("", 13)
            Column_Text["fg"] = "#333333"
            Column_Text["text"] = DoWAcronymList[Num]
            Column_Text.place(x=Mon_Coords[0]+(Box_Dimensions[0]+Column_spacing)*Num+(Box_Dimensions[0]-CTwidth)/2,y=Mon_Coords[1]+Box_Dimensions[1]+CTConstant,width = CTwidth)
        oclock_0.place(x=Mon_Coords[0]-Ruler_spacing[0]+10,y=Mon_Coords[1]-Ruler_spacing[1])
        oclock_6.place(x=Mon_Coords[0]-Ruler_spacing[0]+10,y=Mon_Coords[1]-Ruler_spacing[1]+Box_Dimensions[1]/4)
        oclock_12.place(x=Mon_Coords[0]-Ruler_spacing[0],y=Mon_Coords[1]-Ruler_spacing[1]+Box_Dimensions[1]/2)
        oclock_18.place(x=Mon_Coords[0]-Ruler_spacing[0],y=Mon_Coords[1]-Ruler_spacing[1]++Box_Dimensions[1]*3/4)
        oclock_24.place(x=Mon_Coords[0]-Ruler_spacing[0],y=Mon_Coords[1]-Ruler_spacing[1]+Box_Dimensions[1])
        EditButtonToggleCheck()
        #BLOCKS
        Update_TBlocks()
    
    if Target == "Other":
        donate_textx = [770,385]
        #GLabel_177.place(x=donate_textx[0],y=donate_textx[1],width=145,height=30)
        #Donate_Button.place(x=donate_textx[0]+130,y=donate_textx[1],width=70,height=30)
        Uninstall_Button.place(x=385,y=410,width=230,height=50)
        credit_text_1.place(x=0,y=470,width=250,height=30)
        others_title_text.place(x=200,y=150,width=600,height=100)
        #GSImageFrame.place(x=730,y=140)

    if Target == None:
        Save_Button.place_forget()
        Cancel_Button.place_forget()
        Back_Button.place_forget()
    else:
        SaveChangesCheck()
    #print(Target,"from",ActiveSettingsScene)
    ActiveSettingsScene = Target

def Update_TBlocks():
    for widget in root.winfo_children(): #Removes all tblocks
        if widget["bg"] == BlockBGHex:
            widget.place_forget()
    for Day in ConvertedBTData:
        TodaysBlocks = ConvertedBTData[Day]
        for Block in TodaysBlocks:
            BlockTimeLength = datetime.timedelta(hours=TodaysBlocks[Block][2]-TodaysBlocks[Block][0],minutes=TodaysBlocks[Block][3]-TodaysBlocks[Block][1])
            BlockYUni = datetime.timedelta(hours=TodaysBlocks[Block][0],minutes=TodaysBlocks[Block][1]).seconds/3600/24*Box_Dimensions[1]
            TBlock=tk.Button(root)
            TBlock["activebackground"] = "#393d49"
            TBlock["bg"] = BlockBGHex
            TBlock["font"] = ("", 10)
            TBlock["fg"] = "#000000"
            TBlock["justify"] = "center"
            TBlock["text"] = ""
            TBlock["borderwidth"] = "0px"
            TBlock["command"] = lambda p = Block:SEtk_Command("e",p)
            TBlock.place(x=Mon_Coords[0]+Box_Dimensions[0]*(int(Day)-1)+Column_spacing*(int(Day)-1),y=Mon_Coords[1]+BlockYUni,width=Box_Dimensions[0],height=BlockTimeLength.seconds/3600/24*Box_Dimensions[1])


def SecondsUntilTomorrow():
    CurrentTime = datetime.datetime.now()
    OneDay = datetime.timedelta(days=1)
    TomorrowMorning = (CurrentTime+OneDay).replace(hour=0, minute=0, second=3, microsecond=0)
    SecondsUntilTomorrowVariable = (TomorrowMorning - CurrentTime).seconds
    #print(SecondsUntilTomorrowVariable,"seconds until tomorrow")
    return SecondsUntilTomorrowVariable


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
            ##print(DictValue,KeyValue)
            if (DictValue == CurrentTime.hour and KeyValue > CurrentTime.minute) or DictValue > CurrentTime.hour:
                NextTimeVariable.append(DictValue)
                NextTimeVariable.append(KeyValue)
                break
        if not NextTimeVariable == []:
            break
    #LETS GOO buddy
    if NextTimeVariable == []:
        #print("No more time blocks left today!")
        return None
    NextActivityCheckup = CurrentTime.replace(hour=NextTimeVariable[0], minute=NextTimeVariable[1], second=3, microsecond=0)
    SecondsUntilCheckupVariable = (NextActivityCheckup-CurrentTime).seconds
    ##print("Next checkup time",str(NextTimeVariable[0])+":"+str(NextTimeVariable[1]),"("+str(SecondsUntilCheckupVariable)+" seconds)")
    ##print(SecondsUntilCheckupVariable,"seconds until next checkup.")
    return SecondsUntilCheckupVariable

def TimeBlockCompareFunction(H1,M1,H2,M2):
    ##print(str(H1)+":"+str(M1),str(CurrentHour)+":"+str(CurrentMinute),str(H2)+":"+str(M2))
    if not CurrentHour >= H1 or not CurrentHour <= H2:
        return False
    if CurrentHour == H1 and CurrentMinute < M1:
        return False
    if CurrentHour == H2 and CurrentMinute >= M2:
        return False
    return True


def ShouldScriptRunTest():
    #print("def should script run test")
    global CurrentHour
    global CurrentMinute
    CurrentHour = datetime.datetime.now().hour
    CurrentMinute = datetime.datetime.now().minute
    for TimeInterval in TodaysHours:
        if TimeBlockCompareFunction(TodaysHours[TimeInterval][0],TodaysHours[TimeInterval][1],TodaysHours[TimeInterval][2],TodaysHours[TimeInterval][3]):
            return True
    return False

def NextBlockIsHere():
    global NextBlockTimer
    #print("Next block is here!")
    global IsScriptActive
    IsScriptActive = ShouldScriptRunTest()
    #print("Script is",IsScriptActive)
    #Start timer for next blockcheckup
    if not SecondsUntilCheckup() == None:
        #print("NextTimer started")
        NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
        NextBlockTimer.start()
        #print(SecondsUntilCheckup,"seconds until next checkup.")
    UpdateMenu() #shouldnt do anything is block is false

def TomorrowIsHere():
    global TomorrowTimer
    global NextBlockTimer
    #print("Tomorrow is here!")
    global CurrentWeekDay
    global TodaysHours
    CurrentWeekDay = str(datetime.datetime.today().weekday() + 1) 
    TodaysHours = ConvertedBTData[CurrentWeekDay]
    TomorrowTimer = Timer(SecondsUntilTomorrow(),TomorrowIsHere)
    TomorrowTimer.start()
    NextBlockTimer.cancel()
    NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
    NextBlockTimer.start()
    UpdateMenu() #shouldnt do anything is block is false

def CancelTimerLoop():
    global TomorrowTimer
    global NextBlockTimer
    try:
        NextBlockTimer.cancel()
        TomorrowTimer.cancel()
        sub_timer.cancel()
    except:pass
    #print("canceling timers")

def UpdateMenuLoop():
    print("gts",get_break_time_seconds())
    BreakTimer = Timer(get_break_time_seconds()+3,InitiateTimer)
    BreakTimer.start()
    UpdateMenu()

def UpdateMenu():
    break_time_seconds = get_break_time_seconds()
    IsScriptActive = ShouldScriptRunTest()
    print(IsScriptActive,"is script active")
    OnBreak = False
    if break_time_seconds > 0:
        OnBreak = True
    print(f"ON BREAK? {OnBreak}")
    if IsScriptActive:
        if OnBreak:
            print("disabling")
            menu_title_text["text"] = "enjoy wasting time"
            break_work_btn["text"] = "get back to work"
            break_work_btn["command"] = lambda: take_break_cmd(False)
            menu_sub_text["text"] = ""
        else:
            print("Break Enabled!")
            menu_title_text["text"] = "do your work"
            break_work_btn["text"] = "take a break"
            break_work_btn["command"] = lambda: break_Command()
        #here
    else:
        if OnBreak:
            menu_title_text["text"] = "you're working hard"
            break_work_btn["text"] = "take a rest"
            break_work_btn["command"] = lambda: take_break_cmd(False)
        else:
            menu_title_text["text"] = "Yay! No Restrictions!"
            break_work_btn["text"] = "Do Some Work"
            break_work_btn["command"] = lambda: break_Command()
    sub_timer_function()

def get_break_time_seconds(): 
    try:
        BreakTimeFile = open(BreakTimePath,"r")
        break_time_string = BreakTimeFile.readline()
        print(BreakTimePath,break_time_string)
        BreakTimeFile.close()
        converted_break_time = datetime.datetime.strptime(break_time_string,r"%Y-%m-%d %H:%M:%S.%f")
        time_difference = converted_break_time-datetime.datetime.now()
        if time_difference > datetime.timedelta(seconds=0):
            return time_difference.seconds
        else:
            BreakTimeFile = open(BreakTimePath,"w")
            BreakTimeFile.close()
    except:
        return int(0)

def InitiateTimer():
    global TomorrowTimer
    global NextBlockTimer
    global IsScriptActive
    IsScriptActive = ShouldScriptRunTest()
    TomorrowTimer = Timer(SecondsUntilTomorrow(),TomorrowIsHere)
    TomorrowTimer.start()
    NextBlockTimer = Timer(SecondsUntilCheckup(),NextBlockIsHere)
    NextBlockTimer.start()
    UpdateMenu() #This is needed!

def sub_timer_function():
    #print("def updating subtitle timer")
    global sub_timer
    try:sub_timer.cancel()
    except:pass
    sub_timer = Timer(60,sub_timer_function)
    sub_timer.start()
    break_time = get_break_time_seconds()
    if ShouldScriptRunTest() and break_time == 0:
        menu_sub_text["text"] = f"{SecondsUntilCheckup()//3600}h {SecondsUntilCheckup()%3600//60+1} minutes left"
    elif break_time == 0:
        menu_sub_text["text"] = "enjoy life"
    else:
        menu_sub_text["text"] = f"{break_time//60+1}m minutes left"

def TimeInputInterpreter(Input):
    Input = Input.replace(":"," ")
    SplitInput = Input.split()
    SplitImpNum = []
    Hour = None
    Minute = None
    for KeyIndex in range(len(SplitInput)):
        KeyWord = SplitInput[KeyIndex]
        AMPM = None
        try:
            KeyWord = int(KeyWord)
            SplitImpNum.append(KeyWord)
        except:
            if 'p' in KeyWord:
                AMPM = "pm"
    
    if len(SplitImpNum) == 2:
        Hour = SplitImpNum[0]
        Minute = SplitImpNum[1]
    elif len(SplitImpNum) == 1:
        Hour = SplitImpNum[0]
        Minute = 0
    try:
        if Hour > 24:
            Hour = 24
        if Minute > 60:
            Minute = 60
        if AMPM == "pm" and Hour <= 12:
            Hour += 12
        if Hour >= 24:
            Minute = 0
    except:
        return None
    return [Hour,Minute]

def GetRunningProcesses(): #here
    os.system(f"tasklist > {TasksListFilePath}")
    RunningAppsList = []
    AppsListFilter = []
    TasksFile = open(TasksListFilePath,"r+")
    #print("Successful!")
    ##print(TasksFile.read())
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
            ##print(CurrentLine[5:])
    TasksFile.close()
    TasksFile = open(TasksListFilePath,"w")
    TasksFile.write(str(RunningAppsList))
    TasksFile.close()
    for Application in RunningAppsList:
        ##print(Application)
        if not ".exe" in Application:
            AppsListFilter.append(Application)
        elif Application in ProtectedAppsList:
            AppsListFilter.append(Application)

    RunningAppsList.sort()
    for Application in AppsListFilter:
        RunningAppsList.remove(Application)
    return RunningAppsList



def SwitchScene(New,Old):
    global Unsaved
    #New
    if New == "Menu":
        SettingsButton.place(x=910,y=30,width=50,height=50)
        menu_title_text.place(x=200,y=150,width=600,height=100)
        menu_sub_text.place(x=400,y=310,width=200,height=25)
        break_work_btn.place(x=770,y=420,width=200,height=50)
        UpdateMenuLoop()
    if New == "Settings":
        Unsaved = False
        GButton_492.place(x=80,y=20,width=200,height=50)
        GButton_827.place(x=310,y=20,width=200,height=50)
        GButton_53.place(x=540,y=20,width=200,height=50)
        GButton_866.place(x=770,y=20,width=200,height=50)
        SettingsSwitchScene("Applications")
       
    #Old
    if Old == "Menu":
        SettingsButton.place_forget()
        menu_title_text.place_forget()
        menu_sub_text.place_forget()
        break_work_btn.place_forget()
        CancelTimerLoop()
    if Old == "Settings":
        GButton_492.place_forget()
        GButton_827.place_forget()
        GButton_53.place_forget()
        GButton_866.place_forget()

        SettingsSwitchScene(None)
SwitchScene("Menu",None)

def SaveChangesCheck():
    Save_Button.place_forget()
    Cancel_Button.place_forget()
    Back_Button.place_forget()
    if Unsaved == True:
        Save_Button.place(x=860,y=440,width=110,height=30)
        Cancel_Button.place(x=740,y=440,width=110,height=30)
    else:
        Back_Button.place(x=860,y=440,width=110,height=30)
        
#####################

root.mainloop()