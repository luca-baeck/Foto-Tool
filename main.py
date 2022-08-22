#FotoRename:
#@author: Luca Bäck
#@date: 18.12.21

import shutil
import os
from colorama import Fore
import colorama
colorama.init()
from PIL import Image
from datetime import datetime, timedelta
from pathlib import Path
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from PIL import ImageChops
from tkinter.filedialog import askdirectory
import sys
import calendar
#pip install defusedxml
import filecmp
import json



OriPath = r''
EndPath = r''

FileRenamed = '§'

print(Fore.GREEN + ' *********************************************************')
print(Fore.GREEN + ' Foto Programm:')
print(Fore.GREEN + ' @author: Luca Bäck')
print(Fore.GREEN + ' @date: 21.12.21')
print(Fore.GREEN + ' *********************************************************')

def read_jpg(file):
    print('Read jpg-File...')
    try:

        "returns the image date from image (if available)"
        std_fmt = '%Y:%m:%d %H:%M:%S'
        # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
        tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
                (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
                (306, 37520), ]  # (DateTime, SubsecTime)

        img = Image.open(open(file, 'rb'))
        img.load()

        exif = img._getexif()

        print(Fore.WHITE + 'Got Exif Data')

        for t in tags:
            dat = exif.get(t[0])


            # PIL.PILLOW_VERSION >= 3.0 returns a tuple
            dat = dat[0] if type(dat) == tuple else dat

            if dat != None: break

        if dat == None: return 'No Exif Data'
        full = '{}'.format(dat)
        Time = datetime.strptime(full, std_fmt)
        # T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
        Time = str(Time)
        Final = Time.replace(':', '')
        Final = Final.replace('-', '')
        Final = Final.replace(' ', '_')
        size = len(Final)
        final_str = Final[:size - 2]
        print(final_str)
        return final_str
    except:
        return ('No Exif Data')

def getLastSunday(year, month):


    last_sunday = max(week[-1] for week in calendar.monthcalendar(year, month))

    date = datetime(year, month, last_sunday, 2, 0)

    return (date)

def read_movAndmp4(file):
    print('Read mov/mp4-File...')

    try:
        parser = createParser(file)
        metadata = extractMetadata(parser)
        Time = str(metadata.get('creation_date'))

        date_time_obj = datetime.strptime(Time, '%Y-%m-%d %H:%M:%S')
        date_time_obj = date_time_obj + timedelta(hours=1)


        start = getLastSunday(date_time_obj.year, 3)
        end = getLastSunday(date_time_obj.year, 10)
        end = end + timedelta(hours=1)

        if start <= date_time_obj <= end:
            date_time_obj = date_time_obj + timedelta(hours=1)
            print('1')




        Time = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
        Final = Time.replace(':', '')
        Final = Final.replace('-', '')
        Final = Final.replace(' ', '_')
        size = len(Final)
        final_str = Final[:size - 2]
        print(final_str)
        return final_str
    except:
        return ('No Exif Data')



def read_png(file):
    print('Read png-File...')
    try:
        im = Image.open(file)
        im.load()  # Needed only for .png EXIF data (see citation above)
        #print(im.info)
        xmp = im.getxmp()
        Time = xmp['xmpmeta']['RDF']['Description']['DateCreated']
        Final = Time.replace(':', '')
        Final = Final.replace('-', '')
        Final = Final.replace('T', '_')
        size = len(Final)
        final_str = Final[:size - 2]
        print(final_str)
        return final_str
    except:
        return ('No Exif Data')
def getParentFolder():
    return input(Fore.BLUE + "Herkunft: ")
def makeOutputRename(EndPath):

    isOutput = os.path.isdir(os.path.join(EndPath, 'Output_Rename_1'))
    counter = 1;
    while(isOutput):
        counter = counter+1
        isOutput = os.path.isdir(os.path.join(EndPath, ('Output_Rename_' + str(counter))))

    os.makedirs(os.path.join(EndPath, ('Output_Rename_' + str(counter))))
    OutputPath = os.path.join(EndPath, ('Output_Rename_' + str(counter)))
    os.makedirs(os.path.join(OutputPath, 'Renamed'))
    os.makedirs(os.path.join(OutputPath, 'NotRenamed'))

    print(OutputPath)
    return OutputPath

