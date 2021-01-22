"""
MIT License

Copyright © 2020 Matthew Murphy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import requests
import string
import configparser
import time
import keyboard
import shutil
import subprocess

from bs4 import BeautifulSoup
from zipfile import ZipFile

sven_addons = ""

configpath = '%s\\scmapdb_downloader\\' %  os.environ['APPDATA']
configname = 'scmapdb_downloader.ini'

config = configparser.ConfigParser()


def DownloadMap():
    downloadLink = input("Please type or paste the Sven Co-Op Map Database link for the map you want: ")
    
    #downloadLink = "http://scmapdb.com/map:101-grunts" #testing


    links = []
    stored = "nil"
    try:
        if (downloadLink.find("scmapdb") != -1):
            r = requests.get(downloadLink)
            soup = BeautifulSoup(r.content, features="lxml")
            for i in soup.find_all('a'):
                #print(i.get('href'))
                stored = [str(i.get('href')), ""]
                if stored[0][-4:] == ".zip":
                    links.append(stored)
        else:
            raise UnboundLocalError()
    except UnboundLocalError:
        print ("ERROR: Please enter a valid scmapdb link!")
        DownloadMap()
    except:
        print("ERROR: Map not found, try again!")
        DownloadMap()
    
        
    #try:
        
    num = -1
    print("\n")
    index = 0
    if len(links) > 1:
        for k in links:
            num += 1
            option = "{0}) {1} {2}"
            print(option.format(num, k[1], k[0]))
                
        print("\n")
        index = int(input("Please indicate the file you wish to download from the above list (0, 1, 2, etc): "))
                
    r2 = requests.get(links[index][0], allow_redirects=True)
    open("downloaded.zip", 'wb').write(r2.content)
                
        
            
            #Extract to addons directory
            
    with ZipFile("downloaded.zip", 'r') as zipObj:
        zipObj.extractall("sven_temp")
    os.remove("downloaded.zip")
           
        
    if os.path.exists('sven_temp\svencoop_addon'):
        MoveFiles('sven_temp\svencoop_addon')
    else:
        MoveFiles('sven_temp')
            
    
            
    print("Finished downloading & extracting %s!\n\n" % links[index][0])
    DownloadMap()
        
        
    #except:
        #print("ERROR: Something broke, try again!")
        #DownloadMap()
        
def MoveFiles(path):
    openExplorerOnExcept = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            try:
                thisfile = str(os.path.join(root,name))
                thisfile = thisfile.replace(path, '')
                fullpath = sven_addons + thisfile
                shutil.move(path + thisfile, fullpath)
            except:
                print("\nERROR: unable to move %s from sven_temp folder, you'll have to do it manually." % thisfile)
                print("\nSorry for this bug, I have no clue what causes it and it's not 100% consistent.")
                if openExplorerOnExcept == 0:
                    print("\nOpening temp & addon folders...")
                    openExplorerOnExcept = 1
                    subprocess.Popen('explorer "%s"' % sven_addons)
                    subprocess.Popen('explorer "%s"' % path)
   
def DoCleanup():
    print("TODO")
    
def WriteConfig():
    config['SETTINGS'] = {
        'AddonsFolder': sven_addons
    }
    with open(configpath + configname, 'w') as configfile:
        config.write(configfile)
    
def ReadConfig():
    
    #Gotta globalize
    global sven_addons
    
    #Because "False" == True
    stringToBool = {
        "True": True,
        "False": False
    }
    
    config.read(configpath + configname)
    settings = config['SETTINGS']
    sven_addons = settings['AddonsFolder']
    
def DoConfig():
    #Gotta globalize
    global sven_addons

    sven_addons = input("Where is your Sven Co-Op addons folder located? Please paste the entire path: ")
    #Create the appdata directory to store the config file in
    if not os.path.exists(configpath):
        os.makedirs(configpath)
    WriteConfig()


def InitializeDownloader():
    #Check to see if we've already got a config file. If not, set one up.
    if not os.path.exists(configpath + configname):
        try:
            DoConfig()
        except OSError:
            #TODO Run basic mode if DoConfig fails for any reason.
            global sven_addons
            sven_addons = input("Where is your Sven Co-Op addons folder located? Please paste the entire path: ")
    else:
        #Give the user the chance to change their settings before proceeding
        print("Initializing... Press SHIFT now if you want to change your addons folder location.")
        waittime = time.time() + 3
        ReadConfig()
        while time.time() < waittime:
            if keyboard.is_pressed("shift"):
                DoConfig()
                break
    DownloadMap()
    
InitializeDownloader()