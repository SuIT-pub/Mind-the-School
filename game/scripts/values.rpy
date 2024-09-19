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

    translation_texts = {}
    get_translations()

    loli_filter = {}
    get_loli_filter()

    members = ""
    download_members()

    get_mod_list()
    active_mod_key = ''

default intro_dev_message = "This version of the game only includes content up to day 10, when free roaming begins. You can still play and roam from there, but there will be no content."

default hide_gui = False

default rules = {}
default buildings = {}
default clubs = {}
default charList = {
    'staff': {},
}

default quests = {}

default money = Stat(MONEY, 1000)

default reserved_money = {}

default time = Time()
default stat_data = {}

default gameData = {}
default is_in_replay = False
default replay_data = {}

default event_data = {}

default overview_events_available = {}

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
    )
    define character.headmaster = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.headmaster_whisper = Character(
        "[headmaster_first_name] [headmaster_last_name]",
        #window_background = None,
        who_color = "#ffffff",
        what_color = "#ffffff",
        what_size = 28,
        what_italic = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
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
    )
    define character.secretary = Character(
        "Emiko Langley",
        #window_background = None,
        who_color = "#c71585",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
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
    )
    define character.teacher = Character(
        "Teacher", 
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.teacher1 = Character(
        "Lily Anderson",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.teacher2 = Character(
        "Yulan Chen",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.teacher3 = Character(
        "Finola Ryan",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.teacher4 = Character(
        "Chloe Garcia",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.teacher5 = Character(
        "Zoe Parker",
        #window_background = None,
        who_color = "#00ced1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )

    define character.vendor = Character(
        "Vendor",
        #window_background = None,
        who_color = "#601561",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0)],
    )

    define character.parent = Character(
        "Parent",
        #window_background = None,
        who_color = "#e6e6fa",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0)],
    )
    define character.examiner = Character(
        "Examiner",
        #window_background = None,
        who_color = "#f5deb3",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.regional = Character(
        "Region Manager",
        #window_background = None,
        who_color = "#4169e1",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.sgirl = Character(
        "School Girl",
        #window_background = None,
        who_color = "#8a2be2",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.sboy = Character(
        "School Boy",
        #window_background = None,
        who_color = "#008000",
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.crowd = Character(
        "Crowd",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.crowd_whisper = Character(
        "Crowd",
        who_suffix = " (whispering)",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        what_italics = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.crowd_shout = Character(
        "Crowd",
        who_suffix = " (shouting)",
        #window_background = None,
        what_color = "#ffd700",
        what_size = 28,
        what_bold = True,
        # what_outlines = [( 1, "#000000", 0, 0 )],
    )
    define character.subtitles = Character(
        None,
        #window_background = None,
        what_color = "#ffffff",
        what_size = 28,
        # what_outlines = [( 1, "#000000", 0, 0 )],
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
        what_xalign = 0.5,
        what_textalign = 0,
        what_layout = 'subtitle'
    )

    define character.nv_text = Character(None, kind=nvl, what_text_align=0.5, what_xalign=0.5)
