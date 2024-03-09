import requests
import csv
import sys
from typing import Callable

from Config import API_KEY, MATCH_KEY

TBA_BASE_URL = 'https://www.thebluealliance.com/api/v3'
HEADERS = {'X-TBA-Auth-Key': API_KEY}

stage_scores = {
    'None': 0,
    'Parked': 1,
    'OnStage': 3,
    'Spotlit': 4
}

offstage_status = ['None', 'Parked']

alliances = ['red', 'blue']
robot_tags = ['Robot1', 'Robot2', 'Robot3']
end_game = 'endGame'
taxied = 'autoLine'
trap = 'trap'
harmony_points = 'endGameHarmonyPoints'

def finalStatus(match: dict, alliance: str, bot: str) -> str:
    status = match['score_breakdown'][alliance][end_game+bot]
    if status not in offstage_status:
        if bool(match['score_breakdown'][alliance]['mic'+status]):
            return 'Spotlit'
        else:
            return 'OnStage'
    else:
        return status
    
def trapStatus(match: dict, alliance: str, bot: str) -> bool:
    status = match['score_breakdown'][alliance][end_game+bot]
    if status not in offstage_status:
        return bool(match['score_breakdown'][alliance][trap+status])
    else:
        return False

team_num: Callable[[dict, str, int], str] = lambda match, alliance, bot: match['alliances'][alliance]['team_keys'][bot][3:]
taxis: Callable[[dict, str, str], bool] = lambda match, alliance, bot: True if match['score_breakdown'][alliance][taxied+bot] == 'Yes' else False
other_alliance: Callable[[str], str] = lambda alliance: 'blue' if alliance == 'red' else 'red'
fouls: Callable[[dict, str, bool], str] = lambda match, alliance, tech: match['score_breakdown'][alliance]['foulCount' if not tech else 'techFoulCount']
red_card: Callable[[dict, str, str], bool] = lambda match, alliance, bot: 'frc'+bot in match['alliances'][alliance]['dq_team_keys']
g424: Callable[[dict, str], bool] = lambda match, alliance: bool(match['score_breakdown'][alliance]['g424Penalty'])

total: Callable[[dict, str], str] = lambda match, alliance: match['alliances'][alliance]['score']

info_headers = ['Event', 'Match #', 'Alliance', 'Team #', 'Taxis', 'Final Status', 'Trap', 'Fouls Caused', 'Tech Fouls Caused', 'Red Card', 'Caused 424', 'Can Harmonize']
score_headers = ['Event', 'Match #', 'Alliance', 'Total Score', 'Auto Total Score', 'Taxi Score', 'Auto Speaker Scores', 'Auto Amp Scores', 'Teleop Total Note Score', 'Teleop Unamped Speaker Score', 'Teleop Amped Speaker Score', 'Teleop Amp Score', 'Total Stage Score', 'Final Status Score', 'Trap Score', 'Harmony Score', 'Total Foul Score', 'Fouls Score', 'Tech Fouls Score']
ranking_headers = ['Event', 'Ranking', 'Team #', 'Total Ranking Points', 'g424 Ranking Points', 'Avg Total Ranking Points', 'Avg Coop Ranking Points', 'Avg Match Score', 'Avg Auto Points', 'Avg Stage Points']

matches_req = requests.get(TBA_BASE_URL + f'/event/{MATCH_KEY}/matches', headers=HEADERS)
matches = matches_req.json()

match_nums = [int(match['match_number']) if match['comp_level'] == 'qm' else None for match in matches]

g424_counts: dict[str, int] = {}

