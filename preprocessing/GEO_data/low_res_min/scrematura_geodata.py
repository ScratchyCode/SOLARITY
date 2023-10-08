# scriptino per scremare i Kp registrati a terra referenziati con la data per allinearli agli ingressi della RNN
import os

script_name = os.path.basename(__file__)

file_list = [file for file in os.listdir() if os.path.isfile(file) and file != script_name]

file_list.sort(key=lambda x: int(x.split('_')[0]))

with open("data_Kp", "w") as output_file:
    for file_name in file_list:
        anno = file_name.split('_')[0]
        
        with open(file_name, "r") as input_file:
            lines = input_file.readlines()
            
            for line in lines:
                columns = line.split()
                
                # estrai la prima colonna con l'anno dal nome del file e le colonne 2 e 3 nei file di dati originali
                data = f"{anno} {columns[1]} {columns[2]}"
                
                # estrai la colonna 39 nei file di dati originali (Kp)
                valore = columns[38]
                
                # scrivi i valori nel nuovo file
                output_file.write(f"{data} {valore}\n")

