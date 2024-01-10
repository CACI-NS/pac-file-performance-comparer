# Author: AAnkers
# Date: 10-Jan-2024
# Description: Compare two PAC files for performance and URL behaviour conformance
import pacparser
import time
import datetime
import csv

# Define Constants
INPUT_CSV = "tests.csv" # Filename of the input CSV file (informs the PAC Tester what expected behaviour, proxy or direct, is per URL; header format: url,expected_action)
OUTPUT_CSV = "output.csv" # Filename of the output CSV file
OLD_PAC = "prod.pac" # Filename of the first input PAC file (old pre-optimised version)
NEW_PAC = "prod_new.pac" # Filename of the second intput PAC file (new optimised version)

# Functions
# Perform the comparison and performance timing of each entry via the PAC file
def pac_test(url, pac_file):
    # Start time
    start_time = time.time()
    # PAC Parser
    pacparser.init()
    pacparser.parse_pac(pac_file)
    pacparser.setmyip("10.0.0.1")
    result = pacparser.find_proxy("https://" + url, url)
    # End time
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = int((end_time - start_time) * 1000)
    # Kill PAC Parser
    pacparser.cleanup()

    # Return result and time taken
    return result, elapsed_time


# Main program
print("JOB START: " + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z") + "\n")

# Open Tests CSV file, begin processing
print("Processing and comparing PAC file [" + OLD_PAC + "] against PAC file [" + NEW_PAC + "]...")
output = "url,old_pac_action,old_pac_status,old_pac_timer_milliseconds,new_pac_action,new_pac_status,new_pac_timer_milliseconds\n"
try:
    with open(INPUT_CSV, "r") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Test against old PAC
            result_old = pac_test(row["url"], OLD_PAC)
            status_old = "pass" if row["expected_action"].lower() in result_old[0].lower() else "fail"
            # Test against new PAC
            result_new = pac_test(row["url"], NEW_PAC)
            status_new = "pass" if row["expected_action"].lower() in result_new[0].lower() else "fail"
            print(" Entry: " + row["url"] + ' should go via: ' + row["expected_action"] + ", old PAC goes via: " + result_old[0] + ", new PAC goes via: " + result_new[0] + " [Old PAC Processing: " + str(result_old[1]) + " ms, New PAC Processing: " + str(result_new[1]) + " ms]")
            
            # Add to output string
            output += "{},{},{},{},{},{},{}\n".format(row["url"],result_old[0],status_old,result_old[1],result_new[0],status_new,result_new[1])
except Exception as e:
    print(" Error [" + str(e) + "]")

# Write CSV to output file
print("\nWriting output CSV to file [" + OUTPUT_CSV + "]...")
try:
    f = open(OUTPUT_CSV, "w")
    f.write(output)
    f.close()
    print(" Success")
    print("\nJOB END: " + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z"))
except Exception as e:
    print(" Error [" + str(e) + "]")
    print("\nJOB END: " + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z"))