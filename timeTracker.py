import time
import datetime
import csv
import os

#timer starts
startTime = time.time()
lastTime = startTime
lapNum = 1
value = ""

print("Press ENTER for each lap.\nType Q and press ENTER to stop.")

while value.lower() != "q":

    # Input for the Enter key press
    value = input()

    # The current lap-time
    lapTime = round((time.time() - lastTime), 2)

    # Total time elapsed since start
    totalTime = round((time.time() - lastTime), 2)

    # Printing the lap number, lap-time, and total time
    print("Lap No. "+str(lapNum))
    print("Total Time: "+str(totalTime))
    print("Lap Time: "+str(lapTime))

    print("*"*20)

    #Updating the previous total time and lap number
    lastTime = time.time()
    lapTime += 1

print("complete")

#session time
session_duration = round((time.time() - startTime), 2)

#save file
filename = "sessions.csv"
file_exists = os.path.isfile(filename)

with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Date", "Duration (seconds)"])
    writer.writerow([datetime.datetime.now().isoformat(), session_duration])

print(f"Session duration of {session_duration} seconds saved to {filename}.")

def total_Time():
    filename = "sessions.csv"
    total_seconds = 0

    if not os.path.exists(filename):
        print("No recorded sessions yet.")
        return
    
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_seconds += float(row["Duration (seconds)"])

    
    # Convert to format of hours/minutes/secconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    print(f"Total time spend on project: {hours}h {minutes}m {seconds}s")

# run project time
total_Time()