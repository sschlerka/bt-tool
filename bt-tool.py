#    BT-Tool - Tool for dealing with Bundestag documents
#    Copyright (C) 2020 Sebastian Matthias Schlerka
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, platform, hashlib, glob, webbrowser, time, re#, biblib



# Festlegen der Pfade
xmlPath = 'xml'
pdfPath = 'pdf'
bibPath = 'bib'
txtPath = 'full-text'
dbPath = 'in-db'
nondbPath = 'not-in-database'

# Überprüfung des Betriebssystems für Clearscreen
if platform.system() == 'Linux' or 'Darwin':
    sys = 'unix'
elif platform.system() == 'Windows':
    sys = 'ms'
else:
    print('Entschuldigung, dieses Programm unterstützt nur Linux, Windows und Mac. Das Programm wird jetzt beendet.')
    exit()



def main():
    print('BT-Tool - Version 0.1 - Copyright (C) 2020 Sebastian Matthias Schlerka')
    print('----------------------------------------------------------------------')
    print('This program comes with ABSOLUTELY NO WARRANTY. This is free software,')
    print('and you are welcome to redistribute it under certain conditions; refer')
    print('to the GNU General Public License for more details.')
    print('----------------------------------------------------------------------')
    print('1. Konversion von XML in BibTeX')
    print('2. Extraktion von Volltexten aus XML')
    print('3. Bereits in einer Datenbank vorhandene PDF-Dateien aussortieren')
    print('4. XML-Dateien von der Webseite des Bundestags herunterladen (wird im Browser geöffnet)')
    print('5. PDOK-System des Bundestags öffnen (wird im Browser geöffnet)')
    print('6. Programm beenden')
    eingabe = input('Auswahl: ')
    if eingabe == '1':
        print('\n\n1. Konversion von XML in BibTeX')
        print('----------------------------------------------------------------------')
        print('1. Drucksachen')
        print('2. Plenarprotokolle')
        print('3. Zu PDF-Dateien')
        print('4. Zurück zur Hauptauswahl')
        auswahl = input('Auswahl: ')
        if auswahl == '1':
            print('Liste der Drucksachen bitte als drsliste.txt speichern.')
            input('Bitte ENTER drücken, um fortzufahren...')
            liste = open('drsliste.txt', 'r')
            lines = liste.readlines()
            for i in range(0, len(lines)):
                if lines[i].startswith(' ') or lines[i].startswith('\n'):
                   break
                while len(lines[i]) <= 8:
                    lines[i] = lines[i].replace('/', '/0')
                lines[i] = lines[i].replace('/', '')
                lines[i] = lines[i].replace('\n', '')
                xmltobib(lines[i] + '.xml')
            liste.close
            clearscreen()
            main()
        elif auswahl == '2':
            print('Liste der Plenarprotokolle bitte als ppliste.txt speichern.')
            input('Bitte ENTER drücken, um fortzufahren...')
            liste = open('ppliste.txt', 'r')
            lines = liste.readlines()
            for i in range(0, len(lines)):
                if lines[i].startswith(' ') or lines[i].startswith('\n'):
                   break
                while len(lines[i]) <= 6:
                    lines[i] = lines[i].replace('/', '/0')
                lines[i] = lines[i].replace('/', '')
                lines[i] = lines[i].replace('\n', '')
                xmltobib(lines[i] + '.xml')
            liste.close
            clearscreen()
            main()
        elif auswahl == '3':
            print('Die PDF-Dateien bitte mit Original-Dateinamen im Unterordner ./pdf speichern!')
            input('Bitte ENTER drücken, um fortzufahren...')
            for i in os.listdir(pdfPath):
                # print(i) #Testzwecke
                xml = i.replace('pdf', 'xml')
                for j in os.listdir(xmlPath):
                    if xml == j:
                        # print(j) #Testzwecke
                        xmltobib(j)
            clearscreen()
            main()
        elif auswahl == '4':
            clearscreen()
            main()
        else:
            print('\n\nUngültige Eingabe. Das Programm wird neu gestartet', end='')
            for i in range(0,2):
                print('.', end='', flush=True),
                time.sleep(0.75)
            print('.', flush=True)
            time.sleep(0.75)
            clearscreen()
            main()
    elif eingabe == '2':
       print('\n\n2. Extraktion von Volltexten aus XML')
       print('----------------------------------------------------------------------')
       print('1. Drucksachen')
       print('2. Plenarprotokolle')
       print('3. Aus BibTeX')
       print('4. Zu PDF-Dateien')
       print('5. Zurück zur Hauptauswahl')
       auswahl = input('Auswahl: ')
       if auswahl == '1':
           liste = open('drsliste.txt', 'r')
           lines = liste.readlines()
           for i in range(0, len(lines)):
               if lines[i].startswith(' ') or lines[i].startswith('\n'):
                   break
               while len(lines[i]) <= 8:
                   lines[i] = lines[i].replace('/', '/0')
               lines[i] = lines[i].replace('/', '')
               lines[i] = lines[i].replace('\n', '')
               extracttxt(lines[i] + '.xml')
           liste.close
           clearscreen()
           main()
       elif auswahl == '2':
           liste = open('ppliste.txt', 'r')
           lines = liste.readlines()
           for i in range(0, len(lines)):
               if lines[i].startswith(' ') or lines[i].startswith('\n'):
                   break
               while len(lines[i]) <= 6:
                   lines[i] = lines[i].replace('/', '/0')
               lines[i] = lines[i].replace('/', '')
               lines[i] = lines[i].replace('\n', '')
               extracttxt(lines[i] + '.xml')
           liste.close
           clearscreen()
           main()
       elif auswahl == '3':
           readbib('input.bib')
           for i in range(0, len(drsvorhanden)):
               extracttxt(drsvorhanden[i] + '.xml')
           for i in range(0, len(ppvorhanden)):
               extracttxt(ppvorhanden[i] + '.xml')
       elif auswahl == '4':
           for i in os.listdir(xmlPath):
               pdf = i.replace('xml', 'pdf')
               for j in os.listdir(pdfPath):
                    if pdf == j:
                        extracttxt(i)
                        break
       elif auswahl == '5':
           clearscreen()
           main()
       else:
           print('\n\nUngültige Eingabe. Das Programm wird neu gestartet', end='')
           for i in range(0,2):
               print('.', end='', flush=True),
               time.sleep(0.75)
           print('.', flush=True)
           time.sleep(0.75)
           clearscreen()
           main()
    elif eingabe == '3':
        print('\n\n3. Bereits in einer Datenbank vorhandene PDF-Dateien aussortieren')
        print('.bib-Datei bitte als input.bib im selben Ordner wie das Programm speichern!')
        input('Bitte ENTER drücken, um fortzufahren...')
        readbib('input.bib')
        print('1. OHNE Konversion von XML in BibTeX')
        print('2. MIT Konversion von XML in BibTeX')
        print('3. Zurück zur Hauptauswahl')
        auswahl = input('Auswahl: ')
        if auswahl == '1':
            filterInDatabase()
            comparePdf()
            clearscreen()
            main()
        elif auswahl == '2':
            for i in range(0, len(drsvorhanden)):
                xmltobib(drsvorhanden[i] + '.xml')
            for i in range(0, len(ppvorhanden)):
                xmltobib(ppvorhanden[i] + '.xml')
            print(drsvorhanden)    #Testzwecke
            print(ppvorhanden)     #Testzwecke
            #print(bibitems)        #Testzwecke
            filterInDatabase()
            #print(pppdf)            #Testzwecke
            #print(drspdf)           #Testzwecke
            comparePdf()
            clearscreen()
            main()
        elif auswahl == '3':
            clearscreen()
            main()
        else:
            print('\n\nUngültige Eingabe. Das Programm wird neu gestartet', end='')
            for i in range(0,2):
                print('.', end='', flush=True),
                time.sleep(0.75)
            print('.', flush=True)
            time.sleep(0.75)
            clearscreen()
            main()
    elif eingabe == '4':
        webbrowser.open('https://www.bundestag.de/services/opendata', new=2)
        time.sleep(2)
        clearscreen()
        main()
    elif eingabe == '5':
        webbrowser.open('https://pdok.bundestag.de', new=2)
        time.sleep(2)
        clearscreen()
        main()
    elif eingabe == '6':
        exit()
    else:
        print('\n\nUngültige Eingabe. Das Programm wird neu gestartet', end='')
        for i in range(0,2):
            print('.', end='', flush=True),
            time.sleep(0.75)
        print('.', flush=True)
        time.sleep(0.75)
        clearscreen()
        main()


