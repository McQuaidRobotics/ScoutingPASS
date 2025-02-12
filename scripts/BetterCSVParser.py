import tkinter as tk
from tkinter import filedialog
import csv as csvStuff

AUTO_SCORE_LOCS = 'Auto Scoring Locations'
AUTO_PICKUP_LOCS = 'Auto Pickup Locations'

CYCLE_TIMES = 'Cycle Timer'
TELE_SCORE_LOCS = 'Teleop Scoring Locations'
TELE_MISS_LOCS = 'Teleop Missing Locations'

id: int = 1

CSV = list[list[str]]

class AllianceScores:
    total: int
    leaves: int
    autoAmp: int
    autoSpeaker: int
    teleopAmp: int
    teleopSpeakerScores: int
    teleopSpeakerPoints: int
    teleopAmpedSpeaker: int
    teleopUnampedSpeaker: int
    stage: int
    harmony: int
    trap: int

    stageTotal: int

    speakerCycles: int

    climbing: int
    difference: int

    def __init__(self) -> None:
        self.total = 0
        self.leaves = 0
        self.autoAmp = 0
        self.autoSpeaker = 0
        self.teleopAmp = 0
        self.teleopSpeakerScores = 0
        self.teleopSpeakerPoints = 0
        self.teleopAmpedSpeaker = 0
        self.teleopUnampedSpeaker = 0
        self.stage = 0
        self.harmony = 0
        self.trap = 0

        self.stageTotal = 0

        self.speakerCycles = 0

        self.climbing = 0
        self.difference = 0

isInMain = lambda mainCSV, h: h in mainCSV[0]
isBlueAlliance = lambda pos: pos[0] == 'b'

def findHeader(csv: CSV, header: str) -> int:
    for i in range(len(csv[0])):
        if csv[0][i] == header:
            return i
    return -1

def isolateCycleTime(csv: CSV) -> CSV:
    global id
    newCSV = CSV()
    headers = ['ID', 'Match Level', 'Match #', 'Team #', 'Cycle Time', 'Teleop Scoring Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        times = csv[i][findHeader(csv, CYCLE_TIMES)].split(",")
        locations = csv[i][findHeader(csv, TELE_SCORE_LOCS)].split(",")
        if(times[0] == '' or locations[0] == ''):
            continue
        for i2 in range(len(times)) if len(times) < len(locations) else range(len(locations)):
            newRow: list[str] = []
            for header in headers:
                if isInMain(csv, header):
                    newRow.append(csv[i][findHeader(csv, header)])
                elif header == headers[4]:
                    newRow.append(times[i2])
                elif header == headers[5]:
                    newRow.append(locations[i2])
                elif header == headers[0]:
                    newRow.append(id)
                    id += 1
            newCSV.append(newRow)
    return newCSV

def isolateTeleMisses(csv: CSV) -> CSV:
    global id
    newCSV = CSV()
    headers = ['ID', 'Match Level', 'Match #', 'Team #', 'Teleop Miss Location']
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
                elif header == headers[0]:
                    newRow.append(id)
                    id += 1
                else:
                    newRow.append(location)
            newCSV.append(newRow)
    return newCSV

def isolateAutoScores(csv: CSV) -> CSV:
    global id
    newCSV = CSV()
    headers = ['ID', 'Match Level', 'Match #', 'Team #', 'Auto Score Location']
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
                elif header == headers[0]:
                    newRow.append(id)
                    id += 1
                else:
                    newRow.append(location)
            newCSV.append(newRow)
    return newCSV

def isolateAutoPickupLocations(csv: CSV) -> CSV:
    global id
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Team #', 'Auto Pickup Location']
    newCSV.append(headers)
    for i in range(1, len(csv)):
        locations = csv[i][findHeader(csv, AUTO_PICKUP_LOCS)].split(',')
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
    newCSV.append(['ID', 'Match Level', 'Match #', 'Team #', 'Location'])
    file = open(outputPath + '/CycleTimes.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'ID':
            continue
        newRow = []
        newRow.append(row[0])
        newRow.append(row[1])
        newRow.append(row[2])
        newRow.append(row[3])
        newRow.append(row[5])
        newCSV.append(newRow)
    file.close()
    file = open(outputPath + '/TeleopMisses.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'ID':
            continue
        newCSV.append(row)
    file.close()
    file = open(outputPath + '/AutoScores.csv', encoding='utf-8')
    csvReader = csvStuff.reader(file)
    for row in csvReader:
        if row[0] == 'ID':
            continue
        newCSV.append(row)
    file.close()
    return newCSV

def allianceToList(scores: AllianceScores, matchLevel: str, matchNum: str, alliance: str) -> list[str]:
    row = []
    row.append(matchLevel)
    row.append(matchNum)
    row.append(alliance)
    row.append(scores.total)
    row.append(scores.leaves)
    row.append(scores.autoAmp)
    row.append(scores.autoSpeaker)
    row.append(scores.teleopAmp)
    row.append(scores.teleopSpeakerScores)
    row.append(scores.teleopUnampedSpeaker)
    row.append(scores.teleopAmpedSpeaker)
    row.append(scores.stage)
    row.append(scores.harmony)
    row.append(scores.difference)
    row.append(scores.trap)

    return row

def addAllianceToData(csv: CSV) -> CSV:
    newCSV = CSV()
    newCSV.append(csv[0])
    newCSV[0].append("Alliance")
    for i in range(1, len(csv)):
        newCSV.append(csv[i])
        start = csv[i][findHeader(csv, 'Robot')]
        newCSV[i].append('blue' if isBlueAlliance(start) else 'red')
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

def writeOutputToFile(fileName: str, func):
    global output_path
    csvFile = open(output_path + "/" + fileName + ".csv", 'w', encoding='utf-8')
    global rows
    csv = func(rows)
    writer = csvStuff.writer(csvFile, lineterminator='\n')
    writer.writerows(csv)

writeOutputToFile("CycleTimes", isolateCycleTime)
writeOutputToFile("TeleopMisses", isolateTeleMisses)
writeOutputToFile("AutoPickups", isolateAutoPickupLocations)
writeOutputToFile("AutoScores", isolateAutoScores)
# writeOutputToFile("AllianceScores", isolateAllianceScores)
writeOutputToFile("DataWithAlliance", addAllianceToData)

with open(output_path + "/AllLocations.csv", 'w', encoding='utf-8') as csvFile: # All locations requires special handling
    locationsCSV = isolateLocations(output_path)
    writer = csvStuff.writer(csvFile, lineterminator='\n')
    writer.writerows(locationsCSV)