newCSV: list[list[str]] = []
newCSV.append(info_headers)
for i in range(1, len(match_nums)):
    try:
        match_idx = match_nums.index(i)
        for alliance in alliances:
            bots: list[list[str]] = []
            climb_pos: dict[str, str] = {}
            for idx, bot in enumerate(robot_tags):
                row: list[str] = []
                row.append(MATCH_KEY)
                row.append(str(i))
                row.append(alliance)
                num = team_num(matches[match_idx], alliance, idx)
                row.append(num)
                row.append(int(taxis(matches[match_idx], alliance, bot)))
                pos = matches[match_idx]['score_breakdown'][alliance][end_game+bot]
                if(pos not in offstage_status):
                    climb_pos[num] = pos
                else:
                    climb_pos[num] = None
                row.append(finalStatus(matches[match_idx], alliance, bot))
                row.append(int(trapStatus(matches[match_idx], alliance, bot)))
                row.append(fouls(matches[match_idx], alliance, False))
                row.append(fouls(matches[match_idx], alliance, True))
                row.append(int(red_card(matches[match_idx], alliance, team_num(matches[match_idx], alliance, idx))))
                row.append(int(g424(matches[match_idx], alliance)))
                if g424(matches[match_idx], other_alliance(alliance)):
                    try:
                        g424_counts['frc'+num] += 1
                    except (KeyError):
                        g424_counts['frc'+num] = 1
                bots.append(row)
            for idx, bot in enumerate(climb_pos.keys()):
                if climb_pos[bot] != None:
                    for idx2, bot2 in enumerate(climb_pos.keys()):
                        if bot == bot2 and idx2 != 2:
                            continue
                        elif idx2 == 2:
                            bots[idx].append(str(0))
                        else:
                            if climb_pos[bot] == climb_pos[bot2]:
                                bots[idx].append(str(1))
                                break
                            elif idx2 == 2:
                                bots[idx].append(str(0))
                else:
                    bots[idx].append(str(0))
                newCSV.append(bots[idx])

    except(ValueError):
        break

file = open(sys.argv[1]+'/TBAInfo.csv', 'w', encoding='utf-8')
writer = csv.writer(file, lineterminator='\n')
writer.writerows(newCSV)

newCSV = []
newCSV.append(score_headers)
for i in range(1, len(match_nums)):
    try:
        match_idx = match_nums.index(i)
        for alliance in alliances:
            total_final_status: int = 0
            total_trap: int = 0
            for bot in robot_tags:
                total_final_status += stage_scores[finalStatus(matches[match_idx], alliance, bot)]

            row: list[str] = []
            row.append(MATCH_KEY)
            row.append(str(i))
            row.append(alliance)
            row.append(total(matches[match_idx], alliance))
            row.append(matches[match_idx]['score_breakdown'][alliance]['autoPoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['autoLeavePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['autoSpeakerNotePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['autoAmpNotePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['teleopTotalNotePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['teleopSpeakerNotePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['teleopSpeakerNoteAmplifiedPoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['teleopAmpNotePoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['endGameTotalStagePoints'])
            row.append(str(total_final_status))
            row.append(matches[match_idx]['score_breakdown'][alliance]['endGameNoteInTrapPoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['endGameHarmonyPoints'])
            row.append(matches[match_idx]['score_breakdown'][alliance]['foulPoints'])
            row.append(matches[match_idx]['score_breakdown'][other_alliance(alliance)]['foulCount'] * 2)
            row.append(matches[match_idx]['score_breakdown'][other_alliance(alliance)]['techFoulCount'] * 5)
            newCSV.append(row)
    except(ValueError):
        break

file = open(sys.argv[1]+'/TBAAllianceScores.csv', 'w', encoding='utf-8')
writer = csv.writer(file, lineterminator='\n')
writer.writerows(newCSV)

ranking_req = requests.get(TBA_BASE_URL + f'/event/{MATCH_KEY}/rankings', headers=HEADERS)
ranks = ranking_req.json()

newCSV = []
newCSV.append(ranking_headers)
for rank in ranks['rankings']:
    row: list[str] = []
    row.append(MATCH_KEY)
    row.append(rank['rank'])
    team = rank['team_key']
    row.append(team[3:])
    row.append(rank['extra_stats'][0])
    try:
        row.append(g424_counts[team])
    except (KeyError):
        row.append(0)
    row.append(rank['sort_orders'][0])
    row.append(rank['sort_orders'][1])
    row.append(rank['sort_orders'][2])
    row.append(rank['sort_orders'][3])
    row.append(rank['sort_orders'][4])

file = open(sys.argv[1]+'/TBARankingInfo.csv', 'w', encoding='utf-8')
writer = csv.writer(file, lineterminator='\n')
writer.writerows(newCSV)