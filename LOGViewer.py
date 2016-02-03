############################################################
# Plot csv log files
#

import sys
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime

logamount = len(sys.argv) - 1

class log:
    def __init__(self, file):
        self.name = ''
        self.log = self.readcsv(file)

    def readcsv(self, file):
        # Leggo il file, rimuovo il fine linea, le "" e sostituisco , con .
        with open(file, mode='r') as csvfile:
            mylog = [s.strip().replace('\"', '').replace(',', '.').split(';') for s in csvfile]
        #Leggo il nome del log
        self.name = mylog[2][0]
        # Rimuovo la prima e l'ultima riga
        mylog = mylog[1:len(mylog) - 2]
        # Faccio la trasposizione della lista
        mylog = [list(x) for x in zip(*mylog)]
        # Tengo solo data/ora e valore
        mylog = mylog[1:2] + mylog[2:3]
        # Trasformo il valore da stringa a float
        mylog[1] = [float(v) for v in mylog[1]]
        # Trasformo data/ora in formato datetime
        mylog[0] = [dates.date2num(datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')) for x in mylog[0]]
        return mylog

def adjust_tbase(logs):
    # Inizializzo min e max in base al primo log
    minimum = min(logs[0].log[0])
    maximum = max(logs[0].log[0])
    # Trovo i tempi minimi e massimi presenti in tutti i log
    for log in logs:
        if (min(log.log[0]) > minimum): minimum = min(log.log[0])
        if (max(log.log[0]) < maximum): maximum = max(log.log[0])

    newlogs = [[[], []] for i in range(len(logs))]
    # Limito la finestra di tempo ai minimi e massimi comuni a tutti i log
    # Ricreo la matrice da zero aggiungendo solo i dati da considerare
    i = 0
    for log in logs:
        n = 0
        for col in log.log:
            x = 0
            for v in col:
                if n == 0 & (maximum <= v) & (v >= minimum):
                    newlogs[i][0].append(log.log[0][x])
                    newlogs[i][1].append(log.log[1][x])
                x += 1
            n += 1
        i += 1
    return newlogs

# Lista dei log
logs = []
# Lista dei file selezionati
flist = sys.argv[1:len(sys.argv)]
# Creo un log per ogni file
for f in flist:
    logs.append(log(f))

# Matrice dei dati filtrata
pltlogs = adjust_tbase(logs)

# Aggiungo tutti i log al plot con i relativi nomi
i = 0
for log in pltlogs:
    plt.plot_date(log[0], log[1], '-', label=logs[i].name)
    i += 1

plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
