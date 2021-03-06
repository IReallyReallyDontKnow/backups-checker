import configparser
import glob
import datetime
import sys
import time
import os.path, time
from datetime import datetime
full_date = False
Time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
def log(DIR,Messeage):
  global Time
  DIR = DIR+Time+".log"
  Log = open(DIR,"a")
  Log.write(Messeage)
  Log.close()
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 
def find_date(File,full_date=False):
    check = True
    File_format = File.split(".")[0]
    try:
      File_format.split("-")[1]
    except:
      check = False
    if (check == True):
      if(full_date == False or full_date == True):
        Year = File_format.split("-")[1]
        Month = File_format.split("-")[2]
        Day = File_format.split("-")[3]
      else:
        print("Check Date in Config!")
      if(full_date == True):
        File_format2 = File.split(".")[0]
        File_format2 = File_format2.split("-")[4]
        Hour = File_format2.split(":")[0]
        Minutes = File_format2.split(":")[1]
        Seconds = File_format2.split(":")[2]
      if(full_date == True):
        Messeage = "Last backup in name ("+File+"): "+Year+"-"+Month+"-"+Day+" "+Hour+":"+Minutes+":"+Seconds+"\n"+"Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File))+"\n"+"Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n"
        print("Last backup in name ("+File+"): "+Year+"-"+Month+"-"+Day+" "+Hour+":"+Minutes+":"+Seconds)
        print("Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File)))
        print("Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n")
      elif(full_date == False):
        Messeage = "Last backup in name ("+File+"): "+Year+"-"+Month+"-"+Day+"\n"+"Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File))+"\n"+"Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n"
        log(Log,Messeage)
        print("Last backup in name ("+File+"): "+Year+"-"+Month+"-"+Day)
        print("Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File)))
        print("Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n")
    elif (check == False):
      Messeage = "Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File))+"\n"+"Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n"
      log(Log,Messeage)
      print("Last modified ("+File+"): %s" % time.ctime(os.path.getmtime(File)))
      print("Created ("+File+"): %s" % time.ctime(os.path.getctime(File))+"\n")
    else:
      print("This error is not defined. Please contact developer!")
def read_config():
    global Log
    progress(25,100,'Reading config')
    time.sleep(0.5)
    ConfigParser = configparser.RawConfigParser()   
    configFilePath = r'config/config'
    ConfigParser.read(configFilePath)
    Log = ConfigParser.get('SETTINGS','Log')
    Format = ConfigParser.get('SETTINGS','Format')
    Date = ConfigParser.get('SETTINGS','Date')
    DIR = ConfigParser.get('SETTINGS','DIR')
    file = ConfigParser.get('SETTINGS','Predeclared_Files')
    set_date(Date)
    file_names = 'NULL'
    if file == 'yes':
        file_names = ConfigParser.get('SETTINGS','File_names')
        last_backup(DIR,file_names,Format,True)
    elif file == 'no':
        last_backup(DIR,file_names,Format)
def set_date(Date):
  progress(50,100,'Parsing date')
  time.sleep(0.5)
  global full_date
  Date_pattern = ["NULL","NULL","NULL","NULL","NULL","NULL"]
  num = 0
  Date = Date.split("-")
  for x in Date:
    if x == 'Y':
      Date_pattern[num] = '%Y'
    elif x == 'm':
      Date_pattern[num] = '%m'
    elif x == 'd':
      Date_pattern[num] = '%d'  
    elif x == 'H':
      full_date = True
      Date_pattern[num] = '%H'
    elif x == 'M':
      full_date = True
      Date_pattern[num] = '%M'   
    elif x == 'S':
      full_date = True
      Date_pattern[num] = '%S'
    num = num+1
def last_backup(DIR,file_names,Format,file=False):
    progress(75,100,'Checking file names')
    time.sleep(0.5)
    if file==True:
        file_names = file_names.split(",")
        Format = Format.split(",")
        progress(99,100,'Finding last backup')
        time.sleep(0.5)
        print(chr(27) + "[2J")
        for x in file_names:
          for y in Format:
             for File in glob.glob(DIR+x+"*"+"."+y): 
              find_date(File,full_date)
    elif file==False:
        progress(99,100,'Finding last backup')
        time.sleep(0.5)
        print(chr(27) + "[2J")
        Format = Format.split(",")
        for y in Format:
          for File in glob.glob(DIR+"*"+"."+y):
              find_date(File,full_date)
if __name__ == '__main__':
    read_config()
