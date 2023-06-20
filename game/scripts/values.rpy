init python:
    
    def level_to_string(school = ""):

        high_school_level = str(schools["high_school"].get_level())
        if high_school_level == "10":
            high_school_level = "A"

        middle_school_level = str(schools["middle_school"].get_level())
        if middle_school_level == "10":
            middle_school_level = "A"

        elementary_school_level = str(schools["elementary_school"].get_level())
        if elementary_school_level == "10":
            elementary_school_level = "A"
        
        if school == "high_school":
            return high_school_level
        elif school == "middle_school":
            return middle_school_level
        elif school == "elementary_school":
            return elementary_school_level
        else:
            return high_school_level + ':' + middle_school_level + ':' + elementary_school_level

    def level_to_num(school = ""):
        return schools[school].get_level()

        return -1

    def clamp_stat(value):
        if (value < 0):
            return 0
        if (value > 100):
            return 100
        return value

    loli_content = 0


default character.principal = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.principal_whisper = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.principal_shout = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 35,
    what_outlines=[( 1, "#000000", 0, 0 )],
)
default character.principal_thought = Character(
    "Principal",
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    italics = True,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_whisper = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_shout = Character(
    "Secretary",
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 35,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher = Character(
    "Teacher", 
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.parent = Character(
    "Parent",
    who_color = "#e6e6fa",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0)],
)
default character.examiner = Character(
    "Examiner",
    who_color = "#f5deb3",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.regional = Character(
    "Region Manager",
    who_color = "#4169e1",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sgirl = Character(
    "School Girl",
    who_color = "#8a2be2",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sboy = Character(
    "School Boy",
    who_color = "#008000",
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_whisper = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 15,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_shout = Character(
    "Crowd",
    what_color = "#ffd700",
    what_size = 35,
    what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.subtitles = Character(
    None,
    # window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)
default character.subtitles_Empty = Character(
    None,
    window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)

default rules = {}

default school_name = "Windstor School"
default principal_name = "Mark"

default buildings = {}

default clubs = {}

default stat_data = {}

default schools = {}

default money = Stat("money", 1000)

default time = Time()

default voteProposal = None

# 0 = no loli content (High School age: 18-22)
# 1 = slight loli content (Middle School age: 13-17, High School age: 18-22)
# 2 = hard loli content (Elementary School age: 8-12, Middle School age: 13-17, High School age: 18-22)
# default loli_content = 0
