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
    "p",
    "o",
    "s",
    "x",
];

const LEGAL_BLUE_AS_START = [
    1, 13, 25, 37, 49, 61
];

const LEGAL_RED_AS_START = [
    12, 24, 36, 48, 60, 72
];

const LEGAL_RED_SHOOTING_POSITIONS = [
    7, 8, 9, 10, 11, 12, 
    19, 20, 21, 22, 23, 24,
    31, 32, 33, 34, 35, 36,
    43, 44, 45, 46, 47, 48,
    55, 56, 57, 58, 59, 60,
    67, 68, 69, 70, 71, 72,
];

const LEGAL_BLUE_SHOOTING_POSITIONS = [
    1, 2, 3, 4, 5, 6,
    13, 14, 15, 16, 17, 18,
    25, 26, 27, 28, 29, 30,
    37, 38, 39, 40, 41, 42,
    49, 50, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 66,
];

const LEGAL_BLUE_AUTO_PICKUP_POSITIONS = [1, 4, 7, 2, 5, 8, 11, 14];
const LEGAL_RED_AUTO_PICKUP_POSITIONS = [2, 5, 8, 11, 14, 3, 6, 9];

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
    return FINAL_STATUS[getRandomInt(4)];
}

const getRandomBlueStartingLocation = () => {
    return LEGAL_BLUE_AS_START[getRandomInt(6)];
}

const getRandomRedStartingLocation = () => {
    return LEGAL_RED_AS_START[getRandomInt(6)];
}

const getRandomBlueScoringLocation = () => {
    return getRandomInt(12)+(24*getRandomInt(12));
    //LEGAL_BLUE_SHOOTING_POSITIONS[getRandomInt(36)];
}

const getRandomRedScoringLocation = () => {
    return 12+getRandomInt(12)+(24*getRandomInt(12));
    //return LEGAL_RED_SHOOTING_POSITIONS[getRandomInt(36)];
}

const getStartingLocation = (robotPos) => {
    if(robotPos < 3) return getRandomRedStartingLocation();
    return getRandomBlueStartingLocation();
}

const getScoringLocation = (robotPos) => {
    if (robotPos < 3) return getRandomRedScoringLocation();
    return getRandomBlueScoringLocation();
}

