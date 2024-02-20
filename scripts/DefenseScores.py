import tkinter as tk
from tkinter import filedialog
import csv as csvStuff
import numpy as np

from typing import Callable

CSV = list[list[str]]

inMain = lambda csv, head: head in csv[0]

def findHeader(csv: CSV, header: str) -> int:
    for i in range(len(csv[0])):
        if header == csv[0][i]:
            return i
    return None

isRed: Callable[[str], bool] = lambda bot: bot == 'r1' or 'r2' or 'r3'
diffTeam: Callable[[str, str], bool] = lambda bot1, bot2: bot1[0] != bot2[0]
getHead: Callable[[CSV, int, str], str] = lambda src, idx, head: src[idx][findHeader(src, head)]

time_avgs: dict[int, float] = {}

def populateAvgs(source: CSV):
    global time_avgs
    for i in range(1, len(source)):
        team = int(getHead(source, i, 'Team #'))
        if not (team in time_avgs.keys()):
            times: list[float] = []
            for i2 in range(i, len(source)):
                if team == int(getHead(source, i2, 'Team #')):
                    cycles: list[str] = getHead(source, i2, 'Cycle Timer').split(',')
                    if cycles[0] == '':
                        continue
                    for cycle in cycles:
                        times.append(float(cycle))
            time_avgs[team] = np.average(times)

def calcScore(source: CSV, matchStart: int, matchNum: int, bot: str) -> float:
    global time_avgs
    times: dict[int, float] = {}
    for i in range(matchStart, len(source)):
        if int(getHead(source, i, 'Match #')) != matchNum:
            return np.average([times[team] - time_avgs[team] for team in times.keys()])
        if diffTeam(bot, getHead(source, i, 'Robot')) and getHead(source, i, 'Robot') != bot:
            cycles = getHead(source, i, 'Cycle Timer').split(',')
            if cycles[0] == '':
                continue
            times[int(getHead(source, i, 'Team #'))] = np.average([float(cycles[i]) for i in range(len(cycles))])

def appendScores(csv: CSV, scores: dict[int, float], matchNum: int):
    for team in scores.keys():
        csv.append([matchNum, team, scores[team]])

def calcScores(source: CSV) -> CSV:
    global time_avgs
    output = CSV()
    matchStartIndex = 1
    prevMatch = 1
    headers = ['Match #', 'Team #', 'Score']
    output.append(headers)
    scores: dict[int, float] = {}
    for i in range(1, len(source)):
        if int(getHead(source, i, 'Match #')) != prevMatch:
            appendScores(output, scores, prevMatch)
            scores = {}
            matchStartIndex = i
            prevMatch = int(getHead(source, i, 'Match #'))
        if getHead(source, i, 'Played Defense') == '1':
            scores[int(getHead(source, i, 'Team #'))] = calcScore(source, matchStartIndex, prevMatch, getHead(source, i, 'Robot'))
        if i == len(source) - 1:
            appendScores(output, scores, prevMatch)
    return output

root = tk.Tk()
root.withdraw()


mainPath = filedialog.askopenfilename()
sourceCSV = CSV()
with open(mainPath) as sourceFile:
    reader = csvStuff.reader(sourceFile)
    for row in reader:
        sourceCSV.append(row)

outputPath = filedialog.askdirectory()
populateAvgs(sourceCSV)

with open(outputPath + "/DefenseScores.csv", 'w', encoding='utf-8') as file:
    writer = csvStuff.writer(file)
    writer.writerows(calcScores(sourceCSV))