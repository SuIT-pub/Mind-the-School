init -98 python:
    # 0 = no loli content (High School age: 18-22)
    # 1 = slight loli content (Middle School age: 13-17, High School age: 18-22)
    # 2 = hard loli content (Elementary School age: 8-12, Middle School age: 13-17, High School age: 18-22)
    loli_content = 0
    cheat_mode = False
    nude_vision = 2
    sfw_mode = False
    event_selection_mode = False

    location_event_register = {}
    event_register = {}
    fragment_storage_register = {}

    loli_filter = {}
    get_loli_filter()

    members = ""
    download_members()

    message = ""
    download_message()

    # get_mod_list()
    
    repair_mod_list()
    available_keys = ['base']
    active_mod_key = ''
    mod_count = {}

    translation_texts = {}

    start_methods = []

init -95 python:
    get_translations()

default intro_dev_message = "This version of the game only includes content up to day 10, when free roaming begins. You can still play and roam from there, but there will be no content."

default hide_gui = False

default rules = {}
default buildings = {}
default clubs = {}
default charList = {
    'staff': {},
}

default person_storage = {}

default quests = {}

default money = Stat(MONEY, 1000)

default reserved_money = {}

default time = Time()
default stat_data = {}

default gameData = {}
default is_in_replay = False
default replay_data = {}

default event_data = {}

default overview_events_available = {
    'school_building':  False,
    'school_dormitory': False,
    'labs':             False,
    'sports_field':     False,
    'gym':              False,
    'swimming_pool':    False,
    'cafeteria':        False,
    'bath':             False,
    'kiosk':            False,
    'courtyard':        False,
    'office_building':  False,
    'beach':            False,
    'staff_lodges':     False}
default overview_highlight_available = {
    'school_building':  False,
    'school_dormitory': False,
    'labs':             False,
    'sports_field':     False,
    'gym':              False,
    'swimming_pool':    False,
    'cafeteria':        False,
    'bath':             False,
    'kiosk':            False,
    'courtyard':        False,
    'office_building':  False,
    'beach':            False,
    'staff_lodges':     False}

define audio.forest_ambience = "forest-ambience.mp3"
define audio.night_ambience = "night-ambience.mp3"
define audio.empty_room = "empty-room.mp3"
define audio.muffled_chatter = "muffled-chatter.mp3"
define audio.cafeteria_empty = "cafeteria-empty.mp3"
define audio.cafeteria_chatter = "cafeteria-chatter.mp3"
define audio.gym_active = "gym-active.mp3"

default available_proficiencies = ['math', 'pe']
default headmaster_proficiencies = {}

init -99:
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

    define character.dev = Character(
        "Suit-Kun",
        # window_background = get_textbox(),
        who_color = "#00ff11",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.headmaster = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.headmaster_whisper = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        what_italic = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.headmaster_shout = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        who_suffix = " (shouting)",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        what_bold = True,
        # what_outlines=[( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.headmaster_thought = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        who_suffix = " (thinking)",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        what_italic = True,
        what_prefix = "(  ",
        what_suffix = "  )",
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.secretary = Character(
        "Emiko Langley",
        #window_background = None,
        who_color = "#c71585",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.secretary_whisper = Character(
        "Emiko Langley",
        who_suffix = " (whispering)",
        #window_background = None,
        who_color = "#c71585",
        what_color = "#ffffff",
        what_size = 28,
        what_italic = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.secretary_shout = Character(
        "Emiko Langley",
        who_suffix = " (shouting)",
        #window_background = None,
        who_color = "#c71585",
        what_color = "#ffffff",
        what_size = 28,
        what_bold = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher = Character(
        "Teacher", 
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher_shout = Character(
        "Teacher", 
        who_suffix = " (shouting)",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        what_bold = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher_whisper = Character(
        "Teacher", 
        who_suffix = " (whispering)",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        what_italic = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher1 = Character(
        "Lily Anderson",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher2 = Character(
        "Yulan Chen",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher3 = Character(
        "Finola Ryan",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher4 = Character(
        "Chloe Garcia",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.teacher5 = Character(
        "Zoe Parker",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )

    define character.vendor = Character(
        "Vendor",
        #window_background = None,
        who_color = "#601561",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0)],
        retain = False,
    )

    define character.parent = Character(
        "Parent",
        #window_background = None,
        who_color = "#e6e6fa",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0)],
        retain = False,
    )
    define character.examiner = Character(
        "Examiner",
        #window_background = None,
        who_color = "#f5deb3",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.regional = Character(
        "Region Manager",
        #window_background = None,
        who_color = "#4169e1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.sgirl = Character(
        "School Girl",
        #window_background = None,
        who_color = "#8a2be2",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.sboy = Character(
        "School Boy",
        #window_background = None,
        who_color = "#008000",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.crowd = Character(
        "Crowd",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.crowd_whisper = Character(
        "Crowd",
        who_suffix = " (whispering)",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        what_italics = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.crowd_shout = Character(
        "Crowd",
        who_suffix = " (shouting)",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        what_bold = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
    )
    define character.subtitles = Character(
        None,
        #window_background = None,
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
        what_xalign = 0.5,
        what_textalign = 0,
        what_layout = 'subtitle'
    )
    define character.subtitles_Empty = Character(
        None,
        window_background = None,
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
        retain = False,
        what_xalign = 0.5,
        what_textalign = 0,
        what_layout = 'subtitle'
    )

    define character.nv_text = Character(None, kind=nvl, what_text_align=0.5, what_xalign=0.5)
