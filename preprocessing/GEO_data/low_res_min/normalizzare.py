import os
import datetime
from datetime import timedelta

with open("data_Kp", "r") as input_file:
    lines = input_file.readlines()

# inizializza il massimo valore di Kp a un valore impossibilmente basso
max_kp = float('-inf')

# itera su ogni riga nel file di input per trovare il massimo valore di Kp
for line in lines:
    columns = line.split()
    kp = float(columns[3])
    if kp > max_kp:
        max_kp = kp

with open("output_normalizzati", "w") as output_file:
    #output_file.write("#Anno Mese Giorno Ora Minuti KP\n")

    # itera nuovamente su ogni riga nel file di input
    for line in lines:
        columns = line.split()
        anno = columns[0]
        giorno = columns[1]
        ora = columns[2]
        kp = float(columns[3])
        
        kp_normalized = kp / max_kp
        
        # itera su 60 minuti per eseguire il padding rispetto ai dati in input alla RNN
        for minuto in range(60):
            # calcola il mese e il giorno del mese dalla colonna del giorno dell'anno
            giorno_dell_anno = int(giorno)
            data = datetime.datetime(int(anno), 1, 1) + timedelta(days=giorno_dell_anno - 1)
            mese = data.month
            giorno_del_mese = data.day
            
            # calcola la data sintetizzata in formato "yyyy:mm:dd:hh:min"
            data_sintetizzata = f"{anno} {mese} {giorno_del_mese} {ora} {minuto}"
            
            # scrivi la data sintetizzata e il valore Kp normalizzato nel nuovo file
            output_file.write(f"{data_sintetizzata} {kp_normalized}\n")

