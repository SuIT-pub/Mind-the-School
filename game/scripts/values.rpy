init -98 python:
    # 0 = no loli content (High School age: 18-22)
    # 1 = slight loli content (Middle School age: 13-17, High School age: 18-22)
    # 2 = hard loli content (Elementary School age: 8-12, Middle School age: 13-17, High School age: 18-22)
    loli_content = 0
    cheat_mode = False
    nude_vision = 2
    sfw_mode = False
    
    seenEvents = {}
    location_event_register = {}
    event_register = {}

    translation_texts = {}
    get_translations()

    loli_filter = {}
    get_loli_filter()

default intro_dev_message = "This version of the game only includes content up to day 10, when free roaming begins. You can still play and roam from there, but there will be no content."

default hide_gui = False

default rules = {}
default buildings = {}
default clubs = {}
default charList = {
    'staff': {},
}

default money = Stat(MONEY, 1000)
default time = Time()
default stat_data = {}

default gameData = {}
default is_in_replay = False
default replay_data = {}

default event_data = {}

default default_names = {
    'headmaster': ('Mark', 'Benson'),
    'secretary': ('Emiko', 'Langley'),
    'teacher1': ('Lily', 'Anderson'),
    'teacher2': ('Yulan', 'Chen'),
    'teacher3': ('Finola', 'Ryan'),
    'teacher4': ('Chloe', 'Garcia'),
    'teacher5': ('Zoe', 'Parker'),
    'vendor': ('Vendor', ''),
    'parent1': ('Adelaide', 'Hall'),
    'parent2': ('Nubia', 'Davis'),
    'parent3': ('Yuki', 'Yamamoto'),
}

default headmaster_first_name = default_names['headmaster'][0]
default headmaster_last_name = default_names['headmaster'][1]

default character.dev = Character(
    "Suit-Kun",
    # window_background = get_textbox(),
    who_color = "#00ff11",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.headmaster = Character(
    "[headmaster_first_name] [headmaster_last_name]",
    #window_background = None,
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.headmaster_whisper = Character(
    "[headmaster_first_name] [headmaster_last_name]",
    #window_background = None,
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 15,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.headmaster_shout = Character(
    "[headmaster_first_name] [headmaster_last_name]",
    #window_background = None,
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 35,
    # what_outlines=[( 1, "#000000", 0, 0 )],
)
default character.headmaster_thought = Character(
    "[headmaster_first_name] [headmaster_last_name]",
    #window_background = None,
    who_color = "#ffffff",
    what_color = "#ffffff",
    what_size = 28,
    italics = True,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary = Character(
    "Emiko Langley",
    #window_background = None,
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_whisper = Character(
    "Emiko Langley",
    #window_background = None,
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 15,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.secretary_shout = Character(
    "Emiko Langley",
    #window_background = None,
    who_color = "#c71585",
    what_color = "#ffffff",
    what_size = 35,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher = Character(
    "Teacher", 
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher1 = Character(
    "Lily Anderson",
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher2 = Character(
    "Yulan Chen",
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher3 = Character(
    "Finola Ryan",
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher4 = Character(
    "Chloe Garcia",
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.teacher5 = Character(
    "Zoe Parker",
    #window_background = None,
    who_color = "#00ced1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)

default character.vendor = Character(
    "Vendor",
    #window_background = None,
    who_color = "#601561",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0)],
)

default character.parent = Character(
    "Parent",
    #window_background = None,
    who_color = "#e6e6fa",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0)],
)
default character.examiner = Character(
    "Examiner",
    #window_background = None,
    who_color = "#f5deb3",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.regional = Character(
    "Region Manager",
    #window_background = None,
    who_color = "#4169e1",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sgirl = Character(
    "School Girl",
    #window_background = None,
    who_color = "#8a2be2",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.sboy = Character(
    "School Boy",
    #window_background = None,
    who_color = "#008000",
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd = Character(
    "Crowd",
    #window_background = None,
    what_color = "#ffd700",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_whisper = Character(
    "Crowd",
    #window_background = None,
    what_color = "#ffd700",
    what_size = 15,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.crowd_shout = Character(
    "Crowd",
    #window_background = None,
    what_color = "#ffd700",
    what_size = 35,
    # what_outlines = [( 1, "#000000", 0, 0 )],
)
default character.subtitles = Character(
    None,
    #window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)
default character.subtitles_Empty = Character(
    None,
    window_background = None,
    what_color = "#ffffff",
    what_size = 28,
    # what_outlines = [( 1, "#000000", 0, 0 )],
    what_xalign = 0.5,
    what_textalign = 0,
    what_layout = 'subtitle'
)

default character.nv_text = Character(None, kind=nvl, what_text_align=0.5, what_xalign=0.5)
