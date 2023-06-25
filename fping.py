#!/usr/bin/env python3

import re
import datetime
import subprocess

fping = "/usr/bin/fping"
fping_flags = "-D -Q1 -l"
ip_addr = "1.1.1.1 8.8.8.8"





def run_fping():
    # Get current local date and time
    current_date = datetime.datetime.today()



    # fping -D -Q1 -l 1.1.1.1 8.8.8.8 9.9.9.9 208.67.222.222 10.10.1.1

    cmd = " ".join([fping, fping_flags, ip_addr])

    print(f"Executing command: {cmd}")

    p1 = subprocess.Popen(cmd, stderr=subprocess.PIPE, text = True, shell = True)

    #print(f"Echo: {p1.stderr.read()}")

    for line in p1.stderr:
        line = line.strip()
        m = re.match('^\[(\d+)\:(\d+)\:(\d+)\]', line)

        if m: # Match the timestamp line
            # Compute the date to be stored in the database
            db_date = datetime.datetime(current_date.year, current_date.month, current_date.day, int(m.group(1)), int(m.group(2)), int(m.group(3)), 0)
            print(f"DB Date: {db_date}")
        else: # Match the stats line
            min = 0.0
            avg = 0.0
            max = 0.0

            print(f"Data: {line}")
            # In a normal situation, split returns 8 items, when 5 are returned it means there's a problem
            if len(line.split()) > 5:
                info = line.split()
                print(f"{info}")

                hostname = info[0]
                transfer_stats = info[4]
                time_stats = info[7] # if time_stats is empty it likely means there is a total outage

                print(f"Host : {hostname}")
                print(f"Stats: {time_stats}")

                min = time_stats.split('/')[0]
                avg = time_stats.split('/')[1]
                max = time_stats.split('/')[2]

                print(f"Min: {min}")
                print(f"Avg: {avg}")
                print(f"Max: {max}")
            else:
                print(f"SOMETHING IS WRONG!")

if __name__ == "__main__":
    run_fping()