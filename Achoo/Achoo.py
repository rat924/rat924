'''
Ideen:
NET - Könnte eine mächtige Funktion für Netzwerkfunktionen werden, jedoch finde ich bis jetzt nichts sinnvolles
'''
ver="0.3138"
Titel="Achoo"
_windows = {}
_entries = {}
current_indices = {}
import sys
import builtins
import smtplib
import zipfile
import pickle
import shutil
import msvcrt

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

original_print = builtins.print
def print_with_flush(*args, **kwargs):
    original_print(*args, **{**kwargs, 'flush': True})
builtins.print = print_with_flush

import tkinter as tk
import ctypes
import keyboard
import xml.etree.ElementTree as ET
import winreg
import pyodbc
import threading
import tkinter as tk
import importlib

from tkinter import ttk
from tkinter import filedialog
from sys import exit,argv
from os import system,path,walk,listdir,getcwd,makedirs,environ,remove,startfile
from fnmatch import fnmatch
import datetime
from time import ctime
import time
from tkinter import messagebox
from tkinter import simpledialog
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MController
from pynput.mouse import Button
from subprocess import check_output
from time import sleep as sleeep
from urllib.request import urlretrieve
from json import load, dump
from random import randint

global ENDE
ENDE=0
global file_content
file_content=[]

global start_time
start_time = time.time()

global LOG
LOG=0

global insub
insub=None
global loop_stack
loop_stack=[]

global Seperator1, Seperator2, Variable_Marker,Email_From,Email_SMTP,Email_User,Email_Password,fernet


if path.exists("Achoo.cfg"):
    with open("Achoo.cfg",encoding="UTF-8") as f:
        for line in f:
            Name,Value=line.split("=",1)
            globals()[Name.strip()]=Value.strip()
else:
    Variable_Marker="%"
    Seperator1="|"
    Seperator2="||"
    LineSeperator="::"
    with open("Achoo.cfg","w") as f:
        f.write("Variable_Marker="+Variable_Marker+"\nSeperator1="+Seperator1+"\nSeperator2="+Seperator2+"\nLineSeperator="+LineSeperator+"\nEmail_From=\nEmail_SMTP=\nEmail_User=\nEmail_Password=")


global answers
answers={}
answers.update({"Seperator1":str(Seperator1)})
answers.update({"Seperator2":str(Seperator2)})
answers.update({"LineSeperator":str(LineSeperator)})

x=0
line=""
global EXC
EXC=1
system("title "+Titel+" "+ver)

BlackList= []
try:
    with open("blacklist","r") as f:
        for row in f:
            BlackList.append(row.lower().strip())
except:
    pass

subs={}
for file in listdir():
    if file.endswith('.sub'):
        name=file[0:-4].lower()
        sub=[]
        with open(file,"r") as f:
            for row in f:
                sub.append(row.strip())
        subs[name]=sub


#fernet=Fernet("add your own fernet!")

def Commands(com):
    WriteLog(com+"\n")
    whole=com
    command=(com.lower()[0:3])
    for row in BlackList:
        if row in com.lower():
            return
    lines=com.split(LineSeperator)
    if len(lines)>=2:
        for lin in lines:
            Commands(lin)
        return
    com=com[4:]
    global Var
    Var=com.split(Seperator1)[0]
    #WriteLog(command+" "+com+"\n")
    temp=com
    if whole.lower()=="setup":
        Setup()
    if Variable_Marker in com:# and command!="win":
         com=Decode(Variable_Marker+com+Variable_Marker)
    if temp!=com:
        WriteLog(">" +command+" "+com+"\n")
    if command.lower()=="exe":EXE(com)
    elif command.lower()=="fod":FolderDialog(com)
    elif command.lower()=="fid":FileDialog(com)
    elif command.lower()=="ted":TextDialog(com)
    elif command.lower()=="log":Log(com)
    elif command.lower()=="cmd":CMD(com)
    elif command.lower()=="wrf":WriteFile(com)
    elif command.lower()=="crf":CreateFolder(com)
    elif command.lower()=="ifc":Commands(IFCondition(com))
    elif command.lower()=="get":Get(com)
    elif command.lower()=="qut":Qut(com)
    elif command.lower()=="men":Menu(com)
    elif command.lower()=="set":Set(com)
    elif command.lower()=="got":Goto(com)
    elif command.lower()=="ref":Readfile(com)
    elif command.lower()=="que":Question(com)
    elif command.lower()=="sea":Search(com)
    elif command.lower()=="gel":GetLine(com)
    elif command.lower()=="wrl":WriteLine(com)
    elif command.lower()=="str":Strip(com)
    elif command.lower()=="rem":pass
    elif command.lower()=="rsv":ReplaceStringVariable(com)
    elif command.lower()=="cal":Calculate(com)
    elif command.lower()=="exe":Commands(com)
    elif command.lower()=="dat":Date(com)
    elif command.lower()=="tim":Time(com)
    elif command.lower()=="foe":FolderExists(com)
    elif command.lower()=="fie":FolderExists(com)
    elif command.lower()=="sst":ServiceStatus(com)
    elif command.lower()=="ton":TaskOnline(com)
    elif command.lower()=="dnl":Download(com)
    elif command.lower()=="rxm":ReadXML(com)
    elif command.lower()=="wxm":WriteXML(com)
    elif command.lower()=="rjs":ReadJSon(com)
    elif command.lower()=="wjs":WriteJSon(com)
    elif command.lower()=="tit":Title(com)
    elif command.lower()=="rsf":ReplaceStringFile(com)
    elif command.lower()=="bgr":Background(com)
    elif command.lower()=="fgr":Foreground(com)
    elif command.lower()=="spl":Split(com)
    elif command.lower()=="slp":Sleep(com)
    elif command.lower()=="loc":Locate(com)
    elif command.lower()=="cls":CLS()
    elif command.lower()=="kyi":KeyInput(com)
    elif command.lower()=="brk":Break()
    elif command.lower()=="kyo":KeyOutput(com)
    elif command.lower()=="rnd":Random(com)
    elif command.lower()=="inp":ConsoleInput(com)
    elif command.lower()=="ver":Version(com)
    elif command.lower()=="mou":Mouse(com)
    elif command.lower()=="hlp":Help(com)
    elif command.lower()=="kiw":KeyInputWait(com)
    elif command.lower()=="   ":exec(Decode(whole[3:]),globals())
    elif command.lower()=="win":Window(com)
    elif command.lower()=="sqi":SQLInstances(com)
    elif command.lower()=="sub":SUB(com)
    elif command.lower() == "thr":ThreadCommand(com)
    elif command.lower() == "snd":SendEmail(com)
    elif command.lower() == "dbq":DatabaseQuery(com)
    elif command.lower() == "req":Requirement(com)
    elif command.lower() == "cry":Crypt(com)
    elif command.lower() == "zip":Zip(com)
    elif command.lower() == "add":Addon(com)
    elif command.lower() == "for":For(com)
    elif command.lower() == "whi":While(com)
    elif command.lower() == "len":Len(com)
    elif command.lower() == "kow":KeyOutputWait(com)
    elif command.lower() == "sav":Save(com)
    elif command.lower() == "loa":Load(com)
    elif command.lower() == "env":Environment(com)
    elif command.lower() == "fil":FileManagement(com)
    elif command.lower() == "aut":Authentification(com)
    elif command.lower() == "any":AnyKey(com)
    elif command.lower() == "tmr":Timer(com)
    elif command.lower() == "sch":Scheduler(com)
    elif command.lower() == "!!!":EasterEgg(com)    
    elif command.lower() == "wnd" or command.lower() == "nxt" or command.lower()=="bwi" or command.lower()=="cwi":pass
    elif command=="":pass
    else:
        Log(command+" - Command not found!")

