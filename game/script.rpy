# The game starts here.

label start ():

    $ set_dissolve()

    call load_stats from start_1
    call load_schools from start_2
    call load_buildings from start_3
    call load_clubs from start_4
    call load_rules from start_5

    $ fix_modifier()

    jump ask_age

    return

init python:
    
    ###########################################
    # --- Version Compatibility Functions --- #
    ###########################################

    def check_stats_compatibility():
        school = get_character_by_key("school")
        parents = get_character_by_key("parents")
        teacher = get_character_by_key("teacher")
        secretary = get_character_by_key("secretary")

        map(lambda: x._repair(), school.get_stats().values())
        map(lambda: x._repair(), parents.get_stats().values())
        map(lambda: x._repair(), teacher.get_stats().values())
        map(lambda: x._repair(), secretary.get_stats().values())

    def fix_modifier():
        # add weekly cost for cafeteria if not already added
        if (get_building('cafeteria').is_unlocked() and 
            get_modifier('weekly_cost_cafeteria', 'money', None, 'payroll_weekly') == None
        ):
            set_modifier('weekly_cost_cafeteria', 'money', Modifier_Obj('Cafeteria', "+", -100), collection = 'payroll_weekly')

        if get_modifier('monthly_budget', 'money', None, 'payroll_monthly') == None:
            set_modifier('monthly_budget', 'money', Modifier_Obj('Budget', "+", 1000), collection = 'payroll_monthly')

        if get_modifier('teacher_pay', 'money', None, 'payroll_weekly') == None:
            set_modifier('teacher_pay', 'money', Modifier_Obj('Teacher', "+", -150), collection = 'payroll_weekly')

    def fix_schools():
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

    def check_old_versions():
        if 'headmaster_first_name' in gameData.keys() and 'headmaster_last_name' in gameData.keys():
            set_name("headmaster", gameData['headmaster_first_name'], gameData['headmaster_last_name'])
            gameData.pop('headmaster_first_name')
            gameData.pop('headmaster_last_name')


    ###########################################


label after_load:
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
    $ after_load_event_check('tennis_court', tennis_court_events, tennis_court_general_event, tennis_court_timed_event)
    #################