def clearscreen():
    if sys == 'unix':
        os.system('clear')
    elif sys == 'ms':
        os.system('cls')

def extracttxt(x):
    xml = open(os.path.join(xmlPath, x), 'r')
    lineslist = xml.readlines()
    txt = open(os.path.join(txtPath, x.replace('xml', 'txt')), 'w')

    for i in range(0, len(lineslist)):
        if '<TEXT>' in lineslist[i]:
            lineslist[i] = lineslist[i].replace('  <TEXT>', '')
            text = i
            break
    for i in range(text, len(lineslist)):
        if '</TEXT>' in lineslist[text]:
            lineslist[text] = lineslist[text].replace('</TEXT>', '')
        if '</DOKUMENT>' in lineslist[text]:
            lineslist[text] = lineslist[text].replace('</DOKUMENT>', '')
        txt.write(lineslist[text])
        text = text + 1

    xml.close
    txt.close

def readbib(x): # Liest eine BibTeX-Datei x ein und gibt je eine Listenvariable mit allen Drucksachen (drsvorhanden) und Plenarprotokollen (ppvorhanden) aus -- FINAL
    global drsvorhanden
    global ppvorhanden
    #global bibitems #Hinterher löschen, soll nur zu Testzwecken ausgegeben werden
    ppvorhanden = []
    drsvorhanden = []
    bibitems = []
    counter = 0
    f = open(x, "r")
    lineslist = f.readlines()
    f.close

    for i in range(0, len(lineslist)):
        if lineslist[i].startswith('\n'):
            continue
        if lineslist[i].startswith('@'):
            bibitems.append(lineslist[i])
            counter = bibitems.index(lineslist[i])
        bibitems[counter] = bibitems[counter] + lineslist[i]

    p = re.compile('Plenarprotokoll', re.IGNORECASE)
    for i in range(0, len(bibitems)):
        if re.search(p, bibitems[i]):
            print('True')
            m = re.search('(?<=[Nn][Uu][Mm][Bb][Ee][Rr])\s{1,2}\=\s{1,2}\{\d{1,2}\/\d{1,3}', bibitems[i])
            ppvorhanden.append(m[0])
        else:
            m = re.search('(?<=[Nn][Uu][Mm][Bb][Ee][Rr])\s{1,2}\=\s{1,2}\{\d{1,2}\/\d{1,5}', bibitems[i])
            drsvorhanden.append(m[0])

    #print(ppvorhanden)  #Zu Testzwecken
    #print(drsvorhanden) #Zu Testzwecken

    for i in range(0, len(drsvorhanden)):
        m = re.match('\s*\=\s*\{', drsvorhanden[i])
        drsvorhanden[i] = drsvorhanden[i].replace(m[0], '')
        while len(drsvorhanden[i]) <= 7:
            drsvorhanden[i] = drsvorhanden[i].replace('/', '/0')
        drsvorhanden[i] = drsvorhanden[i].replace('/', '')
    for i in range(0, len(ppvorhanden)):
        m = re.match('\s*\=\s*\{', ppvorhanden[i])
        ppvorhanden[i] = ppvorhanden[i].replace(m[0], '')
        while len(ppvorhanden[i]) <= 5:
            ppvorhanden[i] = ppvorhanden[i].replace('/', '/0')
        ppvorhanden[i] = ppvorhanden[i].replace('/', '')

    #print(ppvorhanden)  #Zu Testzwecken
    #print(drsvorhanden) #Zu Testzwecken

    return ppvorhanden, drsvorhanden#, bibitems