def Setup():
    global LineSeperator,Seperator1, Seperator2, Variable_Marker,Email_From,Email_SMTP,Email_User,Email_Password,fernet
    print("SETUP")
    print("=====")
    print()
    print("1. Change Variable_Marker ("+Variable_Marker+")")
    print("2. Change Seperator1 ("+Seperator1+")")
    print("3. Change Seperator2 ("+Seperator2+")")
    print("4. Change LineSeperator ("+LineSeperator+")")
    print("5. Config E-Mail ("+Email_From+")")
    selection = input("Select an option (1-5): ")
    
    if selection == '1':
        new_value = input("Enter new value for Variable_Marker: ")
        Variable_Marker=new_value
    elif selection == '2':
        new_value = input("Enter new value for Seperator1: ")
        Seperator1 = new_value
    elif selection == '3':
        new_value = input("Enter new value for Seperator2: ")
        Seperator2 = new_value
    elif selection == '4':
        new_value = input("Enter new value for LineSeperator: ")
        LineSeperator = new_value
    elif selection == '5':
        new_value = input("Enter new value for Email_From: ")
        Email_From = new_value
        new_value = input("Enter new value for Email_SMTP: ")
        Email_SMTP = new_value
        new_value = input("Enter new value for Email_User: ")
        Email_User = new_value
        new_value = input("Enter new value for Email_Password: ")
        Crypt("Password"+Seperator1+new_value+Seperator1+"achoo")
        Email_Password = answers['Password']
    else:
        print("Invalid selection.")
        return
    with open("Achoo.cfg","w") as f:
        f.write("Variable_Marker="+Variable_Marker+"\nSeperator1="+Seperator1+"\nSeperator2="+Seperator2+"\nLineSeperator="+LineSeperator+"\nEmail_From="+Email_From+"\nEmail_SMTP="+Email_SMTP+"\nEmail_User="+Email_User+"\nEmail_Password="+Email_Password)
    print("Saved new config.")

def EasterEgg(com):
    import winsound
    note_frequencies = {
    "H3":247,
    "C4": 261,
    "C#4": 277,
    "D4": 294,
    "D#4": 311,
    "E4": 329,
    "F4": 349,
    "F#4": 370,
    "G4": 392,
    "G#4": 415,
    "A4": 440,
    "A#4": 466,
    "B4": 494,
    }
    melody = [
        ("G4", 0.25),
        ("F4", 0.125),
        ("E4", 0.125),
        ("D4", 0.125),
        ("C4", 0.125),
        ("D4", 0.125),
        ("E4", 0.125),
        ("C4", 0.125),
        ("D4", 0.0625),
        ("E4", 0.0625),
        ("F4", 0.0625),
        ("D4", 0.0625),
        ("E4", 0.25),
        ("D4", 0.0625),
        ("C4", 0.0625),
        ("H3", 0.0625),
        ("C4", 0.25)        
    ]
    def Play(Note,Länge):
        if Note in note_frequencies:
            frequency=note_frequencies[Note]
            duration=int(Länge*2000)
            winsound.Beep(frequency,duration)
    for note, length in melody:
        Play(note,length)
    print("🎄 Merry Christmas! 🎄")
    
def Scheduler(com):
    global running
    if com.lower() == "stop":
        running = False
        return

    command, function, interval = com.split(Seperator1)
    interval = float(interval)

    def wrapper():
        global running
        running = True
        while running:
            Commands(function)
            time.sleep(interval)

    if command.lower() == "start":
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()

def Timer(com):
    elapsed_time = str(time.time() - start_time)
    if com!="":
        answers.update({com:elapsed_time})
    else:
        print(elapsed_time)

def AnyKey(com):
    print("Press any key to continue...")
    while True:
        keyboard.read_event()
        if keyboard.read_event():
            return

def Authentification(com):
    if ctypes.windll.shell32.IsUserAnAdmin() == False:
        print("This script needs administrator rights...")
        AnyKey(None)
        Break()
        

def FileManagement(com):
    parts = com.split(Seperator1)
    action = parts[0].strip().lower()
    paths = parts[1:]
    try:
        if action == 'copy' and len(paths) == 2:
            source, destination = paths
            shutil.copy(source.strip(), destination.strip())

        elif action == 'move' and len(paths) == 2:
            source, destination = paths
            shutil.move(source.strip(), destination.strip())
            
        elif action == 'delete' and len(paths) == 1 or action == 'remove' and len(paths) == 1:
            file_path = paths[0]
            remove(file_path.strip())

        elif action == 'execute' and len(paths) == 1:
            file_path = paths[0]
            startfile(file_path.strip())
    except Exception as e:
        print(e)

def Environment(com):
    answers.update({var: environ.get(var) for var in environ})

def Load(com):
    global answers
    answers={}
    with open(com,"rb") as file:
        answers = pickle.load(file)

def Save(com):
    with open(com,"wb") as file:
        pickle.dump(answers,file)

def KeyOutputWait(com):
    keyboard = Controller()
    text, duration = com.split(Seperator1)
    duration = float(duration)

    for char in text:
        if char == ' ':
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif char.isalpha() and char.isupper():  
            keyboard.press(Key.shift)  
            keyboard.press(char)       
            sleeep(duration)
            keyboard.release(char)     
            keyboard.release(Key.shift) 
        else:
            keyboard.press(char)
            sleeep(duration)
            keyboard.release(char)   

        sleeep(duration)
    return

def Len(com):
    if len(com.split(Seperator1))==2:
        Variable,Var=com.split(Seperator1)
        Len=len(Var)
    else:
        Variable,Var,Split=com.split(Seperator1)
        Len=len(Var.split(Split))
    answers.update({Variable:str(Len)})


def While(com):
    global x
    global insub
    global sub
    tmp=x
    try:
        parts = [part.strip() for part in com.split(Seperator1)]
        if len(parts) != 3:
            return
            

        var1 = parts[0].strip(Variable_Marker)  
        operator = parts[1]          
        var2 = parts[2].strip(Variable_Marker)    

        def get_value(var):
            if var in answers:
                return float(answers[var]) 
            try:
                return float(var)
            except ValueError:
                return
            

        value1 = get_value(var1) 
        value2 = get_value(var2) 

        line = ""
        WhileLoop = []
        x += 1
        if insub:
            temp=x
            line = subs[sub][x]
            while line.lower() != "wnd":
                WhileLoop.append(line)
                x += 1
                line = subs[sub][x]
            
        else:
            line = file_content[x - 1]
            while line.lower() != "wnd":
                WhileLoop.append(line)
                x += 1
                line = file_content[x - 1] if x - 1 < len(file_content) else "wnd"
        if "whi" in WhileLoop[0].lower():
            WhileLoop.pop(0)
        while eval(f"{value1} {operator} {value2}"):
            continue_is_on=False
            for command in WhileLoop:
                if continue_is_on:
                    x=tmp
                    
                    break
                if command.lower()[:3]=="ifc":
                    if IFCondition(Decode(command[4:])).lower()=="bwi":
                        x=tmp
                        return
                    if IFCondition(Decode(command[4:])).lower()=="cwi":
                        continue_is_on=True
                    else:
                        Commands(command)
                else:
                    Commands(command)
                value1 = get_value(var1)  
                value2 = get_value(var2)
        x=tmp
        return
    except Exception as e:
        pass

def For(com):
    global x
    loop_stack = []
    parts = com.split(Seperator1)
    if len(parts) == 3:
        Variable, From, To = parts
        Step = 1
    else:
        Variable, From, To, Step = parts

    loop_context = {
        'variable': Variable,
        'from': int(From),
        'to': int(To)+1,
        'step': int(Step),
        'index': 0
        }
    loop_stack.append(loop_context)
    ForLoop = []        
    if insub:
        while True:
            line = subs[sub][x]
            if line.lower().startswith("nxt "):
                nxt_variable = line.split()[1]
                if nxt_variable != Variable:
                    x -= 1
                    break
                else:
                    break
            ForLoop.append(line)
            x += 1
    else:
        while True:
            line = file_content[x]
            if line.lower().startswith("nxt "):
                nxt_variable = line.split()[1]
                if nxt_variable != Variable:
                    x -= 1
                    break
                else:
                    break
            ForLoop.append(line)
            x += 1

    for loop in range(loop_context['from'], loop_context['to'], loop_context['step']):
        answers[loop_context['variable']] = str(loop)
        for command in ForLoop:
            if loop<loop_context['to']-1:
                Commands(command)
    x -= 1

