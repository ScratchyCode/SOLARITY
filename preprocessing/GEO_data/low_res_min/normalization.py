import os
import datetime
from datetime import timedelta

with open("data_Kp", "r") as input_file:
    lines = input_file.readlines()

# initialize the maximum Kp value to an impossibly low value
max_kp = float('-inf')

# iterate over each line in the input file to find the maximum Kp value
for line in lines:
    columns = line.split()
    kp = float(columns[3])
    if kp > max_kp:
        max_kp = kp

with open("output_normalized", "w") as output_file:
    #output_file.write("#Year Month Day Hour Minute KP\n")

    # iterate again over each line in the input file
    for line in lines:
        columns = line.split()
        year = columns[0]
        day_of_year = columns[1]
        hour = columns[2]
        kp = float(columns[3])
        
        kp_normalized = kp / max_kp
        
        # iterate over 60 minutes to perform padding with respect to the data input to the RNN
        for minute in range(60):
            # calculate the month and day of the month from the day of the year column
            day_of_year_int = int(day_of_year)
            date = datetime.datetime(int(year), 1, 1) + timedelta(days=day_of_year_int - 1)
            month = date.month
            day_of_month = date.day
            
            # compute the synthesized date in "yyyy:mm:dd:hh:min" format
            synthesized_date = f"{year} {month} {day_of_month} {hour} {minute}"
            
            # write the synthesized date and the normalized Kp value to the new file
            output_file.write(f"{synthesized_date} {kp_normalized}\n")
