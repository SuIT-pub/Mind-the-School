##############################################################################
# Changelog shown on the main menu ("What's new", a fold-out sheet).
#
# Newest version first. Each version: (title, [section, ...]); each section:
# (heading or "", [line, ...]); a line is a string, or (string, 1) for a
# sub point. Text tags work ({a=url}...{/a}). Older versions belong in the wiki
# (CHANGELOG_FOOTER links there), so only keep the last few here.
##############################################################################

define CHANGELOG = [
    ("Version 0.2.1B_1", [
        ("", [
            "Made small optimization, reducing size of save files",
            "Fixed mixup of yoga outfits",
            "Fixed missing images in event",
        ]),
    ]),
    ("Version 0.2.1B", [
        ("", [
            "Fixed missing character names in events",
            "Fixed some stat changes missing in events",
        ]),
    ]),
    ("Version 0.2.1A", [
        ("", [
            "Fixed Truth or Dare Event Chain not triggering",
            "Fixed New Yoga Outfit Event Chain not triggering",
            "Fixed some keywords not being named correctly",
            "Added missing events and images for sex ed teaching",
            "Added Debug feature in journal allowing for reading in-game values",
        ]),
    ]),
    ("Version 0.2.1", [
        ("", [
            "Added live notifications to main menu",
            "Fixed Replay Gallery crashing to map overview, when handling decisions during replay",
            "Fixed Event in School Dorm and Building showing for level it is not planned for",
            "Fixed missing images in a School Dorm Event",
        ]),
        ("Stats", [
            "1379 new images bringing it up to a total of 7233",
            "21 new animations bringing it up to a total of 203",
            "2 new event chains",
            "20 new events",
            ("one with over 12 fragments", 1),
        ]),
        ("Events", [
            "Added event chain for new yoga outfits",
            ("10 new events", 1),
            "Added event chain for truth or dare",
            ("4 new events", 1),
            ("12 new event fragments", 1),
            "2 new events in gym",
            "2 new events in school building",
            "1 new event in office building",
            "Reworked teaching pe classes to conform to new image creation workflow",
            "Improved Composite Events to allow easier usage of fragments",
        ]),
        ("New Features", [
            "added ambient sound to map and location overview",
        ]),
        ("Changes", [
            "Changed methods for creating menus",
            "unified stat sets of students, parents and teachers to one single set",
            "reworked PTA voting system",
        ]),
        ("Stats", [
            "Stats for students, teachers and parents have been merged into one representing the entire school",
            "each party keeps its own set of stats due to compatibility concerns",
            ("all sets are not in use except for the student set, which is now the main set", 1),
            ("all parties still keep their own progression level", 1),
        ]),
        ("PTA", [
            "Voting system and probability calculation has been overhauled",
            ("rework in accordance to the new stat system", 1),
            ("instead of the parties voting on the same set of conditions based on their own stats, the parties now vote on their own set of conditions together with one shared set", 1),
            ("probability calculation has been simplified.", 1),
            ("calculation is still in testing phase", 1),
            ("it is possible, that the probability shown in the journal does not match the one measured in the pta itself.", 1),
            ("probability in journal is based on the voting probability of all three parties, while in PTA the three parties all calculate their own probability separately", 1),
        ]),
        ("Characters", [
            "Introducing Linh Nguyen",
            "Enhanced character retrieval for use in events",
        ]),
        ("GUI", [
            "Added button to skip to the next day in map overview",
        ]),
        ("Quest System", [
            "Updated quest system to include new events",
            "Rework of Quest System is in progress. Please do not report non-game-breaking bugs for the quest system.",
            "Quest system only shows the current state of the game and has no influence on the game itself.",
        ]),
        ("Misc", [
            "Fixed multiple bugs",
        ]),
    ]),
]

define CHANGELOG_FOOTER = "Changelog for older versions can be found in the {a=https://mts-game.com/wiki/Changelog}wiki{/a}."
