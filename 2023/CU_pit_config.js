const pitScouting = true;
var requiredFields = ["e", "s", "t"];
var config_data = {
  title: "ScoutingPASS 3173",
  page_title: "ScoutingPASS 3173 - PIT SCOUTING",
  prematch: {
    Prematch: {
      code: "prm-div",
      title: "Pregame",
      type: "divider",
      text: 'Fill in "Team Number" field',
    },
    "Scouter Name": {
      code: "s",
      title: "Scouter Name",
      type: "scouter",
      size: 10,
      maxSize: 20,
    },
    Event: {
      code: "e",
      title: "Event",
      type: "event",
      defaultValue: "2023nyrr",
      disabled: "true",
    },
    "Team Number": {
      code: "t",
      title: "Team Number",
      type: "team",
      min: 1,
      max: 9999,
    },
    Robot: {
      code: "r-div",
      title: "Robot Questions",
      type: "divider",
    },
    "Drive Base": {
      code: "db",
      title: "Drive Base",
      type: "radio",
      choices: {
        Swerve: "Swerve<br>",
        Tank: "Tank<br>",
        Mechanum: "Mecanum<br>",
        Other: "Other<br>",
      },
    },
    "Picks Up From Ground": {
      code: "tpg",
      title: "Picks Up From Ground",
      type: "radio",
      choices: {
        Cone: "Cone<br>",
        Cube: "Cube<br>",
        B: "Both<br>",
        N: "Neither<br>",
      },
      defaultValue: "N",
    },
    "Picks Up From Chute": {
      code: "tpc",
      title: "Picks Up From Chute",
      type: "radio",
      choices: {
        Cone: "Cone<br>",
        Cube: "Cube<br>",
        B: "Both<br>",
        N: "Neither<br>",
      },
      defaultValue: "N",
    },
    "Picks Up From Shelf": {
      code: "tps",
      title: "Picks Up From Shelf",
      type: "radio",
      choices: {
        Cone: "Cone<br>",
        Cube: "Cube<br>",
        B: "Both<br>",
        N: "Neither<br>",
      },
      defaultValue: "N",
    },
    "Auto Charging Pad Level": {
      code: "ac",
      title: "Engage Charging Pad in Auto?",
      type: "bool",
    },
    "Auto Routines": {
      code: "ar",
      title: "Autonomous Routines",
      type: "text",
      size: 30,
    },
    Team: {
      code: "t-div",
      title: "Team Questions",
      type: "divider",
    },
    "Num Batteries": {
      code: "nb",
      title: "Batteries Owned",
      type: "counter",
    },
    "Hours Practiced": {
      code: "ph",
      title: "Hours of Driver Practice",
      type: "counter",
    },
    Comments: {
      code: "co",
      title: "Comments",
      type: "text",
      maxSize: 100,
    },
  },
};
