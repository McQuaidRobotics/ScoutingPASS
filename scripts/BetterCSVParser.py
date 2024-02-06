import tkinter as tk
from tkinter import filedialog
import csv as csvStuff

AUTO_SCORE_LOCS = 'Auto Scoring Locations'
AUTO_MISS_LOCS = 'Auto Miss Locations'

CYCLE_TIMES = 'Cycle Timer'
TELE_SCORE_LOCS = 'Teleop Scoring Locations'
TELE_MISS_LOCS = 'Teleop Missing Locations'

CSV = list[list[str]]

isInMain = lambda mainCSV, h: h in mainCSV[0]

def findHeader(csv: CSV, header: str) -> int:
    for i in range(len(csv[0])):
        if csv[0][i] == header:
            return i
    return -1

def isolateCycleTime(csv: CSV):
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Team #', 'Cycle Time', 'Teleop Scoring Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        times = csv[i][findHeader(csv, CYCLE_TIMES)].split(",")
        locations = csv[i][findHeader(csv, TELE_SCORE_LOCS)].split(",")
        if(times[0] == '' or locations[0] == ''):
            continue
        for i2 in range(len(times)):
            newRow: list[str] = []
            for header in headers:
                if isInMain(csv, header):
                    newRow.append(csv[i][findHeader(csv, header)])
                elif header == headers[3]:
                    newRow.append(times[i2])
                elif header == headers[4]:
                    newRow.append(locations[i2])
            newCSV.append(newRow)
    return newCSV

def isolateTeleMisses(csv: CSV): 
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Team #', 'Teleop Miss Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        locations = csv[i][findHeader(csv, TELE_MISS_LOCS)].split(',')
        if locations[0] == '':
            continue
        for location in locations:
            newRow: list[str] = []
            for header in headers:
                if isInMain(csv, header):
                    newRow.append(csv[i][findHeader(csv, header)])
                else:
                    newRow.append(location)
            newCSV.append(newRow)
    return newCSV

def isolateAutoScores(csv: CSV):
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Team #', 'Auto Score Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        locations = csv[i][findHeader(csv, AUTO_SCORE_LOCS)].split(',')
        if locations[0] == '':
            continue
        for location in locations:
            newRow: list[str] = []
            for header in headers:
                if isInMain(csv, header):
                    newRow.append(csv[i][findHeader(csv, header)])
                else:
                    newRow.append(location)
            newCSV.append(newRow)
    return newCSV

def isolateAutoMissLocations(csv: CSV):
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Team #', 'Auto Miss Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        locations = csv[i][findHeader(csv, AUTO_MISS_LOCS)].split(',')
        if locations[0] == '':
            continue
        for location in locations:
            newRow: list[str] = []
            for header in headers:
                if isInMain(csv, header):
                    newRow.append(csv[i][findHeader(csv, header)])
                else:
                    newRow.append(location)
            newCSV.append(newRow)
    return newCSV

def isolateLocations(outputPath: str) -> CSV:
    newCSV = CSV()
    newCSV.append(['Match Level', 'Match #', 'Team #', 'Location'])
    file = open(outputPath + '/CycleTimes.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'Match Level':
            continue
        newRow = []
        newRow.append(row[0])
        newRow.append(row[1])
        newRow.append(row[2])
        newRow.append(row[4])
        newCSV.append(newRow)
    file.close()
    file = open(outputPath + '/TeleopMisses.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'Match Level':
            continue
        newCSV.append(row)
    file.close()
    file = open(outputPath + '/AutoMisses.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'Match Level':
            continue
        newCSV.append(row)
    file.close()
    file = open(outputPath + '/AutoScores.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'Match Level':
            continue
        newCSV.append(row)
    file.close()
    return newCSV

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
rows = CSV()
with open(file_path) as csvFile:
    reader = csvStuff.reader(csvFile)
    for row in reader:
        rows.append(row)

output_path = filedialog.askdirectory()
with open(output_path + "/CycleTimes.csv", 'w', encoding='utf-8') as csvFile:
    timesCSV = isolateCycleTime(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(timesCSV)

with open(output_path + "/TeleopMisses.csv", 'w', encoding='utf-8') as csvFile:
    teleMissesCSV = isolateTeleMisses(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(teleMissesCSV)

with open(output_path + "/AutoMisses.csv", 'w', encoding='utf-8') as csvFile:
    autoMissesCSV = isolateAutoMissLocations(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(autoMissesCSV)

with open(output_path + "/AutoScores.csv", 'w', encoding='utf-8') as csvFile:
    autoScoresCSV = isolateAutoScores(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(autoScoresCSV)

with open(output_path + "/AllLocations.csv", 'w', encoding='utf-8') as csvFile:
    locationsCSV = isolateLocations(output_path)
    writer = csvStuff.writer(csvFile, lineterminator='\n')
    writer.writerows(locationsCSV)
