const {test} = require("@playwright/test")
const fs = require("fs/promises");

const convertToCSV = (arr) => {
    const array = [Object.keys(arr[0])].concat(arr)

    return array.map(it => {
        return Object.values(it)
    }).join('\n')
}

const ROBOT_POSITIONS = [
    "r1",
    "r2",
    "r3",
    "b1",
    "b2",
    "b3",
];

const TEAM_NUMBERS = [
    "108",
    "1523",
    "1744",
    "179",
    "180",
    "2152",
    "2383",
    "3173",
    "3390",
    "348",
    "3627",
    "3932",
    "4206",
    "4388",
    "5410",
    "5472",
    "5557",
    "5842",
    "5872",
    "59",
    "6300",
    "6317",
    "6686",
    "6743",
    "694",
    "744",
    "7652",
    "7833",
    "806",
    "8752",
    "8775",
    "8817",
    "8861",
    "9040",
    "9402",
    "9404",
    "9693",
    "9725",
    "9779"
];

const EVENT_KEY = "2024flwp";
const MATCH_LEVEL = "qm";
const SCOUT_NAME = "JK";

const FINAL_STATUS = [
    0,
    1,
    2,
    3,
];

const LEGAL_SCORING_POSITIONS = [
    "tc1",
    "tc2",
    "tc3",
    "tc4",
    "tap",
    "tan",
];

const getRandomInt = (max) => {
    return Math.floor(Math.random() * max);
};

const getRandomTrueFalse = () => {
    return !!getRandomInt(2);
};

const getWeightedTrueFalse = (weight) => {
    return (Math.floor(Math.random() * 100) < weight) + 0;
}

const getRandomFinalStatus = () => {
    return FINAL_STATUS[getRandomInt(FINAL_STATUS.length)];
}

const getRandomScoringLocation = () => {
    return LEGAL_SCORING_POSITIONS[getRandomInt(LEGAL_SCORING_POSITIONS.length)];
}

const getRandomScoringLocations = (maxScores, robotPos) => {
    var out = "";
    for (var i = 0; i < maxScores; i++) {
        out = out + getRandomScoringLocation(robotPos).toString() + ",";
    }
    if (out.length > 0) out = out.slice(0, -1);
    return out;
}

const getRandomCycleTime = (max) => {
    return (Math.random() * max).toFixed(1);
}

const getCycleTimes = (numCycles) => {
    var out = "";
    for (var i = 0; i < numCycles; i++) {
        out = out + getRandomCycleTime(30).toString() + ",";
    }
    if (out.length > 0) out = out.slice(0, -1);
    return out;
}

const getCycleNumbers = (numCycles) => {
    const level4Coral = getRandomInt(numCycles);
    const level3Coral = getRandomInt(numCycles - level4Coral);
    const level2Coral = getRandomInt(numCycles - level4Coral - level3Coral);
    const level1Coral = getRandomInt(numCycles - level4Coral - level3Coral - level2Coral);
    const algaeProcessor = getRandomInt(numCycles - level4Coral - level3Coral - level2Coral - level1Coral);
    const algaeNet = numCycles - level4Coral - level3Coral - level2Coral - level1Coral - algaeProcessor;
    return [level4Coral, level3Coral, level2Coral, level1Coral, algaeProcessor, algaeNet];
}

test("Create 2025 Event Test Data", async () => {
    const outputArray = [];
    const cycleArray = [];
    var teamIterator = 0;
    for (var matchNum = 1; matchNum <= 100; matchNum++) {
        for (var robotPos = 0; robotPos < 6; robotPos++) {
            const numCycles = getRandomInt(20);
            const [level4Coral, level3Coral, level2Coral, level1Coral, algaeProcessor, algaeNet] = getCycleNumbers(numCycles);
            const [autolevel4Coral, autolevel3Coral, autolevel2Coral, autolevel1Coral, autoAlgaeProcessor, autoAlgaeNet] = getCycleNumbers(getRandomInt(4));
            const algaeFromReef = getRandomInt(algaeNet+algaeProcessor);
            const finalStatus = getRandomFinalStatus();
            const outputObject = {
                "Scouter Name": SCOUT_NAME,
                "Event": EVENT_KEY,
                "Match Level": MATCH_LEVEL,
                "Match #": matchNum,
                "Robot": ROBOT_POSITIONS[robotPos],
                "Team #": TEAM_NUMBERS[teamIterator++],
                "Auto Coral Level 4": autolevel4Coral,
                "Auto Coral Level 3": autolevel3Coral,
                "Auto Coral Level 2": autolevel2Coral,
                "Auto Coral Level 1": autolevel1Coral,
                "Auto Algae Processor": autoAlgaeProcessor,
                "Auto Algae Net": autoAlgaeNet,
                "Cycle Timer": "\"" + getCycleTimes(numCycles) + "\"",
                "Cycle Type": "\"" + getRandomScoringLocations(numCycles) + "\"",
                "Teleop Coral Level 4": level4Coral,
                "Teleop Coral Level 3": level3Coral,
                "Teleop Coral Level 2": level2Coral,
                "Teleop Coral Level 1": level1Coral,
                "Teleop Algae Processor": algaeProcessor,
                "Teleop Algae Net": algaeNet,
                "Teleop Algae Removed From Reef": algaeFromReef,
                "Pickup From Floor": getWeightedTrueFalse(20),
                "Pickup From Coral Station": getWeightedTrueFalse(80),
                "Endgame State": finalStatus,
                "Played Defense": getWeightedTrueFalse(30),
                "Was Defended": getWeightedTrueFalse(30),
                "Died": getWeightedTrueFalse(10),
                "Tippy": getWeightedTrueFalse(10),
                "Yellow Card": getWeightedTrueFalse(4),
                "Red Card": getWeightedTrueFalse(1),
                "Egregiously Bad Event": getWeightedTrueFalse(10),
                "Comment": "comment here",
            }
            outputArray.push(outputObject);
            const cycleTimes = outputObject["Cycle Timer"].replace(/"/g, '').split(',');
            const cycleTypes = outputObject["Cycle Type"].replace(/"/g, '').split(',');
            for (var count = 0; count < cycleTimes.length; count++){
                const cycleOutputObject = {
                    "Scouter Name": SCOUT_NAME,
                    "Event": EVENT_KEY,
                    "Match Level": MATCH_LEVEL,
                    "Match #": matchNum,
                    "Robot": ROBOT_POSITIONS[robotPos],
                    "Team #": TEAM_NUMBERS[teamIterator-1],
                    "Cycle Time": cycleTimes[count],
                    "Cycle Type": cycleTypes[count],
                }
                cycleArray.push(cycleOutputObject);
            }
            if (teamIterator >= TEAM_NUMBERS.length) teamIterator = 0;
        }
    }

    await fs.writeFile(
        "C:\\Source\\personal\\ScoutingPASS\\tests\\teleop.csv",
        convertToCSV(cycleArray),
    );
    await fs.writeFile(
        "C:\\Source\\personal\\ScoutingPASS\\tests\\full.csv",
        convertToCSV(outputArray),
    );
});