def Addon(com):
    Variable,Library, Function, Parameters = com.split(Seperator1)
    if not path.exists(f"{Library}.py"):
        raise ImportError(f"{Library}.py not found!")

    spec = importlib.util.spec_from_file_location(Library, f"{Library}.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    function = getattr(modul, Function)
    execute=function(Parameters)
    if execute!="":
        answers.update({Variable:str(execute)})
    

def Zip(com):
    func=com.split(Seperator1)[0]
    filename=com.split(Seperator1)[1]
    if func.lower()=="zip":
        files=com.split(Seperator1)[2:]
        with zipfile.ZipFile(filename,"w") as zipf:
            for file in files:
                try:
                    zipf.write(file)
                except Exception as e:
                    print(e)
    if func.lower()=="unzip":
        folder=com.split(Seperator1)[2]
        try:
            with zipfile.ZipFile(filename,"r") as zipf:
                zipf.extractall(folder)
        except Exception as e:
            print(e)


    
def Crypt(com):
    crypt="ASS"+str(fernet.encrypt(com.encode())).split("'")[1]
    if len(com.split(Seperator1))==2:
        variable,password=com.split(Seperator1)
        crypt="ASS"+str(fernet.encrypt(password.encode())).split("'")[1]
        answers.update({variable:crypt})
    elif len(com.split(Seperator1))==3:
        variable,password,word=com.split(Seperator1)
        while word.lower() not in crypt.lower():
            crypt="ASS"+str(fernet.encrypt(password.encode())).split("'")[1]
        answers.update({variable:crypt})
        
    else:
        crypt="ASS"+str(fernet.encrypt(com.encode())).split("'")[1]
        print(crypt)
    

def Requirement(com):
    if float(com)>float(ver):
        print("Your version is too old to run this script. Please update to the latest version to proceed.")
        sys.exit()

def DatabaseQuery(com):
    variable, server, database, benutzer, passwort, query = com.split(Seperator1)
    
    if passwort[:3] == "ASS":
        passwort = passwort[3:].encode()
        passwort = str(fernet.decrypt(passwort)).split("'")[1]
    
    verbindung_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={benutzer};PWD={passwort};'
    
    try:
        with pyodbc.connect(verbindung_string) as verbindung:
            cursor = verbindung.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                ergebnisse = cursor.fetchall()
                formatted_results = []
                for row in ergebnisse:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_results.append(formatted_row)  
                answers.update({variable: ' | '.join(formatted_results)})
            else:
                verbindung.commit()
                answers.update({variable: "Update successful"})
    
    except pyodbc.Error as e:
        if "Login failed" in str(e):
            print("Login failed. Please check your credentials.")
        else:
            print(f"An error occurred: {e}")
        try:
            verbindung_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            with pyodbc.connect(verbindung_string) as verbindung:
                cursor = verbindung.cursor()
                cursor.execute(query)
                
                if query.strip().upper().startswith("SELECT"):
                    ergebnisse = cursor.fetchall()
                    formatted_results = []
                    for row in ergebnisse:
                        formatted_row = ', '.join(str(value) for value in row)
                        formatted_results.append(formatted_row)
                    answers.update({variable: ' | '.join(formatted_results)})
                else:
                    verbindung.commit()
                    answers.update({variable: "Update successful"})
        
        except Exception as e:
            print(f"An error occurred during trusted connection: {e}")

   

def SendEmail(com):
    parts = com.split(Seperator1)
    password=Email_Password[3:].encode()
    password=str(fernet.decrypt(password)).split("'")[1]
    
    if len(parts) == 4:
        variable,empfaenger, betreff, nachricht = parts
        datei = None
    elif len(parts) == 5:
        variable,empfaenger, betreff, nachricht, datei = parts
    else:
        answers.update({variable: "Invalid input format. Expected 3 or 4 parts separated by '|'."})
        return

    msg = MIMEMultipart()
    msg['From'] = Email_From
    msg['To'] = empfaenger
    msg['Subject'] = betreff

    msg.attach(MIMEText(nachricht, 'plain'))

    if datei:
        try:
            with open(datei, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={datei}')
                msg.attach(part)
        except FileNotFoundError:
            print(f"Error: The file '{datei}' was not found.")
            return
        except Exception as e:
            print(f"Error while attaching the file: {e}")
            return

    try:
        server = smtplib.SMTP(Email_SMTP, 587)
        server.starttls()  
        server.login(Email_User, password)  
        server.send_message(msg)  
        server.quit()
        answers.update({variable: "E-Mail was sent!"})
    except Exception as e:
        answers.update({variable: f"Error while sending E-Mail: {e}"})

           

def Goto(com):
    global x  
    x = int(com)
    if insub:
        while x <= len(subs[insub]):
            line = subs[insub][x - 1]
            while line[:3].lower() == "got":
                x = int(line[4:])
                line = str(subs[insub][x - 1])
            Commands(line)
            x += 1
    else:       
        while x <= len(file_content):
            line = file_content[x - 1]
            while line[:3].lower() == "got":
                x = int(line[4:])
                line = file_content[x - 1]
            Commands(line)
            x += 1
    Break()

def SUB(com):
     global insub
     insub = True
     global sub
     sub = com.lower()

     if sub not in current_indices:
         current_indices[sub] = 0

     if sub not in subs:
         Log("Sub " + sub + " is not available")
     else:
         subx = current_indices[sub] 
         while subx < len(subs[sub]):
             #print(subx ,str(subs[sub][subx]))
             Com = str(subs[sub][subx])
             if Com.lower()[:3] == "ifc":
                 WriteLog(subs[sub][subx] + "\n")
                 Com = IFCondition(Decode(str(subs[sub][subx])[4:]))
             while Com[:3].lower() == "got":
                 subx = int(Com[4:])-1
                 Com = str(subs[sub][subx])
                 #print(subx ,str(subs[sub][subx]))
                 #continue
             if Com.lower() != "nxt":
                 Commands(Com)
             subx += 1

         if subx >= len(subs[sub]):
             current_indices[sub] = 0  
         else:
             current_indices[sub] = subx  

     insub = None



def ThreadCommand(com):
    thread = threading.Thread(target=Commands, args=(com,))
    thread.start()

            
def SQLInstances(com):
    try:
        var,ver,instuser,instpassword=com.split(Seperator1)
        if instpassword[:3]=="ASS":
            instpassword=instpassword[3:].encode()
            instpassword=str(fernet.decrypt(instpassword)).split("'")[1]
        instances = []
        try:
            reg_path = r"SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL"    
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(winreg.QueryInfoKey(key)[1]):
                    instance_name, instance_id, _ = winreg.EnumValue(key, i)
                    instances.append((instance_name, instance_id))
            if not instances:
                answers.update({var:"none"})
                return
        except:
            answers.update({var:"none"})
            return       

        for instance_name, instance_id in instances:
            
            reg_path = fr"SOFTWARE\Microsoft\Microsoft SQL Server\{instance_id}\MSSQLServer\CurrentVersion"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                version, _ = winreg.QueryValueEx(key, "CurrentVersion")
            version = version[0:2]
            if version==ver:
                try:
                    connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\\{instance_name};UID=sa;PWD={instpassword}"
                    connection = pyodbc.connect(connection_string)
                    cursor=connection.cursor()
                    cursor.execute("SELECT IS_SRVROLEMEMBER('sysadmin')")
                    result=cursor.fetchone()
                    if result[0]==1:
                        answers.update({var:instance_name+" "+instpassword})
                    else:
                        answers.update({var:instance_name+" no"})
                except:
                    
                    try:
                        connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\\{instance_name};Trusted_Connection=yes"
                        connection = pyodbc.connect(connection_string)
                        cursor=connection.cursor()
                        cursor.execute("SELECT IS_SRVROLEMEMBER('sysadmin')")
                        result=cursor.fetchone()
                        
                        if result[0]==1:
                            answers.update({var:instance_name+" trusted"})
                        else:
                          answers.update({var:instance_name+" no"}) 
                    except:
                        
                        answers.update({var:instance_name+" no"})
                        
            else:
                answers.update({var:instance_name+" not"})
    except:
        answers.update({var:"none"})


def create_window(name, title, width, height):
    if name in _windows:
        return
    window = tk.Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    _windows[name] = window

def add_label(name, text, x, y):
    window = _windows.get(name)
    if window:
        label = tk.Label(window, text=text)
        label.place(x=x, y=y)
    else:
        pass

def add_button(windowname, text, command=None, x=10, y=40):
    window = _windows.get(windowname)
    if window:
        button = tk.Button(window, text=text, command=lambda: Commands(command))
        button.place(x=x, y=y)
    else:
        pass

def add_entry(windowname,name,text, x=10, y=70, width=20):
    window = _windows.get(windowname)
    if window:
        entry = tk.Entry(window, width=width)
        entry.insert(0,text)
        entry.place(x=x, y=y)
        _entries[name] = entry
        answers.update({name:text})
    else:
        pass
    
def add_password(windowname, name, text, x=10, y=70, width=20):
    window = _windows.get(windowname)
    if window:
        entry = tk.Entry(window, width=width, show='*')
        entry.insert(0, text)
        entry.place(x=x, y=y)
        _entries[name] = entry
        answers.update({name: text})
    else:
        pass
    
def add_combobox(windowname,name, values, x=10, y=180, width=20):
    window = _windows.get(windowname)
    if window:
        combobox = ttk.Combobox(window, values=values, width=width)
        combobox.place(x=x, y=y)
        _entries[name] = combobox
    else:
        pass

def add_listbox(windowname, name, items, x=10, y=100, width=20, height=5):
    window = _windows.get(windowname)
    if window:
        listbox = tk.Listbox(window, width=width, height=height,selectmode=tk.SINGLE)
        for item in items:
            listbox.insert(tk.END, item)
        listbox.place(x=x, y=y)
        _entries[name] = listbox
    else:
        pass

def add_checkbox_list(windowname, name, text, x, y):
    namevalue=Decode(name).lower()
    window = _windows.get(windowname)
    if window:
        frame = tk.Frame(window)
        frame.place(x=x, y=y)
        var = tk.BooleanVar(value=(namevalue == "true"))
        checkbox = tk.Checkbutton(frame, text=text, variable=var)
        checkbox.pack(anchor='w')
        
        _entries[name] = var

    else:
        pass

def get_entries():
    for row in _entries:
        entry=_entries.get(row)
        if "PY_VAR" in str(entry):
            answers[row] = str(entry.get())
        else:
            try:
                answers.update({row:entry.get()})
            except:
                selected=entry.curselection()
                answers.update({row:entry.get(selected)})

def set_entries():
    for row in _entries:
        if type(_entries[row])==tk.Entry:
            _entries[row].delete(0,tk.END)
            _entries[row].insert(0,answers.get(row))
        
def start(name):
    window = _windows.get(name)
    if window:
        window.focus_force()
        window.mainloop()
    else:
        pass
def end(name):
    window = _windows.get(name)
    
    if window:
        window.withdraw()
    else:
        pass

def Window(com):
    old=com.split(Seperator1)
    Object=com.split(Seperator2)[0].lower()
    com=com.split(Seperator2)[1:]
    if Object=="window":
        create_window(com[0].strip(),Decode(com[1].strip()),int(com[2].strip()),int(com[3].strip()))
    if old[0].lower()=="start":
        start(old[1].strip())
    if old[0].lower()=="end":
        end(old[1].strip())
    if Object=="label":
        add_label(com[0].strip(),Decode(com[1].strip()),int(com[2].strip()),int(com[3].strip()))
    if Object=="button":
        add_button(com[0].strip(),com[1].strip(),com[2].strip(),int(com[3].strip()),int(com[4].strip()))
    if Object=="entry":
        add_entry(com[0].strip(),com[1].strip(),com[2].strip(),int(com[3].strip()),int(com[4].strip()),int(com[5].strip()))
    if Object=="password":
        add_password(com[0].strip(),com[1].strip(),com[2].strip(),int(com[3].strip()),int(com[4].strip()),int(com[5].strip()))
    if Object=="combobox":
        Seperator=com[3]
        add_combobox(com[0].strip(),com[1].strip(),Decode(com[2]).strip().split(Seperator),int(com[4].strip()),int(com[5].strip()),int(com[6].strip()))
    if Object=="listbox":
        Seperator=com[3]
        add_listbox(com[0].strip(),com[1].strip(),Decode(com[2]).strip().split(Seperator),int(com[4].strip()),int(com[5].strip()),int(com[6].strip()),int(com[7].strip()))
    if Object=="checkbox":
        add_checkbox_list(com[0].strip(),com[1].strip(),Decode(com[2]).strip(),int(com[3].strip()),int(com[4].strip()))
    if Object=="getcontent":
        get_entries()
    if Object=="setcontent":
        set_entries()

def KeyInputWait(com):
    variable=com.split(Seperator1)[0]
    ende=com.split(Seperator1)[1]
    global eingaben
    eingaben = ""

    def on_key_event(event):
        global eingaben
        if event.name == ende:
            return
        else:
            if len(event.name)==1:
                eingaben=eingaben+event.name
            if event.name=="space":
                eingaben=eingaben+" "
            if event.name=="backspace":
                eingaben=eingaben[:-1]
            if event.name=="enter":
                eingaben=eingaben+"\n"
            if event.name=="tab":
                eingaben=eingaben+"\t"
                
    keyboard.on_press(on_key_event)
    keyboard.wait(ende)
    keyboard.unhook_all()
    answers.update({variable:eingaben})
    eingaben = ""

def WriteLog(com):
    global LOG
    if LOG==1:
        with open("Achoo.log","a") as f:
            f.write(com)

def EXE(com):
    for row in str(com).split("++"):
        Commands(row)
    return


def Help(com):

    def show_help(command=None, subcommand=None):
        if command is None:
            print("Available Commands:")
            print("=" * 40)
            for cmd, details in commands.items():
                print(f"{cmd}: {details['description']}")
            print("=" * 40)
            print("Use 'help <command>' to get detailed information about a specific command.\n")

            print("Note:")
            print("=====")
            print("If SSL files are present in the current folder, they will be executed with the following priority:")
            print("1. Default.SSL")
            print("2. The only SSL file in the folder")
            print("3. If multiple SSL files exist, you must select one (unless Default.SSL is present).\n")
            print("If you want to add/change your email connection or the settings, just use the keyword 'Setup'")
            print()

            print("About:")
            print("=====")
            print("Programmer: RAT924")


        elif command in commands:
            details = commands[command]
            print(f"Command: {command}")
            print(f"Description: {details['description']}")
            print(f"Usage: {details['usage']}")
            if 'example' in details:
                print(f"Example: {details['example']}")
            
            if 'options' in details:
                print("\nAvailable subcommands (objects):")
                for subcmd, subdetails in details['options'].items():
                    print(f"{subcmd}: {subdetails['description']}")
                
                if subcommand and subcommand in details['options']:
                    subdetails = details['options'][subcommand]
                    print(f"\nSubcommand: {subcommand}")
                    print(f"Description: {subdetails['description']}")
                    print(f"Usage: {subdetails['usage']}")
                    if 'example' in subdetails:
                        print(f"Example: {subdetails['example']}")
        else:
            print(f"Command '{command}' not found. Use 'hlp' to see available commands.\n")

    commands = {
    "ADD": {
        "description": "The ADD function allows you to execute functions from an external library. If the function returns a value, it will be stored in the specified variable.",
        "usage": "ADD VARIABLE|LIBRARY|FUNCTION|PARAMETER",
        "example": "ADD NONE|PRINT|PRINT|HALLO"
    },
    "ANY": {
        "description": "Waits for the user to press any key before continuing.",
        "usage": "ANYKEY",
        "example": "ANYKEY"
    },
    "AUT": {
        "description": "Checks if the script is running with administrator rights. If not, prompts the user to gain admin rights.",
        "usage": "AUTH",
        "example": "AUTH"
    },
    "BRK": {
        "description": "Terminates the execution of the script.",
        "usage": "BRK",
        "example": "BRK"
    },
    "CAL": {
        "description": "Performs arithmetic calculations using variables and numbers.",
        "usage": "CAL Variable|Operator|Variable/Number",
        "example": "CAL Number|+|1"
    },
    "CLS": {
        "description": "Clears the command line window, removing all displayed text.",
        "usage": "CLS",
        "example": "CLS"
    },
    "CMD": {
        "description": "Executes a command in the command line interface (similar to CMD).",
        "usage": "CMD Command",
        "example": "CMD shutdown -s -t 00"
    },
    "CRF": {
        "description": "Creates a new folder at the specified path. If the folder already exists, no action is taken.",
        "usage": "CRF Folder",
        "example": "CRF C:\\Program Files\\SupplyPoint\\Temp"
    },
    "CRY": {
        "description": "Formats the provided string as a password for the Achoo system, ensuring it meets usability standards.",
        "usage": "CRY Variable|Password",
        "example": "CRY Pass|ThisIsMyNewPassword"
    },
    "ENV": {
        "description": "Updates the answers dictionary with the current environment variables.",
        "usage": "ENV",
        "example": "ENV"
    },
    "DAT": {
        "description": "Sets the current date in a specified variable. Use 'e' for English or 'g' for German.",
        "usage": "DAT Variable|e/g",
        "example": "DAT Date|e"
    },
    "DBQ": {
        "description": "Executes a database query and stores the result in a variable.",
        "usage": "DBQ Variable|Server|Database|User|Password|Query",
        "example": "DBQ Items|.\\SQLEXPRESS|Database|sa|password|SELECT * FROM items"
    },
    "DNL": {
        "description": "Downloads a file from the specified URL and saves it to the designated location.",
        "usage": "DNL Destination|Source",
        "example": "DNL Example.pdf|https://example.com/file.pdf"
    },
    "FID": {
        "description": "Displays a file dialog for the user to select a file, storing the selected file path in a variable.",
        "usage": "FID Variable|FileExtension|WindowName",
        "example": "FID UpdateFile|cab|Choose the update file"
    },
    "FIE": {
        "description": "Checks if a specified file exists and stores 'true' in a variable if it does, or 'false' if it does not.",
        "usage": "FIE Variable|File",
        "example": "FIE found|C:\\Temp\\Test.txt"
    },
    "FIL": {
        "description": "Performs file management operations such as copy, move, delete, and execute.",
        "usage": "FILEM action|source|destination",
        "options": {
            "copy": {
                "description": "Copies a file from source to destination.",
                "usage": "FILEM copy|source_path|destination_path"
            },
            "move": {
                "description": "Moves a file from source to destination.",
                "usage": "FILEM move|source_path|destination_path"
            },
            "delete": {
                "description": "Deletes a specified file.",
                "usage": "FILEM delete|file_path"
            },
            "execute": {
                "description": "Executes a specified file.",
                "usage": "FILEM execute|file_path"
            }
        },
        "example": "FILEM copy|source.txt|destination.txt"
    },
    "FOD": {
        "description": "Displays a folder dialog for the user to select a folder, storing the selected path in a specified variable.",
        "usage": "FOD Variable|WindowName",
        "example": "FOD InstallationFolder|Choose the installation folder"
    },
    "FOE": {
        "description": "Checks if a specified folder exists and stores 'true' in a variable if it does, or 'false' if it does not.",
        "usage": "FOE Variable|Path",
        "example": "FOE found|C:\\Temp"
    },
    "FOR": {
        "description": "Creates a FOR-LOOP that iterates a specified number of times, defined by the starting value, ending value, and step size. The loop concludes with the keyword NXT.",
        "usage": "FOR Variable|Beginning|End|Step ... NXT",
        "options": {
            "NXT": {
                "description": "Indicates the end of the FOR-LOOP. The program returns to the beginning of the loop for the next iteration until the end condition is met.",
                "usage": "Used to signify the conclusion of the loop block."
            }
        },
        "example": "FOR X|0|10|2 ... NXT",
        "explanation": "In this example, the loop starts with X at 0, increments X by 2 each iteration, and continues until X reaches 10. The loop body executes for each value of X."
    },
    "GET": {
        "description": "Executes a command similar to CMD and stores the output in a specified variable.",
        "usage": "GET Variable|CMD Command",
        "example": "GET content|type Datei.txt"
    },
    "GOT": {
        "description": "Jumps to a specific line number in the current script.",
        "usage": "GOT LineNumber",
        "example": "GOT 1"
    },
    "HLP": {
        "description": "Displays help information for the available commands.",
        "usage": "HLP",
        "example": "HLP"
    },
    "IFC": {
        "description": "Executes a command if the specified IF condition is true (supported operators: =, >, >=, <, <=).",
        "usage": "IFC Variable1|Operator|Variable2|Then-command|Else-command",
        "example": "IFC Folder|=|C:\\Program Files|LOG=Match|LOG=No match"
    },
    "INP": {
        "description": "Prompts the user to enter a string, which is then stored in a specified variable.",
        "usage": "INP Variable|PromptText",
        "example": "INP Username|Enter your name:"
    },
    "KIW": {
        "description": "Creates a variable that captures the key input as its content.",
        "usage": "KIW Variable|ExitKey",
        "example": "KIW input|enter"
    },
    "KOW": {
        "description": "Simulates keyboard input, but with delay",
        "usage": "KOW Text|Delay",
        "example": "KOW This is a Test|0.1"
    },
    "KYI": {
        "description": "Assigns a command to be executed when a specified key is pressed.",
        "usage": "KYI Key|Command",
        "example": "KYI f2|CMD Explorer.exe"
    },
    "KYO": {
        "description": "Simulates keyboard input, with special keys indicated using .Key and combinations using +.",
        "usage": "KYO Text/Key.(special key)",
        "example": "KYO Key.cmd+e"
    },
    "LEN": {
        "description": "Sets a variable to the length of a specified string or list.",
        "usage": "LEN Variable|String/List|ListSeparator",
        "example": "LEN Length|Hello,this,is,a,list|,"
    },
    "LOA": {
        "description": "Loads data from a specified file into the answers dictionary.",
        "usage": "LOAD file_path",
        "options": {
            "file_path": {
                "description": "The path to the file from which data will be loaded.",
                "usage": "LOAD data.pkl"
            }
        },
        "example": "LOAD data.pkl"
    },
    "LOC": {
        "description": "Sets the cursor coordinates in the command line window.",
        "usage": "LOC x|y",
        "example": "LOC 10|20"
    },
    "LOG": {
        "description": "Adds a new line of text to the LOG window.",
        "usage": "LOG Text",
        "example": "LOG Files copied to %InstallationFolder%"
    },
    "MEN": {
        "description": "Creates a menu or button dialog with specified options.",
        "usage": "MEN Title||Text1||CMD1||Text2||CMD2…",
        "example": "MEN Choose||Local||SPSSetupscript.exe Local.ssl||Online||SPSSetupscript.exe Online.ssl"
    },
    "MOU": {
        "description": "Simulates mouse input at specified coordinates or simulates a mouse click (right or left).",
        "usage": "MOU x|y or MOU r/l (for right/left click)",
        "example": "MOU 100|100 or MOU r"
    },
    "QUE": {
        "description": "Displays a Yes/No dialog and sets the specified variable to true or false based on the user's response.",
        "usage": "QUE Variable|Question",
        "example": "QUE answer|Did you install .NET Framework?"
    },
    "QUT": {
        "description": "Ends the program after the user clicks OK on the dialog.",
        "usage": "QUT Text",
        "example": "QUT Installation finished."
    },
    "REF": {
        "description": "Reads a specified line from a file and optionally replaces a string within that line.",
        "usage": "REF Variable|File|Line|From|To|Replace|With",
        "example": "REF Mac|Macs.txt|4|1|17|(|-)"
    },
    "REM": {
        "description": "Disables a command without deleting it, allowing for future use.",
        "usage": "REM Command or Note",
        "example": "REM This is a comment"
    },
    "REQ": {
        "description": "Checks if the current version of Achoo is greater than or equal to the specified required version.",
        "usage": "REQ VER",
        "example": "REQ 0.23"
    },
    "RJS": {
        "description": "Reads a variable from a specified JSON file.",
        "usage": "RJS Variable|JSON-File|Path",
        "example": "RJS found|appsettings.json|DeviceSettings/ID"
    },
    "RND": {
        "description": "Sets a variable to a random number within a specified range.",
        "usage": "RND Variable|From|To",
        "example": "RND Dice|1|6"
    },
    "RSF": {
        "description": "Replaces a specified string with another in a file.",
        "usage": "RSF File|Old Content|New Content",
        "example": "RSF Document.txt|Hello|Hi"
    },
    "RSV": {
        "description": "Replaces a specified string with another in a variable.",
        "usage": "RSV Variable|Old Content|New Content",
        "example": "RSV Text|Hello|Hi"
    },
    "RXM": {
        "description": "Reads a variable from a specified XML file.",
        "usage": "RXM Variable|XML file|Path",
        "example": "RXM found|SPSConfig.xml|Config/Database/SQLServerName"
    },
    "SAV": {
        "description": "Saves the current answers dictionary to a specified file.",
        "usage": "SAVE file_path",
        "options": {
            "file_path": {
                "description": "The path to the file where data will be saved.",
                "usage": "SAVE data.pkl"
            }
        },
        "example": "SAVE data.pkl"
    },

    "SCH": {
        "description": "Starts or stops a scheduled task that executes a specified function at regular intervals.",
        "usage": "SCHED start|function|interval OR SCHED stop",
        "options": {
            "start": {
                "description": "Starts the scheduler with the specified function and interval.",
                "usage": "SCHED start|function_name|interval_in_seconds"
            },
            "stop": {
                "description": "Stops the currently running scheduler.",
                "usage": "SCHED stop"
            }
        },
        "example": "SCHED start|my_function|5"
    },
    "SET": {
        "description": "Assigns a specified value or string to a variable.",
        "usage": "SET Variable|Value/String",
        "example": "SET Count|20"
    },
    "SEA": {
        "description": "Searches for a file or folder and stores the selected path in a specified variable.",
        "usage": "SEA Variable|File/Folder|Filename/Path|Destination|Text",
        "example": "SEA File|File|SPSConfig.xml|C:\\|Choose the correct folder"
    },
    "SLP": {
        "description": "Pauses the execution for a specified number of seconds.",
        "usage": "SLP Seconds",
        "example": "SLP 1"
    },
    "SND": {
        "description": "Sends an email to the specified recipient with an optional attachment.",
        "usage": "SND Variable|Receiver|Subject|Message|Optional:File",
        "example": "SND var|Example@Example.com|Hi|Hi There! or SND var|Example@Example.com|Hi|Hi|File"
    },
    "SPL": {
        "description": "Splits a variable by a specified string and writes the resulting index into another variable.",
        "usage": "SPL New|Old|Separator|Index",
        "example": "SPL Part|Text|-|2"
    },
    "SQI": {
        "description": "Checks if a specific version of SQL Server is installed locally and verifies the provided login credentials.",
        "usage": "SQI Variable|Version|User|Password",
        "example": "SQI instance|15|sa|Tools4Vend"
    },
    "SST": {
        "description": "Stores the current status of a specified service in a variable.",
        "usage": "SST Variable|Service",
        "example": "SST status|MSSQL$EXP_2019"
    },
    "STR": {
        "description": "Deletes a specified number of characters from the beginning or end of a variable.",
        "usage": "STR Variable|r/l|Number",
        "example": "STR Folder|r|1"
    },
    "SUB": {
        "description": "Executes a subprogram by creating a file with the .sub extension. The filename serves as the name of the subprogram.",
        "usage": "SUB Subname",
        "example": "SUB MySub"
    },
    "TED": {
        "description": "Prompts the user to enter a string, which is then stored in a specified variable.",
        "usage": "TED Variable|PromptText",
        "example": "TED ID|Please enter your ID"
    },
    "THR": {
        "description": "Starts a new thread to execute a specified command in parallel.",
        "usage": "THR Command",
        "example": "THR LOG Test"
    },
    "TIM": {
        "description": "Sets the current time in a specified variable.",
        "usage": "TIM Variable",
        "example": "TIM CurrentTime"
    },
    "TIT": {
        "description": "Sets the title of the command line window.",
        "usage": "TIT Title",
        "example": "TIT My Application"
    },
    "TMR": {
        "description": "Records the elapsed time since the start of the timer and updates the answers dictionary.",
        "usage": "TIMER task_name",
        "options": {
            "task_name": {
                "description": "The name of the task for which the elapsed time is recorded.",
                "usage": "TIMER my_task"
            }
        },
        "example": "TIMER my_task"
    },
    "TON": {
        "description": "Sets a variable to 'true' if a specified task is started, otherwise sets it to 'false'.",
        "usage": "TON Variable|Task",
        "example": "TON answer|Firefox"
    },
    "VER": {
        "description": "Sets the current version number of SSL in a specified variable.",
        "usage": "VER Variable",
        "example": "VER SSLVersion"
    },
    "WHI": {
        "description": "Creates a WHILE-LOOP that continues executing as long as the specified condition is true.",
        "usage": "WHI Condition ... WND",
        "options": {
            "WND": {
                "description": "Returns to the beginning of the loop to re-evaluate the condition.",
                "usage": "Used to indicate the end of the loop block and return to the start for the next iteration."
            },
            "CWI": {
                "description": "Continue While; skips the remaining code in the loop for the current iteration and goes back to re-evaluate the condition.",
                "usage": "CWI ... WND"
            },
            "BWI": {
                "description": "Break While; exits the loop immediately, skipping any remaining iterations.",
                "usage": "BWI"
            }
        },
        "example": "WHI X|<|10 ... WND"
    },
    "WIN": {
        "description": "Creates a graphical user interface (GUI) with various interactive elements.",
        "usage": "WIN Object||Options",
        "options": {
            "BUTTON": {
                "description": "Creates a button in an existing window.",
                "usage": "BUTTON||WindowName||Label||Command||X||Y",
                "example": "BUTTON||WIN||OK||WIN GETCONTENT||0||200"
            },
            "CHECKBOX": {
                "description": "Creates a checkbox in an existing window.",
                "usage": "CHECKBOX||WindowName||CheckboxName||Label||X||Y",
                "example": "CHECKBOX||WIN||CHECK1||I am a checkbox||0||150"
            },
            "COMBOBOX": {
                "description": "Creates a combobox in an existing window.",
                "usage": "COMBOBOX||WindowName||ComboBoxName||Content1|Content2|...||Separator||X||Y||Length",
                "example": "COMBOBOX||WIN||COMBO1||THIS IS A COMBOBOX|| ||100||0||20"
            },
            "END": {
                "description": "Destroys the specified window.",
                "usage": "END||WindowName",
                "example": "END||MainWindow"
            },
            "ENTRY": {
                "description": "Creates an entry field in an existing window.",
                "usage": "ENTRY||WindowName||EntryName||Content||X||Y||Length",
                "example": "ENTRY||WIN||ENTRY1||I am an entry||50||0||20"
            },
            "GETCONTENT": {
                "description": "Retrieves the content of all objects in the window.",
                "usage": "GETCONTENT",
                "example": "GETCONTENT"
            },
            "LABEL": {
                "description": "Creates a label in an existing window.",
                "usage": "LABEL||WindowName||Text||X||Y",
                "example": "LABEL||WIN||This is a label||0||0"
            },
            "LISTBOX": {
                "description": "Creates a listbox in an existing window.",
                "usage": "LISTBOX||WindowName||ListBoxName||Content1|Content2|...||Separator||X||Y||Length||Width||Height",
                "example": "LISTBOX||WIN||LIST1||THIS IS A LISTBOX|| ||0|50||125||100||100"
            },
            "PASSWORD": {
                "description": "Creates a password entry field in an existing window, masking input with asterisks.",
                "usage": "PASSWORD||WindowName||EntryName||Content||X||Y||Length",
                "example": "PASSWORD||WIN||ENTRY1||I am a password entry||50||0||20"
            },
            "START": {
                "description": "Opens a defined window if not in console mode.",
                "usage": "START||WindowName",
                "example": "START||WIN"
            },
            "WINDOW": {
                "description": "Creates an empty window with specified dimensions.",
                "usage": "WINDOW||WindowName||Title||X||Y",
                "example": "WINDOW||WIN||EXAMPLEWINDOW||640||480"
            }
        }
    },
    "WJS": {
        "description": "Updates a specified value in a JSON file.",
        "usage": "WJS File|Path|Value",
        "example": "WJS AppSettings.json|DeviceSettings/ID|1"
    },
    "WRF": {
        "description": "Creates a file with specified content, overwriting if it already exists.",
        "usage": "WRF File|Content",
        "example": "WRF Log.txt|Installing..."
    },
    "WRL": {
        "description": "Rewrites a specific line in a file.",
        "usage": "WRL File|LineNumber|Content",
        "example": "WRL SPSConfig.xml|27|<SQLDebug>1</SQLDebug>"
    },
    "WXM": {
        "description": "Updates a specified value in an XML file.",
        "usage": "WXM File|Path|Value",
        "example": "WXM SPSConfig.xml|Config/Database/SQLServerName|EXP_2019"
    },
    "ZIP": {
        "description": "Compresses files into a zip archive or decompresses a zip archive.",
        "usage": "ZIP Function",
        "options": {
            "ZIP": {
                "description": "Compresses specified files into a zip archive.",
                "usage": "ZIP Filename|File1|File2|File3 ...",
                "example": "ZIP TEST.ZIP|FILE1.TXT|FILE2.TXT"
            },
            "UNZIP": {
                "description": "Decompresses a specified zip archive.",
                "usage": "UNZIP Filename|Folder",
                "example": "UNZIP TEST.ZIP|FOLDER"
            },
        },
    },
}
    com_parts = com.split(" ")
    
    if len(com_parts) == 1:
        if com_parts[0].upper()=="":
            show_help(None)
        else:
            show_help(com_parts[0].upper())
    elif len(com_parts) == 2:
        show_help(com_parts[0].upper(), com_parts[1].upper())
    else:
        print(f"Command '{com}' not found. Use 'hlp' to see available commands.\n")
    
def Mouse(com):
    mouse = MController()
    if com.lower()=="r":
        mouse.click(Button.right)
    elif com.lower()=="l":
        mouse.click(Button.left)
    else:
        x=int(com.split(Seperator1)[0])
        y=int(com.split(Seperator1)[1])
        mouse.position = (x, y)
        
def Version(com):
    Variable=com
    if com!="":
        answers.update({Variable:ver})
    if com=="":
        Log(ver)
    
def ConsoleInput(com):
    Variable=com.split(Seperator1)[0]
    Text=com.split(Seperator1)[1]
    print(Text)
    Ausgabe=input()
    answers.update({Variable:Ausgabe})
    #WriteLog(Text,Ausgabe)

def Random(com):
    Variable=com.split(Seperator1)[0]
    Von=int(com.split(Seperator1)[1])
    Bis=int(com.split(Seperator1)[2])
    Ausgabe=str(randint(Von,Bis))
    answers.update({Variable:Ausgabe})

def KeyOutput(com):
    keyboard = Controller()
    keys = com.split("+")
    processed_keys = []
    for key in keys:
        if key.startswith("Key."):
            processed_keys.append(getattr(Key, key[4:]))
        else:
            processed_keys.append(key)
    for key in processed_keys:
        if isinstance(key, str):
            keyboard.type(key)
        else:
            keyboard.press(key)
    for key in reversed(processed_keys):
        if not isinstance(key, str):
            keyboard.release(key)
            
def Break():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    exit()

def Keys(event, key, com):
    if event.name == key:
        Commands(com)

def KeyInput(com):
    key = com.split(Seperator1)[0]
    command = Seperator1.join(com.split(Seperator1)[1:])
    keyboard.on_press(lambda event: Keys(event, key, command))

def CLS():
    system("cls")

def Locate(com):
    x=int(com.split(Seperator1)[0])
    y=int(com.split(Seperator1)[1])
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    yx = ctypes.c_ulong((y << 16) | x)
    ctypes.windll.kernel32.SetConsoleCursorPosition(handle, yx)
    
def Sleep(com):
    sleeep(float(com))

def Split(com):
    Variable=com.split(Seperator1)[1]
    NVariable=com.split(Seperator1)[0]
    Splitter=com.split(Seperator1)[2]
    Index=com.split(Seperator1)[3]
    if "." in Index:
        Index=Index[:-2]
    if Splitter!="":
        Ausgabe=str(answers[Variable].split(Splitter)[int(Index)])
    else:
        Ausgabe=str(answers[Variable][int(Index)])
    answers.update({NVariable:Ausgabe})


def ReplaceStringFile(com):
    Datei=com.split(Seperator1)[0]
    oString=com.split(Seperator1)[1]
    nString=com.split(Seperator1)[2]
    Content=[]
    with open(Datei, "r") as f:
        for line in f:
            Content.append(line)
    Content= [item.replace(oString,nString) for item in Content]
    with open(Datei,"w") as f:
        for row in Content:
            f.write(row)

def Title(com):
    top.title(com)    

def WriteJSon(com):
    Datei=com.split(Seperator1)[0]
    Key=com.split(Seperator1)[1]
    Wert=com.split(Seperator1)[2]
    with open(Datei) as f:
        data = load(f)
    keys = Key.split('/')
    temp = data
    for key in keys[:-1]:
        temp = temp[key]
    temp[keys[-1]] = Wert
    with open(Datei, 'w') as f:
        dump(data, f)

def ReadJSon(com):
    Variable=com.split(Seperator1)[0]
    Datei=com.split(Seperator1)[1]
    Key=com.split(Seperator1)[2]
    with open(Datei) as f:
        data = load(f)
    try:
        Ausgabe = eval("data" + "['" + Key.replace("/", "']['") + "']")
    except:
        Ausgabe=''
    answers.update({Variable:str(Ausgabe)})

def WriteXML(com):
    Datei=com.split(Seperator1)[0]
    Key=com.split(Seperator1)[1]
    Wert=com.split(Seperator1)[2]
    tree = ET.parse(Datei)
    root = tree.getroot()
    type_element = root.find(Key)
    type_element.text = Wert
    tree.write(Datei)

def ReadXML(com):
    Variable=com.split(Seperator1)[0]
    Datei=com.split(Seperator1)[1]
    Key=com.split(Seperator1)[2]
    tree = ET.parse(Datei)
    root = tree.getroot()
    Ausgabe = root.find(Key).text
    answers.update({Variable:Ausgabe})

def Download(com):
    Ziel=com.split(Seperator1)[0]
    Quelle=com.split(Seperator1)[1]
    try:
        urlretrieve(Quelle, Ziel)
    except:
        Log("File not found")

def TaskOnline(com):
    Variable=com.split(Seperator1)[0]
    Task=com.split(Seperator1)[1]
    tasklist=str(check_output(['tasklist']))
    if Task in tasklist:
        Ausgabe="true"
    else:
        Ausgabe="false"
    answers.update({Variable:Ausgabe})

def ServiceStatus(com):
    Variable=com.split(Seperator1)[0]
    Service=com.split(Seperator1)[1]
    try:
        output = str(check_output(['sc', 'query', Service]))
        Ausgabe= str(output.split("\\r\\n")[3]).split(" ")[25]
    except:
        Ausgabe="NOTFOUND"
    answers.update({Variable:Ausgabe})

def FileExists(com):
    Variable=com.split(Seperator1)[0]
    Folder=com.split(Seperator1)[1]
    if path.exists(Folder):
        Ausgabe="true"
    else:
        Ausgabe="false"
    answers.update({Variable:Ausgabe})

def FolderExists(com):
    Variable=com.split(Seperator1)[0]
    Folder=com.split(Seperator1)[1]
    if path.exists(Folder):
        Ausgabe="true"
    else:
        Ausgabe="false"
    answers.update({Variable:Ausgabe})

def Time(com):
    Variable=com
    Ausgabe=str(ctime()[11:19])
    answers.update({Variable:Ausgabe})

def Date(com):
    Variable=com.split(Seperator1)[0]
    Config=com.split(Seperator1)[1]
    if Config.lower()=="e":
        Ausgabe=str(datetime.date.today())
    if Config.lower()=="g":
        Tmp=str(datetime.date.today())
        Ausgabe=Tmp[8:10]+"."+Tmp[5:7]+"."+Tmp[0:4]        
    answers.update({Variable:Ausgabe})

def Calculate(com):
    w=0
    Wert=0
    Variable=com.split(Seperator1)[0]
    Wert=float(answers[com.split(Seperator1)[0]])
    Operator=com.split(Seperator1)[1]
    Number=float(com.split(Seperator1)[2])
    if Operator=="*":
        Ausgabe=Wert*Number
    if Operator=="/":
        Ausgabe=float(Wert/Number)
    if Operator=="+":
        Ausgabe=Wert+Number
    if Operator=="-":
        Ausgabe=Wert-Number
    answers.update({Variable:str(Ausgabe)})  

def ReplaceStringVariable(com):
    Content=answers[com.split(Seperator1)[0]]
    String=com.split(Seperator1)[1]
    if String=="Seperator1":
        String=Seperator1
    if String=="Seperator2":
        String=Seperator2        
    RepString=com.split(Seperator1)[2]
    if RepString=="Seperator1":
        RepString=Seperator1
    if RepString=="Seperator2":
        RepString=Seperator2     
    
    answer=Content.replace(String,RepString)
    answers.update({Var:answer})
    
def Strip(com):
    Variable=com.split(Seperator1)[0]
    Pos=com.split(Seperator1)[1].lower()
    Len=int(com.split(Seperator1)[2])
    Te=str(answers[Variable])
    Var=answers[Variable]
    if Pos=="r":
        Var=Var[:-Len]
        answers.update({Variable:Var})
    if Pos=="l":
        Var=Var[Len:]
        answers.update({Variable:Var})

def WriteLine(com):
    z=1
    Datei=com.split(Seperator1)[0]
    Zeile=int(float(com.split(Seperator1)[1]))
    Content=com.split(Seperator1)[2]
    TEMP=[]
    rel=open(Datei,"r")
    for lines in rel:
        TEMP.append(lines)
    rel.close()
    
    wrl=open(Datei,"w")
    for item in TEMP:
        if z==Zeile:
            wrl.write(Content+"\n")
        if z!=Zeile:
            wrl.write(item)
        z=z+1

    if z==Zeile:
        wrl.write(Content+"\n")
        
    if z<Zeile:
        while z<Zeile:
            wrl.write("\n")
            z=z+1
        wrl.write(Content)
    wrl.close()

def GetLine(com):
    Variable=com.split(Seperator1)[0]
    Datei=com.split(Seperator1)[1]
    Content=com.split(Seperator1)[2].lower()
    gel=open(Datei,"r")
    z=1
    for lines in gel:
        if Content in str(lines).lower():
            answers.update({Variable:str(z)})
        z=z+1
    gel.close()

def Auswahl(event):
    Listewahl=str(Lis.get(Lis.curselection()))
    answers.update({Variable:Listewahl})
    Lis.destroy()
    List.destroy()
    
def Search(com):
    global Variable
    Found=[]
    Variable=com.split(Seperator1)[0]
    Option=com.split(Seperator1)[1].lower()
    Value=com.split(Seperator1)[2].lower()
    Destination=com.split(Seperator1)[3]
    Text=com.split(Seperator1)[4]
    if Option=="folder" or Option=="file":
        for root, dirs, files in walk(Destination):
            ro=str(root).replace("/",chr(92))
            tmp=ro.split(chr(92))
            le=len(root.split(chr(92)))
            if Option=="folder" and Value == str(tmp[le]).lower():
                Found.append(str(root).replace("/",chr(92)))
            for file in files:
                if Option=="file" and Value==file.lower():
                    Found.append(root+"/"+file)
    if len(Found)>1:
        global List
        global Lis
        List= tk.Tk()
        List.title(Text)
        List.geometry("800x600")
        Lis=Listbox(List, height=35, width=150)
        for item in Found:
            Lis.insert(tk.END,item)
        Lis.pack()
        List.lift()
        List.attributes('-topmost', True)
        Lis.bind('<<ListboxSelect>>', lambda event:Auswahl(event))
        List.wait_window(List)
    if len(Found)==0:    
        Commands("LOG File "+Value+" not found!")
    if len(Found)==1:
        answers.update({Variable:Found[0]})
             
def Question(com):
    answer=str(messagebox.askyesno("Please answer",com.split(Seperator1)[1])).lower()
    answers.update({com.split(Seperator1)[0]:answer})
    
def Readfile(com):
    ref=com.split(Seperator1)
    Variable=ref[0]
    tmp=open(ref[1],"r",encoding="utf-8")
    l=int(float(ref[2]))
    s=""
    r=""
    f=int(ref[3])-1
    e=int(ref[4])-1
    if len(ref)>5:
        s=ref[5]
        r=ref[6]
    i=1
    for line in tmp:
        if i==l:
            answer=str(line)[f:e].replace(s,r).rstrip()
            answers.update({Variable:answer})
            break
        i=i+1
    tmp.close()
    
def Set(com):
    temp=com.split(Seperator1)
    Output=""
    x=0
    Variable=temp[0]
    Output=com[len(Variable)+1:]
    answers.update({Variable:Output})

def Decode(String):
    segments = String.split(Variable_Marker)
    result = ""

    for segment in segments:
        if segment in answers:
            result += answers[segment]
        else:
            result += segment 
    try:
        result=answers[result]
    except:
        pass
    return result

def Clicked(com):
    window.withdraw()
    window.destroy()
    Commands(com)

def Menu(com):
    global window
    window = tk.Tk()
    window.focus_force()
    window.title(com.split(Seperator1)[0])
    window.width = 800
    window.height = 600
    window.attributes('-topmost', True)
    for i in range(1,len(com.split(Seperator2)),2):
        b=tk.Button(window,width=80,height=int(40/(int(len(com.split(Seperator2))/2))),text=com.split(Seperator2)[i],command=lambda i=i:Clicked(com.split(Seperator2)[i+1]))
        b.pack()
        b.place()
    window.lift()
    window.update()
    window.wait_window(window)

def Qut(com):
    global ENDE
    if ENDE==0:
        messagebox.showinfo("Info",com)
    ENDE=1
    raise SystemExit

def Get(com):
    Variable=com.split(Seperator1)[0]
    Coms=com.split(Seperator1)[1]
    try:
        answer=str(check_output(Coms, shell=True).decode()).replace("\n","").replace("\r","")
    except:
        answer=str(check_output(Coms, shell=True).decode('cp1252')).replace("\n","").replace("\r","")
    answers.update({Variable:answer})
    
def FolderDialog(com):
    Variable=com.split(Seperator1)[0]
    Title=com.split(Seperator1)[1]
    answer=filedialog.askdirectory(title=Title).replace("/",chr(92))+chr(92)
    if answer==chr(92):
        top.destroy()
    answers.update({Variable:answer}) 

def FileDialog(com):
    Variable=com.split(Seperator1)[0]
    Title=com.split(Seperator1)[2]
    Ending=com.split(Seperator1)[1]
    answer=filedialog.askopenfilename(title=Title,filetypes=((Ending+" files","*."+Ending),("all files","*.*"))).replace("/",chr(92))
    if answer=="":
        top.destroy()
    answers.update({Variable:answer})

def TextDialog(com):
    Variable=com.split(Seperator1)[0]
    Title=com.split(Seperator1)[1]
    answer=simpledialog.askstring("Please enter",Title)
    answers.update({Variable:answer})
    
def Log(com):
    WriteLog(com+"\n")
    print(com)

def CMD(com):
    system(com)

def WriteFile(com):
    with open(com.split(Seperator1)[0].replace(chr(92)+chr(92),chr(92)),"w") as file:
        file.write(com.split(Seperator1)[1].replace(chr(92)+"n","\n")+"\n")

def IFCondition(com):
    operator = com.split(Seperator2)[1]
    value1 = com.split(Seperator2)[0]
    value2 = com.split(Seperator2)[2]
    if operator == "=":
        if value1 == value2:
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator == ">":
        if float(value1) > float(value2):
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator == ">=":
        if float(value1) >= float(value2):
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator == "<=":
        if float(value1) <= float(value2):
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator == "<":
        if float(value1) < float(value2):
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator == "!=":
        if value1 != value2:
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator.lower() == "in":
        if value1 in value2:
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    elif operator.lower() == "not in":
        if value1 not in value2:
            return com.split(Seperator2)[3]
        else:
            return com.split(Seperator2)[4]
    else:
        if com.split(Seperator2)[0] == com.split(Seperator2)[1]:
            return com.split(Seperator2)[2]
        else:
            return com.split(Seperator2)[3]       
            
def CreateFolder(com):
    if path.exists(com)==False:
        makedirs(com)

files=[]
for file_name in listdir():
    if fnmatch(file_name,"*.ssl"):
        files.append(file_name)
if(path.isfile("default.ssl"))==True:
    files=[]
    files.append("Default.ssl")
try:
    if len(argv)>1:
        files=[]
        if "cmd" in str(argv).lower():
            Ende=0
            while Ende==0:
                try:
                    line=input(">")
                    Commands(line)
                except Exception as e:
                    if EXC==1:
                        WriteLog(str(e)+"\n")
                        print(e)
                    else:
                        continue
        if "cmd" not in argv[1].lower():
            files.append(argv[1])
    Log("Searching for Scriptfiles ...")

    if len(files)==0:
        Log("No file was found in the directory")
        Log("Starting into command line")

        Ende=0
        while Ende==0:
            try:
                line=input(">")
                Commands(line)
            except Exception as e:
                if EXC==1:
                    WriteLog(str(e)+"\n")
                    print(e)
                else:
                    continue
        
    if len(files)>1:
        Log("More than one file were found in the directory")
        file=filedialog.askopenfilename(initialdir=getcwd(),title="Select Script file",filetypes=(("SetupScriptFiles","*.ssl"),("all files","*.*")))
        file=file.replace("/",chr(92)).replace(getcwd()+chr(92),"") 
    if len(files)==1:
        file=files[0]
    if file=="":
        Log("No file was selected, starting console ...")
        Ende=0
        while Ende==0:
            try:
                line=input(">")
                Commands(line)
            except Exception as e:
                if EXC==1:
                    WriteLog(str(e)+"\n")
                    print(e)
                else:
                    continue
                
    Log("Execute file: "+file)
    file_read=open(file,"r",encoding="utf-8")
    for line in file_read:
        file_content.append(line.replace("\n",""))
    x=1
    while x <= len(file_content):
        line=file_content[x-1]
        while line[:3].lower()=="got":
            x=int(line[4:])
            line=file_content[x-1]
        Commands(line)
        x=x+1
    Break()

except Exception as e:
    with open("Achoo.log","a") as f:
        WriteLog(str(e)+"\n")
    if EXC==1:
        print(e)
        WriteLog(str(e)+"\n")
    else:
        pass
