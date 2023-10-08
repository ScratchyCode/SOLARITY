# small script to skim the Kp recorded on the ground, referenced with the date to align them to the inputs of the RNN
import os

script_name = os.path.basename(__file__)

file_list = [file for file in os.listdir() if os.path.isfile(file) and file != script_name]

file_list.sort(key=lambda x: int(x.split('_')[0]))

with open("data_Kp", "w") as output_file:
    for file_name in file_list:
        year = file_name.split('_')[0]
        
        with open(file_name, "r") as input_file:
            lines = input_file.readlines()
            
            for line in lines:
                columns = line.split()
                
                # extract the first column with the year from the file name and columns 2 and 3 in the original data files
                date = f"{year} {columns[1]} {columns[2]}"
                
                # extract column 39 in the original data files (Kp)
                value = columns[38]
                
                # write the values to the new file
                output_file.write(f"{date} {value}\n")
