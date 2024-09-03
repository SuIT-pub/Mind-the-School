# The game starts here.

label start ():

    $ set_dissolve()

    call load_stats from start_1
    call load_schools from start_2
    call load_buildings from start_3
    call load_clubs from start_4
    call load_rules from start_5

    $ fix_modifier()

    call intro from _call_intro
label splashscreen:
    menu:
        "This game is not suitable for children or those who are easily disturbed.\n\nBy playing this game you agree that you are 18 years of age or older and are not offended by adult content."

        "I am 18 years of age or older.":
            pass
        "I am not 18 years of age or older.":
            $ renpy.quit()

    subtitles "The game downloads the current list of {a=https://www.patreon.com/suitji}Patreon{/a} supporters every time the game starts. The file's size is max 1KB. If you don't want the game to download this file, you can disable it in the options menu."
    subtitles "For everyone with an old save-game from the previous version:\nYou can still open the game with the old save-game. If you encounter an error after loading because of a missing image, just press 'Ignore' and the game will continue normally."
init python:
    
    ###########################################
    # --- Version Compatibility Functions --- #
    ###########################################

    def check_stats_compatibility():
        """
        Check if the stats are compatible with the current version
        """

        school = get_character_by_key("school")
        parent = get_character_by_key("parent")
        teacher = get_character_by_key("teacher")
        secretary = get_character_by_key("secretary")

        map(lambda: x._repair(), school.get_stats().values())
        map(lambda: x._repair(), parent.get_stats().values())
        map(lambda: x._repair(), teacher.get_stats().values())
        map(lambda: x._repair(), secretary.get_stats().values())

        if time.today_is_after_date(9, 1, 2023):
            if school.get_level() == 0:
                school.set_level(1)
            if parent.get_level() == 0:
                parent.set_level(1)
            if teacher.get_level() == 0:
                teacher.set_level(1)
            if secretary.get_level() == 0:
                secretary.set_level(5)

    def fix_modifier():
        """
        Fix the modifiers for the new version
        """

        # add weekly cost for cafeteria if not already added
        if (get_building('cafeteria').is_unlocked() and 
            get_modifier('weekly_cost_cafeteria', 'money', None, 'payroll_weekly') == None
        ):
            set_modifier('weekly_cost_cafeteria', Modifier_Obj('Cafeteria', "+", -100), stat = 'money', collection = 'payroll_weekly')

        if get_modifier('monthly_budget', 'money', None, 'payroll_monthly') == None:
            set_modifier('monthly_budget', Modifier_Obj('Budget', "+", 1000), stat = 'money', collection = 'payroll_monthly')

        if get_modifier('teacher_pay', 'money', None, 'payroll_weekly') == None:
            set_modifier('teacher_pay', Modifier_Obj('Teacher', "+", -150), stat = 'money', collection = 'payroll_weekly')
    
    def fix_schools():
        """
        Fix the schools for the new version
        Merges the multiple schools from 0.1.2 into one school
        """

        fix_thinking_characters(character.headmaster_thought)
        fix_shouting_characters(character.headmaster_shout)
        fix_whisper_characters(character.headmaster_whisper)
        fix_shouting_characters(character.secretary_shout)
        fix_whisper_characters(character.secretary_whisper)
        fix_shouting_characters(character.crowd_shout)
        fix_whisper_characters(character.crowd_whisper)


        old_character = get_character("school_mean_values", charList)
        if old_character != None:
            max_level = 0
            high_school = get_character("high_school", charList['schools'])
            middle_school = get_character("middle_school", charList['schools'])
            elementary_school = get_character("elementary_school", charList['schools'])
            if high_school != None:
                max_level = max(max_level, high_school.get_level())

            old_character.name = "school"
            old_character.title = "School"
            old_character.level = Stat("level", max_level)
            charList["school"] = old_character
            charList.pop("school_mean_values")
        if 'schools' in charList:
            charList['schools'].pop("high_school")
            charList['schools'].pop("middle_school")
            charList['schools'].pop("elementary_school")
            charList.pop('schools')

        load_character("school", "School", charList, {
            'stats_objects': {
                "corruption": Stat(CORRUPTION, 0),
                "inhibition": Stat(INHIBITION, 100),
                "happiness": Stat(HAPPINESS, 12),
                "education": Stat(EDUCATION, 9),
                "charm": Stat(CHARM, 8),
                "reputation": Stat(REPUTATION, 7),
            }
        })

    def fix_whisper_characters(person: Person):
        """
        Fix the whispering characters for the new version
        """

        person.who_suffix = " (whispering)"
        fix_characters(person)

    def fix_shouting_characters(person: Person):
        """
        Fix the shouting characters for the new version
        """

        person.who_suffix = " (shouting)"
        fix_characters(person)

    def fix_thinking_characters(person: Person):
        """
        Fix the thinking characters for the new version
        """

        person.who_suffix = " (thinking)"
        fix_characters(person)
    
    def fix_characters(person: Person):
        """
        Fix the characters for the new version
        """

        person.what_size = 28
        person.what_italic = True
        person.what_prefix = "(  {i}"
        person.what_suffix = "{/i}  )"

    def check_old_versions():
        """
        Check for old versions and apply the necessary fixes
        """

        if 'headmaster_first_name' in gameData.keys() and 'headmaster_last_name' in gameData.keys():
            set_name("headmaster", gameData['headmaster_first_name'], gameData['headmaster_last_name'])
            gameData.pop('headmaster_first_name')
            gameData.pop('headmaster_last_name')

    ###########################################

label after_load:
    $ log('\n\n\n####################################################################################################\n####################################################################################################\n')

    call load_stats from after_load_1
    call load_schools from after_load_2
    call load_rules from after_load_3
    call load_buildings from after_load_4
    call load_clubs from after_load_5
    
    #####################################
    # check for version incompatibilities
    $ check_old_versions()

    $ check_stats_compatibility()

    $ fix_modifier()
    ####################################

    if contains_game_data("names") and "headmaster" in get_game_data("names"):
        $ headmaster_first_name = get_game_data("names")["headmaster"][0]
        $ headmaster_last_name = get_game_data("names")["headmaster"][1]

    #################
    # load all events
    $ after_load_event_check('daily', None, time_check_events, temp_time_check_events)
    $ after_load_event_check('bath', bath_events, bath_general_event, bath_timed_event)
    $ after_load_event_check('cafeteria', cafeteria_events, cafeteria_general_event, cafeteria_timed_event)
    $ after_load_event_check('courtyard', courtyard_events, courtyard_general_event, courtyard_timed_event)
    $ after_load_event_check('gym', gym_events, gym_general_event, gym_timed_event)
    $ after_load_event_check('kiosk', kiosk_events, kiosk_general_event, kiosk_timed_event)
    $ after_load_event_check('labs', labs_events, labs_general_event, labs_timed_event)
    $ after_load_event_check('office_building', office_building_events, office_building_general_event, office_building_timed_event)
    $ after_load_event_check('school_building', sb_events, sb_general_event, sb_timed_event)
    $ after_load_event_check('school_dormitory', sd_events, sd_general_event, sd_timed_event)
    $ after_load_event_check('sports_field', sports_field_events, sports_field_general_event, sports_field_timed_event)
    $ after_load_event_check('swimming_pool', swimming_pool_events, swimming_pool_general_event, swimming_pool_timed_event)
    $ after_load_event_check('beach', beach_events, beach_general_event, beach_timed_event)
    $ after_load_event_check('staff_lodges', staff_lodges_events, staff_lodges_general_event, staff_lodges_timed_event)
    #################

    return