def Rename(file, OutputPath, parentFolder, pfad):
    date = ''
    try:
        if (file.endswith('.PNG') or file.endswith('.png')):
            date = str(read_png(pfad))
        elif (file.endswith('.MOV') or file.endswith('.mov')):
            date = str(read_movAndmp4(pfad))
        elif (file.endswith('.mp4') or file.endswith('.MP4')):
            date = str(read_movAndmp4(pfad))
        elif (file.endswith('.jpg') or file.endswith('.JPG')):
            date = str(read_jpg(pfad))
    except:
        pass
    if ('No Exif Data' in date or date == ''):
        print(Fore.WHITE + 'File: ' + file + Fore.RED + ' New Name: ' + date)
        shutil.copy2(pfad, os.path.join(OutputPath, 'NotRenamed'))
        NewFileDest = os.path.join(OutputPath, 'NotRenamed')
        NewFileDest = os.path.join(NewFileDest, file)
        print(Fore.WHITE)
    else:

        indexName = file.rindex('.')
        sub = len(file) - indexName
        filename = file[:-sub]
        date = date[2:]
        newName = date + '_' + parentFolder + '_' + FileRenamed + '_' + filename + file.replace(filename, '')
        try:
            newName = newName.replace('               ', '')
            newName = newName.replace(':', '-')
        except:
            pass
        print(newName)
        print(Fore.WHITE + 'File: ' + file + Fore.GREEN + ' New Name: ' + date)
        shutil.copy2(pfad, os.path.join(OutputPath, 'Renamed'))

        NewFileDest = os.path.join(OutputPath, 'Renamed')
        NewFileDest = os.path.join(NewFileDest, file)

        NewFileName = os.path.join(OutputPath, 'Renamed')
        NewFileName = os.path.join(NewFileName, newName)

        os.rename(NewFileDest, NewFileName)
        print(Fore.WHITE)