const getRandomScoringLocations = (maxScores, robotPos) => {
    var out = "";
    for (var i = 0; i < maxScores; i++) {
        out = out + getScoringLocation(robotPos).toString() + ",";
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

const isAmpScore = (speakerScores, ampScores) => {
    if (speakerScores === 0) return true;
    if (ampScores === 0) return false;
    return getRandomTrueFalse();
}

const getRandomTeleopScoringLocations = (numCycles, robotPos, numAmps) => {
    var out = "";
    var speakerScores = numCycles - numAmps;
    for (var i = 0; i < numCycles; i++) {
        if (isAmpScore(speakerScores, numAmps)) {
            out = out + "a,";
            numAmps--;
        }
        else {
            out = out + getScoringLocation(robotPos).toString() + ",";
            speakerScores--;
        }
    }
    if (out.length > 0) out = out.slice(0, -1);
    return out;
}

const getRandomAutoPickupLocations = (numCycles, robotPos) => {
    if (numCycles > 8) return;
    const randomNumbersPicked = [];
    var outString = "";
    var i = 0;
    while (i < numCycles) {
        const randomAttempt = getRandomInt(8);
        if (!randomNumbersPicked.includes(randomAttempt)) {
            outString = outString + (robotPos < 3 ? LEGAL_RED_AUTO_PICKUP_POSITIONS[randomAttempt].toString() : LEGAL_BLUE_AUTO_PICKUP_POSITIONS[randomAttempt].toString()) + ",";
            randomNumbersPicked.push(randomAttempt);
            i++;
        }
    }
    if (outString.length > 0) outString = outString.slice(0, -1);
    return outString;
}

const calculateRobotScore = (leaveStart, autoAmp, autoCycles, teleopSpeaker, ampedSpeaker, teleopAmp, finalStatus, trapScore) => {
    var finalPoints = parseInt((leaveStart)*2) +
    parseInt((autoAmp) * 2) + 
    calculateSpeakerScore(autoCycles, teleopSpeaker, ampedSpeaker) +
    parseInt((teleopAmp) * 1) + 
    calculateStageScore(finalStatus, trapScore);
    return finalPoints;
}

const calculateSpeakerScore = (autoCycles, teleopSpeaker, ampedSpeaker) => {
    return parseInt((autoCycles) * 5) + 
    parseInt((teleopSpeaker) * 2) +
    parseInt((ampedSpeaker) * 5);
}

const calculateStageScore = (finalStatus, trapScore) => {
    var finalStatusPoints = 0;
    if (finalStatus === "p") finalStatusPoints = 1;
    else if (finalStatus === "o") finalStatusPoints = 3;
    else if (finalStatus === "s") finalStatusPoints = 4;
    return parseInt(finalStatusPoints) + 
    parseInt((trapScore) * 5);
}

test("Create 2024 Event Test Data", async () => {
    const outputArray = [];
    var teamIterator = 0;
    var allianceScore = 0;
    var allianceSpeakerScore = 0;
    var allianceStageScore = 0;
    for (var matchNum = 1; matchNum <= 100; matchNum++) {
        for (var robotPos = 0; robotPos < 6; robotPos++) {
            const numCycles = getRandomInt(11);
            const numAmps = getRandomInt(numCycles);
            const ampedSpeakers = getRandomInt(numCycles-numAmps);
            const autoPickups = getRandomInt(6);
            const autoCycles = getRandomInt(autoPickups);
            const leaveStart = getWeightedTrueFalse(80);
            const autoAmpScores = getRandomInt(3);
            const finalStatus = getRandomFinalStatus();
            const noteInTrap = getWeightedTrueFalse(20);
            const outputObject = {
                "Scouter Name": SCOUT_NAME,
                "Event": EVENT_KEY,
                "Match Level": MATCH_LEVEL,
                "Match #": matchNum,
                "Robot": ROBOT_POSITIONS[robotPos],
                "Team #": TEAM_NUMBERS[teamIterator++],
                "Auto Start Location": getStartingLocation(robotPos),
                "Leave Starting Zone": leaveStart,
                "Auto Amp Scores": autoAmpScores,
                "Auto Scoring Locations": "\"" + getRandomScoringLocations(autoCycles, robotPos) + "\"",
                "Auto Pickup Locations": "\"" + getRandomAutoPickupLocations(autoPickups, robotPos) + "\"",
                "Cycle Timer": "\"" + getCycleTimes(numCycles) + "\"",
                "Teleop Scoring Locations": "\"" + getRandomTeleopScoringLocations(numCycles, robotPos, numAmps) + "\"",
                "Teleop Missing Locations": "\"" + getRandomScoringLocations(getRandomInt(11), robotPos) + "\"",
                "Teleop Amp Scores": numAmps,
                "Pickup From Floor": getWeightedTrueFalse(60),
                "Pickup From Source": getWeightedTrueFalse(70),
                "Stage Timer": getRandomCycleTime(20),
                "Final Status": finalStatus,
                "Note in Trap": noteInTrap,
                "Speaker Score": 0,
                "Stage Score": 0,
                "Played Defense": getWeightedTrueFalse(30),
                "Died": getWeightedTrueFalse(10),
                "Tippy": getWeightedTrueFalse(10),
                "Dropped Notes": getWeightedTrueFalse(10),
                "Yellow Card": getWeightedTrueFalse(5),
                "Red Card": getWeightedTrueFalse(2),
                "Egregiously Bad Event": getWeightedTrueFalse(15),
                "Comment": "comment here",
            }
            outputArray.push(outputObject);
            allianceSpeakerScore += calculateSpeakerScore(autoCycles, numCycles-ampedSpeakers-numAmps, ampedSpeakers);
            allianceStageScore += calculateStageScore(finalStatus, noteInTrap);
            if (teamIterator % 3 === 0) {
                var onstageRobots = 0;
                if (outputArray[outputArray.length-1]["Final Status"] === "o") onstageRobots++;
                if (outputArray[outputArray.length-2]["Final Status"] === "o") onstageRobots++;
                if (outputArray[outputArray.length-3]["Final Status"] === "o") onstageRobots++;
                if (onstageRobots > 1) allianceStageScore += ((onstageRobots-1)*2);
                var spotlitRobots = 0;
                if (outputArray[outputArray.length-1]["Final Status"] === "s") spotlitRobots++;
                if (outputArray[outputArray.length-2]["Final Status"] === "s") spotlitRobots++;
                if (outputArray[outputArray.length-3]["Final Status"] === "s") spotlitRobots++;
                if (spotlitRobots > 1) allianceStageScore += ((spotlitRobots-1)*2);
                outputArray[outputArray.length-1]["Speaker Score"] = allianceSpeakerScore;
                outputArray[outputArray.length-1]["Stage Score"] = allianceStageScore;
                outputArray[outputArray.length-2]["Speaker Score"] = allianceSpeakerScore;
                outputArray[outputArray.length-2]["Stage Score"] = allianceStageScore;
                outputArray[outputArray.length-3]["Speaker Score"] = allianceSpeakerScore;
                outputArray[outputArray.length-3]["Stage Score"] = allianceStageScore;
                allianceSpeakerScore = 0;
                allianceStageScore = 0;
            }
            if (teamIterator >= TEAM_NUMBERS.length) teamIterator = 0;
        }
    }

    await fs.writeFile(
        "C:\\Source\\personal\\ScoutingPASS\\tests\\output3.csv",
        convertToCSV(outputArray),
    );
});