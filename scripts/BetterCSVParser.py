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
    penalty: int

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
        self.penalty = 0

        self.speakerCycles = 0

        self.climbing = 0
        self.difference = 0
    
    def setInvalid(self):
        self.teleopAmpedSpeaker = -1
        self.teleopUnampedSpeaker = -1

isInMain = lambda mainCSV, h: h in mainCSV[0]
isBlueAlliance = lambda pos: pos == 1 or pos == 13 or pos == 35 \
    or pos == 37 or pos == 49 or pos == 61

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
        for i2 in range(len(times)):
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

def calcAmpedVsUnampedExact(totalCycles: int, speakerScore: int, climbing: int) -> list[int]:
    for harmony in range(climbing + 1):
        harmony_points = 0 if harmony == 0 else (harmony - 1) * 2
        for unamped in range(totalCycles + 1):
            amped = totalCycles - unamped
            if unamped * 2 + amped * 5 + harmony_points == speakerScore:
                return [unamped * 2, amped * 5, harmony_points]
    return None

def calcAmpedVsUnampedClosest(totalCycles: int, speakerScore: int, climbing: int) -> tuple[int, list[int]]:
    minDiff: int = 1e16
    res: list[int] = []

    for harmony in range(climbing + 1):
        harmony_points = 0 if harmony == 0 else (harmony - 1) * 2

        for unamped in range(totalCycles + 1):
            amped = totalCycles - unamped
            diff = abs(speakerScore - (unamped * 2 + amped * 5 + harmony_points))
            if(diff < minDiff):
                minDiff = diff
                res = [unamped * 2, amped * 5, harmony_points]
    
    return res

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
    row.append(scores.penalty)

    return row