def RunRenameFile(fileList):
    if not(fileList.endswith('.txt')):
        print(Fore.RED + 'Falsches Dateiformat')
        start()
    if not(Path(fileList).is_file()):
        print(Fore.RED + 'Liste existiert nicht')
        start()
    EndPath = input('Wählen sie das Zielverzeichnis: ')  # shows dialog box and return the path

    OutputPath = makeOutputRename(EndPath)
    print(Fore.WHITE)
    parentFolder = getParentFolder()

    with open(fileList, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            pfad = stripped_line


            try:
                indexName = pfad.rindex(chr(47))
            except:
                pass
            try:
                indexName = pfad.rindex(chr(92))
            except:
                pass


            sub = len(pfad) - indexName-1
            onlypath = pfad[:-sub]
            file = pfad.replace(onlypath, '')
            print(file)
            print(Fore.WHITE + "")
            Rename(file, OutputPath, parentFolder, pfad)




def RunRename():

    OriPath = input('Wählen sie das Ursprungsverzeichnis: ')  # shows dialog box and return the path

    EndPath = input('Wählen sie das Zielverzeichnis: ')  # shows dialog box and return the path
    print(OriPath)
    print(EndPath)

    OutputPath = makeOutputRename(EndPath)
    print(Fore.WHITE)
    parentFolder = getParentFolder()

    for root, dirs, files in os.walk(OriPath):
        for file in files:
            pfad = os.path.join(root, file)
            print(Fore.WHITE + "")
            Rename(file, OutputPath, parentFolder, pfad)
        break
    print(Fore.WHITE)




def help():
    print(Fore.GREEN + '')
    print(Fore.GREEN + 'fotos   -v')
    print(Fore.GREEN + '-v      Auswahl zweier Verzeichnisse zum Vergleich. Ergebnis sind 5 Vergleichslisten in Form von txt-Dateien')
    print(Fore.GREEN + '')
    print(Fore.GREEN + 'fotos   -r [<Pfad>]')
    print(Fore.GREEN + '-r      Ersetze Dateinamen mit <YYMMTT_HHMM_Origin_§_Originalfilename.Filetype>')
    print(Fore.GREEN + '        Zeiten immer an Sommerzeit und Winterzeit angepasst')
    print(Fore.GREEN + '<Pfad>  Pfad zu einer txt-Datei mit Pfaden zu den Dateien, die verarbeitet werden sollen')
    print(Fore.GREEN + '')
    print(Fore.GREEN + 'fotos   -c <Pfad>')
    print(Fore.GREEN + '-c      Kopiere Dateien in ausgewähltes Zielverzeichnis')
    print(Fore.GREEN + '<Pfad>  Pfad zu einer txt-Datei mit Pfaden zu den Dateien, die verarbeitet werden sollen')
    print(Fore.GREEN + '')
    print(Fore.GREEN + 'fotos   -d <Pfad>')
    print(Fore.GREEN + '-d      Lösche Dateien')
    print(Fore.GREEN + '<Pfad>  Pfad zu einer txt-Datei mit Pfaden zu den Dateien, die verarbeitet werden sollen')
    print(Fore.GREEN + '')
    start()
def makeOutputVergleich(ZielPath):

    isOutput = os.path.isdir(os.path.join(ZielPath, 'Output_Vergleich_1'))
    counter = 1;
    while(isOutput):
        counter = counter+1
        isOutput = os.path.isdir(os.path.join(ZielPath, ('Output_Vergleich_' + str(counter))))

    os.makedirs(os.path.join(ZielPath, ('Output_Vergleich_' + str(counter))))
    OutputPath = os.path.join(ZielPath, ('Output_Vergleich_' + str(counter)))


    print(OutputPath)
    return OutputPath


def Vergleich():
    ZielPath = r''
    verz1 = input('Wählen Sie das erste Verzeichnis: ')  # shows dialog box and return the path
    verz2 = input('Wählen Sie das zweite Verzeichnis: ')  # shows dialog box and return the path
    ZielPath = input('Wählen Sie, wo das Ergebnis gespeichert werden soll: ')  # shows dialog box and return the path
    if(verz1 == verz2):
        print(Fore.RED + 'Die Verzeichnisse dürfen nicht identisch sein')
        start()
    unique1 = []
    unique2 = []
    same = []
    same1 = []
    same2 = []
    hide = []
    print("Verz1: " + verz1)
    print("Verz2: " + verz2)
    print("Ziel: " + ZielPath)

    for root1, dirs1, files1 in os.walk(verz1):
        for file1 in files1:
            pfad1 = os.path.join(root1, file1)

            for root2, dirs2, files2 in os.walk(verz2):
                for file2 in files2:
                    pfad2 = os.path.join(root2, file2)
                    if (file1.startswith('._') or file2.startswith('._')):
                        continue

                    if filecmp.cmp(pfad1, pfad2):
                        img = []
                        img.append(pfad1)
                        img.append(pfad2)
                        same.append(img)
                break  # auch bei Vergleich?
        break  # auch bei Vergleich?


    for root1, dirs1, files1 in os.walk(verz1):
        for file1 in files1:
            if (file1.startswith('._')):
                pfad1 = os.path.join(root1, file1)
                hide.append(pfad1)
                continue

            pfad1 = os.path.join(root1, file1)
            pfad1 = pfad1.replace(chr(92), '/')
            b = False
            for a in same:

                for r in a:
                    f = r.replace(chr(92), '/')

                    if (pfad1 == f):
                        b = True
            if not b:
                unique1.append(pfad1)
        break #auch bei Vergleich?

    for root2, dirs2, files2 in os.walk(verz2):
        for file2 in files2:
            if (file2.startswith('._')):
                pfad2 = os.path.join(root2, file2)
                hide.append(pfad2)
                continue
            pfad2 = os.path.join(root2, file2)
            pfad2 = pfad2.replace(chr(92), '/')
            b = False
            for a in same:

                for r in a:
                    f = r.replace(chr(92), '/')

                    if (pfad2 == f):
                        b = True
            if not b:
                unique2.append(pfad2)
        break  # auch bei Vergleich?


    for ar in same:
        same1.append(ar[0])
        same2.append(ar[1])





    try:
        indexName = verz1.rindex('/')
    except:
        pass
    try:
        indexName = verz1.rindex(chr(92))
    except:
        pass
    sub = len(verz1) - indexName-1
    name1 = verz1[:-sub]
    name1 = verz1.replace(name1, '')

    try:
        indexName = verz2.rindex('/')
    except:
        pass
    try:
        indexName = verz2.rindex(chr(92))
    except:
        pass
    sub = len(verz2) - indexName-1
    name2 = verz2[:-sub]
    name2 = verz2.replace(name2, '')



    OutputPath = makeOutputVergleich(ZielPath)


    print("name1: " + name1)
    print("name2: " + name2)

    myfile1 = Path(OutputPath+'/Einzigartig1_'+name1+'.txt')
    myfile2 = Path(OutputPath+'/Einzigartig2_'+name2+'.txt')

    print("Anzahl Dateien in Same: " + str(len(same)))
    print("Anzahl Dateien nur in Verzeichnis1: " + str(len(unique1)))
    print("Anzahl Dateien nur in Verzeichnis2: " + str(len(unique2)))
    print("Anzahl versteckter Dateien  in beiden Verzeichnissen: " + str(len(hide)))

    f1 = open(myfile1, 'w+')
    f2 = open(myfile2, 'w+')
    for l in unique1:
        f1.write(l)
        f1.write("\n")
    f1.close()
    for l in unique2:
        f2.write(l)
        f2.write("\n")
    f2.close()

    myfile3 = Path(OutputPath+'/Überlappung_'+ name1 + '_' + name2+'.txt')
    f3 = open(myfile3, 'w+')
    for l in same:
        for s in l:
            f3.write(s)
            f3.write(" \n")
        f3.write(" \n")
    f3.close()

    myfile4 = Path(OutputPath + '/Überlappung1_' + name1 + '.txt')
    f4 = open(myfile4, 'w+')
    for l in same1:
        f4.write(l)
        f4.write(" \n")
    f4.close()

    myfile5 = Path(OutputPath + '/Überlappung2_' + name2 + '.txt')
    f5 = open(myfile5, 'w+')
    for l in same2:
        f5.write(l)
        f5.write(" \n")
    f5.close()

    myfile6 = Path(OutputPath + '/HiddenResourceFork' + '.txt')
    f6 = open(myfile6, 'w+')
    for l in hide:
        f6.write(l)
        f6.write(" \n")
    f6.close()

    print('Vergleich beendet')
    start()


def Copy(fileList):
    if not(fileList.endswith('.txt')):
        print(Fore.RED + 'Falsches Dateiformat')
        start()
    if not(Path(fileList).is_file()):
        print(Fore.RED + 'Liste existiert nicht')
        start()
    ZielPath = input('Wählen sie das Zielverzeichnis: ')  # shows dialog box and return the path
    with open(fileList, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            if(os.path.isfile(stripped_line)):
                shutil.copy2(stripped_line, ZielPath)
    start()


def Delete(fileList):
    if not(fileList.endswith('.txt')):
        print(Fore.RED + 'Falsches Dateiformat')
        start()
    if not(Path(fileList).is_file()):
        print(Fore.RED + 'Liste existiert nicht')
        start()

    with open(fileList, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            if(os.path.isfile(stripped_line)):
                os.remove(stripped_line)
    start()

def start():

    print(Fore.WHITE + 'Geben Sie ihren Befehl ein... (fotos -h für hilfe)')
    command = input()
    command = command.strip()
    if not("fotos " in command):
        start()
    else:
        command = command.replace("fotos ", '')
    if('-h' in command):
        help()
    elif('-r' in command):
        if('-r ' in command):
            command = command.replace("-r ", '')
            RunRenameFile(command)
        else:
            RunRename()
    elif('-v' in command):
        command = command.replace("-v", '')
        Vergleich()
    elif('-c ' in command):
        command = command.replace("-c ", '')
        Copy(command)
    elif('-d ' in command):
        command = command.replace("-d ", '')
        Delete(command)

    start()


start()

