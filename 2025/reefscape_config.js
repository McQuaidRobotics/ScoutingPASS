var requiredFields = ["e", "m", "l", "r", "s"];
var config_data = {
  dataFormat: "noSpace",
  title: "Scouting PASS 2025",
  page_title: "Reefscape 3173",
  checkboxAs: "10",
  prematch: [
    {
      name: "Scouter Name",
      code: "s",
      type: "scouter",
      size: 5,
      maxSize: 5,
      required: "true",
    },
    {
      name: "Event",
      code: "e",
      type: "event",
      defaultValue: "2025dal",
      required: "true",
      disabled: "true",
    },
    {
      name: "Match Level",
      code: "l",
      type: "level",
      choices: {
        qm: "Quals<br>",
        sf: "Semifinals<br>",
        f: "Finals",
      },
      defaultValue: "qm",
      required: "true",
    },
    {
      name: "Match #",
      code: "m",
      type: "match",
      min: 1,
      max: 150,
      required: "true",
    },
    {
      name: "Robot",
      code: "r",
      type: "robot",
      choices: {
        r1: "Red-1",
        b1: "Blue-1<br>",
        r2: "Red-2",
        b2: "Blue-2<br>",
        r3: "Red-3",
        b3: "Blue-3",
      },
      required: "true",
    },
    { name: "Team #", code: "t", type: "team", min: 1, max: 99999 },
    { name: "Autonomous", code: "a-div", title: "Autonomous", type: "divider" },
    { name: "Auto Coral Level 4", code: "ac4", type: "counter" },
    { name: "Auto Coral Level 3", code: "ac3", type: "counter" },
    { name: "Auto Coral Level 2", code: "ac2", type: "counter" },
    { name: "Auto Coral Level 1", code: "ac1", type: "counter" },
    { name: "Auto Coral Miss", code: "acm", type: "counter" },
    { name: "Auto Algae Processor", code: "aap", type: "counter" },
    { name: "Auto Algae Net", code: "aan", type: "counter" },
    { name: "Auto Algae Remove From Reef", code: "aar", type: "counter" },
    { name: "Leave", code: "al", type: "bool" },
    { name: "Teleop", code: "t-div", title: "Teleoperated", type: "divider" },
    {
      name: "Cycle Timer",
      code: "tct",
      type: "cycle",
      showUndo: "true",
      showCycle: "false",
      storeCycleType: "tcty",
    },
    { name: "Cycle Type", code: "tcty", type: "cycleType" },
    {
      name: "Teleop Coral Level 4",
      code: "tc4",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tc4",
      valueAttribute: "tcty",
    },
    {
      name: "Teleop Coral Level 3",
      code: "tc3",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tc3",
      valueAttribute: "tcty",
    },
    {
      name: "Teleop Coral Level 2",
      code: "tc2",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tc2",
      valueAttribute: "tcty",
    },
    {
      name: "Teleop Coral Level 1",
      code: "tc1",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tc1",
      valueAttribute: "tcty",
    },
    { name: "Teleop Coral Miss", code: "tcm", type: "counter" },
    { name: "Teleop Algae Removed From Reef", code: "tar", type: "counter" },
    {
      name: "Teleop Algae Processor",
      code: "tap",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tap",
      valueAttribute: "tcty",
    },
    {
      name: "Teleop Algae Net",
      code: "tan",
      type: "counter",
      cycleTimer: "tct",
      valueInput: "tan",
      valueAttribute: "tcty",
    },
    { name: "Teleop Algae Miss", code: "tam", type: "counter" },
    { name: "Pickup Coral From Floor", code: "tpf", type: "bool" },
    { name: "Pickup From Coral Station", code: "tps", type: "bool" },
    { name: "Endgame", code: "e-div", title: "Endgame", type: "divider" },
    {
      name: "Endgame State",
      code: "tes",
      type: "radio",
      choices: {
        0: "None<br>",
        1: "Park<br>",
        2: "Shallow Climb<br>",
        3: "Deep Climb",
      },
      defaultValue: "0",
    },
    { name: "Postmatch", code: "p-div", title: "Post Match", type: "divider" },
    {
      name: "Played Defense",
      code: "ppd",
      type: "bool",
    },
    { name: "Was Defended", code: "pwd", type: "bool" },
    { name: "Died/Immobilized", code: "die", type: "bool" },
    { name: "Tippy<br>(almost tipped over)", code: "tip", type: "bool" },
    { name: "Good Driver", code: "pgd", type: "bool" },
    { name: "Bad Driver", code: "pbd", type: "bool" },
    { name: "Yellow Card", code: "pyc", title: "Yellow Card", type: "bool" },
    { name: "Red Card", code: "prc", title: "Red Card", type: "bool" },
    {
      name: "Egregiously Bad Event Occurred (put info in comments)",
      code: "peb",
      title: "Egregiously Bad",
      type: "bool",
    },
    { name: "Comments", code: "co", type: "text", size: 15, maxSize: 255 },
  ],
};