def xmltobib(x): # Übersetzer von Bundestags-XML zu .bib -- FINAL
    xml = open(os.path.join(xmlPath, x), 'r')
    lineslist = xml.readlines()
    bib = open(os.path.join(bibPath, x.replace('xml', 'bib')), 'w')
    out = open('output.bib', 'a')

    for i in range(0, len(lineslist)):
        if lineslist[i].startswith('  <DOKUMENTART>PLENARPROTOKOLL'):
            typ = 'pp'
            break
        elif lineslist[i].startswith('  <DOKUMENTART>DRUCKSACHE'):
            typ = 'drs'
            break

    bib.write('@techreport{' + x + ',\n')
    out.write('\n@techreport{' + x + ',\n')
    bib.write('\tinstitution = {Deutscher Bundestag},\n')
    out.write('\tinstitution = {Deutscher Bundestag},\n')

    for i in range(0, len(lineslist)):
        if lineslist[i].startswith(' <WAHLPERIODE>1') or lineslist[i].startswith(' <WAHLPERIODE>2') or lineslist[i].startswith(' <WAHLPERIODE>3') or lineslist[i].startswith(' <WAHLPERIODE>4') or lineslist[i].startswith(' <WAHLPERIODE>5') or lineslist[i].startswith(' <WAHLPERIODE>6') or lineslist[i].startswith(' <WAHLPERIODE>7') or lineslist[i].startswith(' <WAHLPERIODE>8') or lineslist[i].startswith(' <WAHLPERIODE>9') or lineslist[i].startswith(' <WAHLPERIODE>10') or lineslist[i].startswith(' <WAHLPERIODE>11') or lineslist[i].startswith(' <WAHLPERIODE>12') or lineslist[i].startswith(' <WAHLPERIODE>13'):
            bib.write('\taddress = {Bonn},\n')
            out.write('\taddress = {Bonn},\n')
        if lineslist[i].startswith('  <WAHLPERIODE>14'):
            bib.write('\taddress = {Bonn/Berlin},\n')
            out.write('\taddress = {Bonn/Berlin},\n')
        if lineslist[i].startswith('  <WAHLPERIODE>15') or lineslist[i].startswith(' <WAHLPERIODE>16') or lineslist[i].startswith(' <WAHLPERIODE>17') or lineslist[i].startswith(' <WAHLPERIODE>18') or lineslist[i].startswith(' <WAHLPERIODE>19') or lineslist[i].startswith(' <WAHLPERIODE>20') or lineslist[i].startswith(' <WAHLPERIODE>21') or lineslist[i].startswith(' <WAHLPERIODE>22') or lineslist[i].startswith(' <WAHLPERIODE>23') or lineslist[i].startswith(' <WAHLPERIODE>24') or lineslist[i].startswith(' <WAHLPERIODE>25') or lineslist[i].startswith(' <WAHLPERIODE>26') or lineslist[i].startswith(' <WAHLPERIODE>27'): #Das Ding funktioniert ohne Einschränkungen bis 2053!!!
            bib.write('\taddress = {Berlin},\n')
            out.write('\taddress = {Berlin},\n')


    for i in range (0, len(lineslist)):
        if lineslist[i].startswith('  <DRS_TYP>') and not lineslist[i+1].startswith('  <TEXT>'):
            lineslist[i] = lineslist[i].replace('  <DRS_TYP>', '\ttype = {')
            lineslist[i] = lineslist[i].replace('</DRS_TYP>', '},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <DRS_TYP>') and lineslist[i+1].startswith('  <TEXT>'):
            lineslist[i] = lineslist[i].replace('  <DRS_TYP>', '\ttype = {')
            lineslist[i] = lineslist[i].replace('</DRS_TYP>', '}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <NR>') and not lineslist[i+1].startswith('  <TEXT>'):
            lineslist[i] = lineslist[i].replace('  <NR>', '\tnumber = {')
            lineslist[i] = lineslist[i].replace('</NR>', '},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <NR>') and lineslist[i+1].startswith('  <TEXT>'):
            lineslist[i] = lineslist[i].replace('  <NR>', '\tnumber = {')
            lineslist[i] = lineslist[i].replace('</NR>', '}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <DATUM>') and not lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <DATUM>', '\tdate = {')
            lineslist[i] = lineslist[i].replace('</DATUM>', '},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <DATUM>') and lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <DATUM>', '\tdate = {')
            lineslist[i] = lineslist[i].replace('</DATUM>', '}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <TITEL>') and not lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <TITEL>', '\ttitle = {')
            lineslist[i] = lineslist[i].replace('</TITEL>', '},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <TITEL>') and lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <TITEL>', '\ttitle = {')
            lineslist[i] = lineslist[i].replace('</TITEL>', '}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <K_URHEBER') and not lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <K_URHEBER>', '\tauthor = {{')
            lineslist[i] = lineslist[i].replace('</K_URHEBER>', '}},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <K_URHEBER') and lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <K_URHEBER>', '\tauthor = {{')
            lineslist[i] = lineslist[i].replace('</K_URHEBER>', '}}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <P_URHEBER') and not lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <P_URHEBER>', '\tauthor = {')
            lineslist[i] = lineslist[i].replace('</P_URHEBER>', '},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <P_URHEBER') and lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <P_URHEBER>', '\tauthor = {')
            lineslist[i] = lineslist[i].replace('</P_URHEBER>', '}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <WAHLPERIODE') and not lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <WAHLPERIODE>', '\tkeywords = {')
            lineslist[i] = lineslist[i].replace('</WAHLPERIODE>', '. Wahlperiode},')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <WAHLPERIODE') and lineslist[i+1].startswith('  <TEXT'):
            lineslist[i] = lineslist[i].replace('  <WAHLPERIODE>', '\tkeywords = {')
            lineslist[i] = lineslist[i].replace('</WAHLPERIODE>', '. Wahlperiode}')
            bib.write(lineslist[i])
            out.write(lineslist[i])
        if lineslist[i].startswith('  <TEXT'):
            bib.write('}')
            out.write('}')
            break

    xml.close
    bib.close
    out.close

def filterxmlbib(): # Filtert aus allen XML-Dateien (Drs und PP) diejenigen heraus, die in der .bib vorkommen #FÜR FINAL: Kopieren noch auf löschen umstellen, wenn bit == 0
    for j in os.listdir(xmlPath):
        bit = 0
        for i in range(0, len(drsvorhanden)):
            if x == drsvorhanden[i] + '.xml':
                bit = 1
                break
        for i in range(0, len(ppvorhanden)):
            if x == ppvorhanden[i] + '.xml':
                bit = 1
                break
        if bit == 1:
            xmltobib(os.path.join(xmlPath, j))

def filterxmlpdf(): # Filtert aus allen XML-Dateien diejenigen heraus, die als PDF (Originalnamen) vorliegen
    main()

def filterInDatabase():
    global drspdf, pppdf
    drspdf = []
    pppdf = []
    for x in os.listdir(pdfPath):
        bit = 0
        for i in range(0, len(drsvorhanden)):
            if x == drsvorhanden[i] + '.pdf':
                bit = 1
                drspdf.append(drsvorhanden[i] + '.pdf')
                break
        for i in range(0, len(ppvorhanden)):
            if x == ppvorhanden[i] + '.pdf':
                bit = 1
                pppdf.append(ppvorhanden[i] + '.pdf')
                break
    return drspdf, pppdf

def comparePdf(): # Sortiert PDF-Dateien im Stammordner in dbPath, wenn sie in der Bib-Datei enthalten sind, und in nondbPath, wenn sie nicht enthalten sind; hängt von der vorherigen Ausführung von filterInDatabase ab!
    for x in glob.glob('*.pdf'):
        inDB = 0
        hash1 = hashlib.md5()
        BLOCKSIZE = 32768
        with open(x, 'rb') as pdfA:
            buf1 = pdfA.read(BLOCKSIZE)
            while len(buf1) > 0:
                hash1.update(buf1)
                buf1 = pdfA.read(BLOCKSIZE)
            for y in range(0, len(drspdf)):
                hash2 = hashlib.md5()
                with open(os.path.join(pdfPath, drspdf[y]), 'rb') as pdfB:
                    buf2 = pdfB.read(BLOCKSIZE)
                    while len(buf2) > 0:
                        hash2.update(buf2)
                        buf2 = pdfB.read(BLOCKSIZE)
                    if hash1.hexdigest() == hash2.hexdigest():
                        inDB = 1
                        break
            for y in range (0, len(pppdf)):
                hash2 = hashlib.md5()
                with open(os.path.join(pdfPath, pppdf[y]), 'rb') as pdfB:
                    buf2 = pdfB.read(BLOCKSIZE)
                    while len(buf2) > 0:
                        hash2.update(buf2)
                        buf2 = pdfB.read(BLOCKSIZE)
                    if hash1.hexdigest() == hash2.hexdigest():
                        inDB = 1
                        break
            if inDB == 1:
                oldfile = x
                newfile = os.path.join(dbPath, x)
                os.rename(oldfile, newfile)
            #else:
            #    oldfile = x
            #    newfile = os.path.join(nondbPath, x)
            #    os.rename(oldfile, newfile)

def test():
    print(ppvorhanden)
    print('Anzahl Plenarprotokolle: ', len(ppvorhanden))
    print(drsvorhanden)
    print('Anzahl Drucksachen: ', len(drsvorhanden))

main()