def isolateAllianceScores(csv: CSV) -> CSV:
    newCSV = CSV()
    headers = ['Match Level', 'Match #', 'Alliance', 'Total Score', 'Leaves Start', 'Auto Amp Points', 'Auto Speaker Points', 'Teleop Amp Points', 'Speaker Cycles', 'Teleop Unamped Points', 'Teleop Amped Points', 'Stage Points', 'Harmony Points', 'Difference', 'Trap Points', 'Penalty Points']
    newCSV.append(headers)
    red = AllianceScores()
    blue = AllianceScores()
    prevMatch = 1
    for i in range(1, len(csv)):
        if int(csv[i][findHeader(csv, 'Match #')]) != prevMatch:
            red.teleopSpeakerPoints = red.total - red.leaves - red.autoAmp - red.autoSpeaker - red.teleopAmp - red.stage - red.trap - red.penalty
            blue.teleopSpeakerPoints = blue.total - blue.leaves - blue.autoAmp - blue.autoSpeaker - blue.teleopAmp - blue.stage - blue.trap - blue.penalty
            scores: list[int] = None
            scores = calcAmpedVsUnampedExact(red.teleopSpeakerScores, red.teleopSpeakerPoints, red.climbing)
            if scores == None:
                close = calcAmpedVsUnampedClosest(red.teleopSpeakerScores, red.teleopSpeakerPoints, red.climbing)
                red.difference = close[0]
                red.teleopUnampedSpeaker = close[1][0]
                red.teleopAmpedSpeaker = close[1][1]
                red.harmony = close[1][2]
            else:
                red.difference = 0
                red.teleopUnampedSpeaker = scores[0]
                red.teleopAmpedSpeaker = scores[1]
                red.harmony = scores[2]

            scores = None
            scores = calcAmpedVsUnampedExact(blue.teleopSpeakerScores, blue.teleopSpeakerPoints, blue.climbing)
            if scores == None:
                close = calcAmpedVsUnampedClosest(blue.teleopSpeakerScores, blue.teleopSpeakerPoints, blue.climbing)
                blue.difference = close[0]
                blue.teleopUnampedSpeaker = close[1][0]
                blue.teleopAmpedSpeaker = close[1][1]
                blue.harmony = close[1][2]
            else:
                blue.difference = 0
                blue.teleopUnampedSpeaker = scores[0]
                blue.teleopAmpedSpeaker = scores[1]
                blue.harmony = scores[2]

            redRow = allianceToList(red, csv[i - 1][findHeader(csv, 'Match Level')], str(prevMatch), 'red')
            blueRow = allianceToList(blue, csv[i - 1][findHeader(csv, 'Match Level')], str(prevMatch), 'blue')

            newCSV.append(redRow)
            newCSV.append(blueRow)

            red = AllianceScores()
            blue = AllianceScores()

            prevMatch = int(csv[i][findHeader(csv, 'Match #')])
        start = int(csv[i][findHeader(csv, 'Auto Start Location')])
        alliance = blue if isBlueAlliance(start) else red

        alliance.total = int(csv[i][findHeader(csv, 'Alliance Score')])
        alliance.leaves += int(csv[i][findHeader(csv, 'Leave Starting Zone')]) * 2
        alliance.autoAmp += int(csv[i][findHeader(csv, 'Auto Amp Scores')]) * 2
        autoSpeaker = csv[i][findHeader(csv, 'Auto Scoring Locations')].split(',')
        alliance.autoSpeaker += (len(autoSpeaker) if autoSpeaker[0] != '' else 0) * 5
        teleopScores = csv[i][findHeader(csv, TELE_SCORE_LOCS)].split(',')
        teleopSpeaker = 0
        teleopAmp = 0
        for loc in teleopScores:
            if loc == 'a':
                teleopAmp += 1
            elif loc == '':
                continue
            else:
                teleopSpeaker += 1
        alliance.teleopAmp += teleopAmp
        alliance.teleopSpeakerScores += teleopSpeaker
        stageValue = csv[i][findHeader(csv, 'Final Status')]
        alliance.stage += 4 if stageValue == 's' else 3 if stageValue == 'o' else 1 if stageValue == 'p' else 0
        alliance.climbing += 1 if stageValue == 's' or 'o' else 0
        alliance.trap += int(csv[i][findHeader(csv, 'Note in Trap')]) * 5
        alliance.penalty = int(csv[i][findHeader(csv, 'Alliance Penalty Score')])

    red.teleopSpeakerPoints = red.total - red.leaves - red.autoAmp - red.autoSpeaker - red.teleopAmp - red.stage - red.trap - red.penalty
    blue.teleopSpeakerPoints = blue.total - blue.leaves - blue.autoAmp - blue.autoSpeaker - blue.teleopAmp - blue.stage - blue.trap - blue.penalty
    scores: list[int] = None
    scores = calcAmpedVsUnampedExact(red.teleopSpeakerScores, red.teleopSpeakerPoints, red.climbing)
    if scores == None:
        close = calcAmpedVsUnampedClosest(red.teleopSpeakerScores, red.teleopSpeakerPoints, red.climbing)
        red.difference = close[0]
        red.teleopUnampedSpeaker = close[1][0]
        red.teleopAmpedSpeaker = close[1][1]
        red.harmony = close[1][2]
    else:
        red.difference = 0
        red.teleopUnampedSpeaker = scores[0]
        red.teleopAmpedSpeaker = scores[1]
        red.harmony = scores[2]

    scores = None
    scores = calcAmpedVsUnampedExact(blue.teleopSpeakerScores, blue.teleopSpeakerPoints, blue.climbing)
    if scores == None:
        close = calcAmpedVsUnampedClosest(blue.teleopSpeakerScores, blue.teleopSpeakerPoints, blue.climbing)
        blue.difference = close[0]
        blue.teleopUnampedSpeaker = close[1][0]
        blue.teleopAmpedSpeaker = close[1][1]
        blue.harmony = close[1][2]
    else:
        blue.difference = 0
        blue.teleopUnampedSpeaker = scores[0]
        blue.teleopAmpedSpeaker = scores[1]
        blue.harmony = scores[2]

    redRow = allianceToList(red, csv[i - 1][findHeader(csv, 'Match Level')], str(prevMatch), 'red')
    blueRow = allianceToList(blue, csv[i - 1][findHeader(csv, 'Match Level')], str(prevMatch), 'blue')

    newCSV.append(redRow)
    newCSV.append(blueRow)
    return newCSV

def addAllianceToData(csv: CSV) -> CSV:
    newCSV = CSV()
    newCSV.append(csv[0])
    newCSV[0].append("Alliance")
    for i in range(1, len(csv)):
        newCSV.append(csv[i])
        start = int(csv[i][findHeader(csv, 'Auto Start Location')])
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
with open(output_path + "/CycleTimes.csv", 'w', encoding='utf-8') as csvFile:
    timesCSV = isolateCycleTime(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(timesCSV)

with open(output_path + "/TeleopMisses.csv", 'w', encoding='utf-8') as csvFile:
    teleMissesCSV = isolateTeleMisses(rows)
    writer = csvStuff.writer(csvFile, lineterminator="\n")
    writer.writerows(teleMissesCSV)

with open(output_path + "/AutoPickups.csv", 'w', encoding='utf-8') as csvFile:
    autoMissesCSV = isolateAutoPickupLocations(rows)
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

with open(output_path + "/AllianceScores.csv", 'w', encoding='utf-8') as csvFile:
    scoresCSV = isolateAllianceScores(rows)
    writer = csvStuff.writer(csvFile, lineterminator='\n')
    writer.writerows(scoresCSV)

with open(output_path + "/DataWithAlliance.csv", 'w', encoding='utf-8') as csvFile:
    dataCSV = addAllianceToData(rows)
    writer = csvStuff.writer(csvFile, lineterminator='\n')
    writer.writerows(dataCSV)