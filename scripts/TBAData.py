import requests
import csv
import sys
from typing import Callable

from Config import API_KEY, MATCH_KEY

TBA_BASE_URL = 'https://www.thebluealliance.com/api/v3'
HEADERS = {'X-TBA-Auth-Key': API_KEY}

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

csv_headers = ['Event', 'Match #', 'Alliance', 'Team #', 'Taxis', 'Final Status', 'Trap']

matches_req = requests.get(TBA_BASE_URL + f'/event/{MATCH_KEY}/matches', headers=HEADERS)
matches = matches_req.json()

match_nums = [int(match['match_number']) if match['comp_level'] == 'qm' else None for match in matches]

newCSV: list[list[str]] = []
newCSV.append(csv_headers)
for i in range(1, len(match_nums)):
    try:
        match_idx = match_nums.index(i)
        for alliance in alliances:
            for idx, bot in enumerate(robot_tags):
                row: list[str] = []
                row.append(MATCH_KEY)
                row.append(str(i))
                row.append(alliance)
                row.append(team_num(matches[match_idx], alliance, idx))
                row.append(int(taxis(matches[match_idx], alliance, bot)))
                row.append(finalStatus(matches[match_idx], alliance, bot))
                row.append(int(trapStatus(matches[match_idx], alliance, bot)))
                newCSV.append(row)
    except(ValueError):
        break


file = open(sys.argv[1]+'/TBAInfo.csv', 'w', encoding='utf-8')
writer = csv.writer(file, lineterminator='\n')
writer.writerows(newCSV)